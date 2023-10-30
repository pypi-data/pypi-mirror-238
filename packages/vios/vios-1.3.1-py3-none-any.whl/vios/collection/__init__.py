"""本模块主要由工具函数构成, 且依赖server
>>> task: 从kernel兼容而来的各Scanner及任务描述例子
>>> uapi: 与前端进行交互, 如matplotlib画图、数据库查询、实时画图等, 详见各函数说明. 
"""

import json
import time
from collections import defaultdict
from pathlib import Path
from threading import current_thread

import dill
import git
import h5py
import numpy as np
from loguru import logger
from quark import connect, loads
from tqdm import tqdm
from waveforms import Waveform, wave_eval
from waveforms.scan_iter import StepStatus

from vios import SYSTEMQ, Task, select

from .task import Scan, Scanner

try:
    with open(SYSTEMQ / 'etc/bootstrap.json', 'r') as f:
        bootstrap = json.loads(f.read())

    srv = bootstrap['executor']
    cfg = bootstrap['quarkserver']
except Exception as e:
    print(e)
    srv = {"host": "127.0.0.1", "port": 2088}
    cfg = {}

print(srv)
sp = defaultdict(lambda: connect('QuarkServer', srv['host'], srv['port']))
_s = sp[current_thread().name]
_cs = connect('QuarkCanvas', port=2089)
_vs = connect('QuarkViewer', port=2086)


def submit(app: dict | Scan | Scanner, block: bool | float = False,
           path: str | Path = Path.cwd(), suffix: str = '0', encoding: bool = True,
           reset: list = [], dry_run: bool = False, preview: list = [], plot: bool = False):
    """转换继承自App的任务为server可执行任务

    Args:
        app (dict | Scan | Scanner): 任务基类, 必须实现circuits方法.
        block (bool | float, optional): 是否阻塞任务, 用于多个任务顺序执行.
        path (str | Path, optional): 线路文件读写路径. Defaults to Path.cwd().
        encoding (bool, optional): 是否序列化线路. Defaults to True.
        suffix (str, optional): 线路文件后缀, 用于多个任务循环时避免文件覆盖.
        reset (bool, optional): 任务开始前执行，重置设备指令列表, 如[('WRITE','Q0.waveform.Z','zero()','au')].
        dry_run (bool, optional): 是否跳过设备执行, 但波形正常计算可以显示, 用于debug.
        preview (list, optional): 需要实时显示的波形, 对应etc.preview.filter.

    Raises:
        TypeError: _description_


    任务字典整体分两个字段: toserver
    >>> metainfo (dict):
      > name (str): filename:/s21, filename表示数据将存储于filename.hdf5中, s21为实验名字, 以:/分隔
      > user (str): 实验者代号. 默认为usr. 
      > tid (int): 任务id, 全局唯一, 如不指定, 则由系统生成. 
      > priority (int): 优先级, 任务同时提交时, 优先级数值小的先执行. 默认为0. 
      > other (dict): 其他参数, 如shots、signal等, 作为kwds传递给ccompile(见envelope.assembler)
    >>> taskinfo (dict):
      > STEP (dict): 大写, 描述任务执行的变量(即for循环变量)与执行步骤(即for循环体)
      > CIRQ (list | str): 大写, 描述任务线路, 长度等于STEP中for循环变量长度. 可为空. 
      > INIT (list): 大写, 任务初始化设置. 可为空. 
      > RULE (list): 大写, 变量关系列表, 可为表达式或空, 如[f'<gate.rfUnitary.{q}.params.frequency>=<freq.{q}>']. 可为空. 
      > LOOP (dict): 大写, 定义循环执行所用变量, 与STEP中main的值对应, STEP中main所用变量为LOOP的子集
    """

    ss = sp[current_thread().name]
    if preview:
        ss.update('etc.preview.filter', preview)

    if isinstance(app, dict):
        t = Task(app, block)
        t.server = ss
        t.run()
        return t

    ss.feed(0, 0, {'reset': reset})

    app.toserver = 'ready'
    app.run(dry_run=True, quiet=True)
    time.sleep(3)

    filepath = Path(path)/f'{app.name.replace(".", "_")}_{suffix}.cirq'
    circuits = []
    with open(filepath, 'w', encoding='utf-8') as f:
        for step in tqdm(app.circuits(), desc='CircuitExpansion'):
            if isinstance(step, StepStatus):
                cc = step.kwds['circuit']
                if not encoding:
                    f.writelines(str(cc)+'\n')
                else:
                    f.writelines(str(dill.dumps(cc))+'\n')
                # circuits.append(cc)
            else:
                raise TypeError('Wrong type of step!')
    app.shape = [i+1 for i in step.index]

    loops = app.variables()
    sample = ss.query('station.sample')
    trigger = ss.query('station.triggercmds')

    toserver = Task(dict(metainfo={'name': f'{sample}:/{app.name.replace(".", "_")}_{suffix}',
                                   'user': ss.query('etc.username'),
                                   'tid': app.id,
                                   'priority': app.task_priority,
                                   'other': {'shots': app.shots,
                                             'signal': app.signal,
                                             #  'lib': app.lib, # WindowsPath error on Mac
                                             'align_right': app.align_right,
                                             'waveform_length': app.waveform_length,
                                             'autorun': not dry_run,
                                             'timeout': 1000.0}},

                         taskinfo={'STEP': {'main': ['WRITE', tuple(loops.keys())],  # 主循环，写波形等设置类操作
                                            'trigger': ['WRITE', 'trig'],  # 触发
                                            'READ': ['READ', 'read'],  # 读取
                                            },
                                   'INIT': [(f'{t.split(".")[0]}.CH1.Shot', app.shots, 'any') for t in trigger],
                                   'RULE': app.dependencies(),
                                   'CIRQ': str(filepath.resolve()) if not circuits else circuits,
                                   'LOOP': loops | {'trig': [(t, 0, 'au') for t in trigger]}
                                   }))

    toserver.server = ss
    toserver.canvas = _vs
    toserver.timeout = 1e9 if block else None
    toserver.show = plot

    toserver.app = app
    app.toserver = toserver
    app.run()
    app.bar()


