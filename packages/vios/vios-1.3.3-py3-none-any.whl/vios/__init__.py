# vios(Virtual Input and Output System)，主要定义设备驱动及执行流程，包含以下功能模块：

# 一、driver：设备驱动
#     1、所有驱动继承自BaseDriver，类名统一为Driver，并要求实现open/close/read/write四个方法。样板见VirtualDevice
#     2、以设备或厂家为名新建文件夹（并于其内新建__init__.py文件）放于driver/common内，将厂家提供的底层库（若有）置于其内

# 二、envelope：执行流程，见各模块说明

# 三、collection：一些与server相关的操作函数


import asyncio
import inspect
import json
import os
import sqlite3
import sys
import time
from functools import cached_property
from pathlib import Path
from threading import current_thread

import numpy as np
from loguru import logger

QUARK = Path.home()/'quark'

try:
    sql = sqlite3.connect(QUARK/'checkpoint.db', check_same_thread=False)
    with open(QUARK/'startup.json', 'r') as f:
        startup = json.loads(f.read())
        SYSTEMQ = Path(startup['site'])
    sys.path.append(SYSTEMQ.resolve())  # for python>=3.11.4
except Exception as e:
    logger.error(str(e))
    startup = {}
    SYSTEMQ = ''


try:
    from IPython import get_ipython

    shell = get_ipython().__class__.__name__
    if shell == 'ZMQInteractiveShell':
        from tqdm.notebook import tqdm  # jupyter notebook or qtconsole
    else:
        # ipython in terminal(TerminalInteractiveShell)
        # None(Win)
        # Nonetype(Mac)
        from tqdm import tqdm
except Exception as e:
    # not installed or Probably IDLE
    from tqdm import tqdm


def debug(circuit: list = [(('Measure', 0), 'Q1001')]):
    from .collection import _s
    from .envelope import ccompile, initialize
    initialize(_s.snapshot())
    return ccompile(0, {}, circuit, signal='iq')


def select(tid: int):
    try:
        return sql.execute(f'select * from task where tid={tid}').fetchall()[0]
    except Exception as e:
        logger.error(f'Record not found: {e}!')


class Progress(tqdm):
    """兼容JupyterProgressBar接口(from kernel)的实现
    """
    bar_format = '{desc} {percentage:3.0f}%|{bar}|{n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]'

    def __init__(self, desc='test', total=100, postfix='running'):
        super().__init__([], desc, total, ncols=None, colour='blue',
                         bar_format=self.bar_format, position=0, postfix=postfix)

    @property
    def max(self):
        return self.total

    @max.setter
    def max(self, value: int):
        self.reset(value)

    def goto(self, index: int):
        self.n = index
        self.refresh()

    def finish(self, success: bool = True):
        self.colour = 'green' if success else 'red'
        # self.set_description_str(str(success))


class Task(object):
    """适用于大量任务连续提交(如量子云), 获取任务状态、结果、进度等. 
    Args:
        task (dict): 任务描述
        timeout (float | None, optional):任务最大时长, 默认为None, 即任务执行完毕结束.

    任务样例见本模块下experiment. 使用方法: 
    >>> task = Task(s21) # s21 为task.py中字典描述
    >>> task.run()
    >>> task.bar() # 适用于notebook
    """

    handles = {}
    server = None
    canvas = None

    def __init__(self, task: dict, timeout: float | None = None, show: bool = False) -> None:
        """_summary_

        Args:
            task (dict): 任务描述，详见submit函数
            timeout (float | None, optional): 阻塞任务最大时间. Defaults to None.
            show (bool, optional): 是否实时画图. 默认为False.
        """
        self.task = task
        self.timeout = timeout
        self.show = show

        self.data: dict[str, np.ndarray] = {}  # 从server取回的数据
        self.meta = {}  # 坐标轴等描述类信息
        self.index = 0  # 当前已取回的数据数量
        self.last = 0  # 上一次获取的数据量

        self.thread = current_thread().name

    @cached_property
    def name(self):
        return self.task['metainfo'].get('name', 'Unknown')

    def run(self):
        self.stime = time.time()  # start time
        try:
            circuit = self.task['taskinfo']['CIRQ']
            if isinstance(circuit, list) and callable(circuit[0]):
                circuit[0] = inspect.getsource(circuit[0])
        except Exception as e:
            logger.error(f'Failed to get circuit: {e}')
        self.tid = self.server.submit(self.task)

    def cancel(self):
        self.server.cancel(self.tid)
        # self.clear()

    def save(self):
        self.server.save(self.tid)

    def result(self):
        meta = True if not self.meta else False
        res = self.server.fetch(self.tid, start=self.index, meta=meta)

        if isinstance(res, str):
            return self.data
        elif isinstance(res, tuple):
            if isinstance(res[0], str):
                return self.data
            data, self.meta = res
        else:
            data = res
        self.last = self.index
        self.index += len(data)
        # data.clear()
        self.process(data)

        if self.show:
            self.plot(not meta)

        return self.data

    def status(self, key: str = 'runtime'):
        if key == 'runtime':
            return self.server.track(self.tid)
        elif key == 'compile':
            return self.server.apply('status', user='task')
        else:
            return 'supported arguments are: {rumtime, compile}'

    def report(self):
        return self.server.report(self.tid)

    def step(self, index: int, stage: str = 'raw'):
        """获取任务中某一步的详细信息

        Args:
            index (int): 步数.
            stage (str, optional): 任务执行所经历的阶段. Defaults to 'raw'.包括:
                > ini: 编译生成的指令.
                > raw: 映射为硬件通道后的指令及收集好的相关参数.
                > ctx: 编译所用的上下文环境(ctx).
                > debug: 由设备返回的原始数据.
                > trace: 每个指令执行所用时间.

        Returns:
            _type_: _description_
        """
        if stage in ['ini', 'raw', 'ctx']:
            return self.server.review(self.tid, index)[stage]
        elif stage in ['debug', 'trace']:
            return self.server.track(self.tid, index)[stage]

    def process(self, data: list[dict]):
        """处理从server取回的数据

        Args:
            data (list[dict]): 一维数组, 其中每个元素均为dict, 即envelope.process函数返回值.
        """
        for dat in data:
            for k, v in dat.items():
                if k in self.data:
                    self.data[k].append(v)
                else:
                    self.data[k] = [v]

    def update(self):
        try:
            self.result()
        except Exception as e:
            logger.error(f'Failed to get result: {e}')

        status = self.status()['status']

        if status in ['Failed', 'Canceled']:
            self.stop(self.tid, False)
            return True
        elif status in ['Running']:
            self.progress.goto(self.index)
            return False
        elif status in ['Finished', 'Archived']:
            self.progress.goto(self.progress.max)
            if hasattr(self, 'app'):
                self.app.save()
            self.stop(self.tid)
            self.result()
            return True

    def clear(self):
        for tid, handle in self.handles.items():
            self.stop(tid)

    def stop(self, tid: int, success: bool = True):
        try:
            self.progress.finish(success)
            self.handles[tid].cancel()
        except Exception as e:
            pass

    def bar(self, interval: float = 2.0):
        """任务进度信息. 如果timeout非零, 则同步阻塞执行, 否则异步.
        NOTE: 如果结果获取不到或者不全, 可能是save清空导致,可 减小interval增加取数频率.

        Args:
            interval (float, optional): 进度刷新时间间隔, 不宜也不必过快. Defaults to 2.0.

        Raises:
            TimeoutError: 如果任务超过了认定的最大时间还未完则停止.
            实际还在执行, 只是Task不再获取数据及进度.
        """
        while True:
            try:
                status = self.status()['status']
                if status in ['Pending']:
                    time.sleep(interval)
                    continue
                else:
                    self.progress = Progress(desc=self.name,
                                             total=self.report()['size'],
                                             postfix=self.thread)
                    break
            except Exception as e:
                logger.error(
                    f'Failed to get status: {e},{self.report()}')

        if isinstance(self.timeout, float):
            while True:
                if self.timeout > 0 and (time.time() - self.stime > self.timeout):
                    msg = f'Timeout: {self.timeout}'
                    logger.warning(msg)
                    raise TimeoutError(msg)
                time.sleep(interval)
                if self.update():
                    break
        else:
            self.progress.clear()
            self.refresh(interval)
        self.progress.close()

    def refresh(self, interval: float = 2.0):
        """异步获取数据并刷新进度, 不会阻塞notebook。

        Args:
            interval (float, optional): 刷新时间间隔. Defaults to 2.0.
        """
        self.progress.display()
        if self.update():
            self.progress.display()
            return
        self.handles[self.tid] = asyncio.get_running_loop(
        ).call_later(interval, self.refresh, *(interval,))

    def plot(self, append: bool = False):
        """实时画图

        Args:
            append (bool, optional): 绘图方法, 首次画图(True)或增量数据画图(False).

        NOTE: 子图数量不宜太多(建议最大6*6), 单条曲线数据点亦不宜过多(建议不超过5000)

        >>> 如
        row = 4
        col = 4
        for i in range(100): # 步数
            time.sleep(0.1) # 防止刷新过快导致卡顿
            try:
                data = []
                for r in range(row):
                    rd = []
                    for c in range(col):
                        cell = {}
                        for j in range(2):
                            line = {}
                            line['xdata'] = np.arange(i, i+1)
                            line['ydata'] = np.random.random(1)
                            line['title'] = f'{r}_{c}'
                            line['xlabel'] = f'xx'
                            line['ylabel'] = f'yy'
                            line['titlecolor'] = 'red'
                            line['linecolor']=random.choice(['r', 'g', 'b', 'k', 'c', 'm', 'y', (31, 119, 180)])
                            cell[f'test{j}'] = line
                        rd.append(cell)
                    data.append(rd)
                if i == 0:
                    _vs.plot(data)
                else:
                    _vs.append(data)
            except Exception as e:
                print(e)
        """
        if self.last == 0:
            self.canvas.clear()

        if 'population' in str(self.meta['other']['signal']):
            signal = 'population'
        else:
            signal = str(self.meta['other']['signal']).split('.')[-1]
        raw = np.abs(np.asarray(self.data[signal][self.last:self.index]))

        if hasattr(self, 'app'):
            try:
                title = self.app.consts['couplers']
            except Exception as e:
                title = self.app.consts['qubits']
        axis = self.meta['axis']
        label = tuple(axis)

        if len(label) == 1:
            xlabel = label[0]
            ylabel = 'Any'
            xdata = axis[xlabel][xlabel][self.last:self.index]
            ydata = raw
        elif len(label) == 2:
            xlabel, ylabel = label
            xdata = axis[xlabel][xlabel]
            ydata = axis[ylabel][ylabel]
            zdata = raw

        if len(label) > 3:
            return
        row, col = raw.shape[-1]//4+1, 4

        time.sleep(0.1)  # 防止刷新过快导致卡顿
        try:
            data = []
            for r in range(row):
                rd = []
                for c in range(col):
                    cell = {}

                    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    # for j in range(1):
                    idx = r*col+c
                    line = {}
                    if len(label) == 1:
                        try:
                            line['xdata'] = xdata
                            line['ydata'] = ydata[..., idx].squeeze()
                        except Exception as e:
                            # line['ydata'] = ydata[..., 0]*0
                            continue

                    if len(label) == 2:
                        try:
                            if self.last == 0:
                                line['xdata'] = xdata
                                line['ydata'] = ydata
                            line['zdata'] = zdata[..., idx]
                            line['colormap'] = 'jet'  # magma
                        except Exception as e:
                            # line['zdata'] = np.array([0])
                            continue

                    try:
                        line['title'] = f'{self.name}_{self.app.record_id}_{title[idx]}'
                    except Exception as e:
                        line['title'] = f'{r}_{c}'
                    line['xlabel'] = xlabel
                    line['ylabel'] = ylabel
                    line['linecolor'] = 'r'
                    cell[f'test'] = line
                    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

                    rd.append(cell)
                data.append(rd)
            if not append:
                self.canvas.plot(data)
            else:
                self.canvas.append(data)
        except Exception as e:
            logger.error(f'Failed to update canvas: {e}')