def rollback(tid: int, replace: bool = False):
    """将cfg表回滚至指定的任务id

    Args:
        tid (int): 任务id,与submit中tid相同
        replace (bool, optional): 是否替换当前server中的cfg表. Defaults to False.

    Returns:
        dict: cfg表
    """
    try:
        ckpt = '/'.join([cfg['home'], 'cfg', cfg['checkpoint']])
        file = (SYSTEMQ/ckpt).with_suffix('.json')

        tree = git.Repo(file.resolve().parent).commit(select(tid)[-1]).tree
        cpkt: dict = loads(tree[file.name].data_stream.read().decode())
        if replace:
            _s.clear()
            for k, v in cpkt.items():
                _s.create(k, v)
        return cpkt
    except Exception as e:
        logger.error(f'Failed to rollback: {e}')


def get_data_by_tid(tid: int, shape: tuple | list = [], snapshot: bool = False):
    """根据任务id从hdf5获取数据

    Args:
        tid (int): 任务id
        shape (tuple|list): data shape, 如果不指定尝试从记录中推出,形如(*sweeps, *(shots, qubits))
        snapshot (bool): 是否返回cfg表, 默认为False

    Returns:
        tuple: 数据体、元信息、cfg表
    """
    filename, dataset = select(tid)[7:9]

    info, data = {}, {}
    with h5py.File(filename) as f:
        group = f[dataset]
        info = loads(dict(group.attrs)['snapshot'])
        if not shape:
            shape = []
            for k, v in info['taskinfo']['meta']['axis'].items():
                shape.extend(tuple(v.values())[0].shape)

        for k in group.keys():
            ds = group[f'{k}']
            data[k] = np.full((*shape, *ds.shape[1:]), 0, ds.dtype)
            data[k][np.unravel_index(np.arange(ds.shape[0]), shape)] = ds[:]

    snp = info['snapshot'] if info and snapshot else {}

    return {'data': data, 'meta': info['taskinfo']['meta'], 'snapshot': snp}


def showave(task: Task | int, index: int = 0,
            start: float = 0, stop: float = 99e-6, sample_rate: float = 6e9,
            keys: tuple = ('Q0',), stage: str = 'raw', step: str = 'main', backend: str = 'mpl'):
    if isinstance(task, Task):
        cmds = task.step(index)[stage][step]
    else:
        cmds = _s.review(task, index)[stage][step]

    _stop = round(stop * sample_rate)
    _start = round(start * sample_rate)
    # n = round((stop - start) * sample_rate)
    xt = np.arange(_stop - _start) / sample_rate + start

    wdict = {}
    if stage in ['ini', 'raw']:
        for target, (ctype, value, unit, kwds) in cmds.items():
            if kwds['target'].split('.')[0] not in keys:  # qubit name
                continue

            if isinstance(value, str):
                value = wave_eval(value)

            if isinstance(value, Waveform):
                wdict[target] = value(xt)
    elif stage in ['debug', 'trace']:
        for dev, chqval in cmds.items():
            if dev not in keys:  # device name
                continue
            for chq, value in chqval.items():
                if chq.endswith('Waveform'):
                    wdict[f'{dev}.{chq}'] = value[_start:_stop]

    if backend == 'mpl':
        import matplotlib.pyplot as plt
        sdict = {k: wdict[k] for k in sorted(wdict)}
        plt.figure()
        for i, (target, wave) in enumerate(sdict.items()):
            plt.plot(xt, wave+i*0)
        plt.legend(list(sdict))
    else:
        sdict = {k: {'xdata': xt, 'ydata': wdict[k]} for k in sorted(wdict)}
        _cs.plot([[sdict]])
