"""任务形式规则
详见submit函数
"""

from abc import ABC, abstractmethod

import numpy as np
from kernel.terminal.scan import App
from kernel.terminal.scan import Scan as _Scan
from qos_tools.experiment.scanner2 import Scanner as _Scanner
from waveforms.dicttree import flattenDictIter


class TaskMixin(ABC):
    """扩展兼容App
    """

    def __new__(cls, *args, **kwds):
        for base in cls.__mro__:
            if base.__name__ == 'TaskMixin':
                for k in dir(base):
                    if not k.startswith('__') and k not in base.__abstractmethods__:
                        setattr(cls, k, getattr(base, k))
        return super().__new__(cls)

    @abstractmethod
    def variables(self):
        """形如
        >>> {'x':[('x1', [1,2,3], 'au'), ('x2', [1,2,3], 'au')],
             'y':[('y1', [1,2,3], 'au'), ('y2', [1,2,3], 'au')],
             'z':[('z1', [1,2,3], 'au'), ('z2', [1,2,3], 'au')]
            }
        """
        return {}

    @abstractmethod
    def dependencies(self):
        """形如
        >>> [f'<gate.rfUnitary.{q}.params.frequency>=12345' for q in qubits]

        """
        return []

    @abstractmethod
    def circuits(self):
        pass

    def run(self, dry_run=False, quiet=False):
        try:
            self.toserver.run()
        except:
            import kernel
            from kernel.sched.sched import generate_task_id, get_system_info
            self.runtime.prog.task_arguments = (), {}
            self.runtime.prog.meta_info['arguments'] = {}
            self.runtime.id = generate_task_id()
            self.runtime.user = None
            self.runtime.system_info = {}  # get_system_info()
            kernel.submit(self, dry_run=dry_run)
            if not dry_run and not quiet:
                self.bar()

    def result(self, reshape=True):
        d = super(App, self).result(reshape)
        try:
            for k, v in self.toserver.result().items():
                dk = np.asarray(v)
                d[k] = dk.reshape([*self.shape, *dk[0].shape])
            return d
        except:
            return d

    def cancel(self):
        try:
            self.toserver.cancel()
        except:
            super(App, self).cancel()

    def bar(self):
        try:
            self.toserver.bar()
        except:
            super(App, self).bar()

    def save(self):
        from kernel.sched.sched import session
        from storage.models import Record
        with session() as db:
            record = db.get(Record, self.record_id)
            record.data = self.result(self.reshape_record)


class Scan(_Scan, TaskMixin):
    def __init__(self, name, *args, mixin=None, **kwds):
        super().__init__(name, *args, mixin=mixin, **kwds)

    def variables(self):
        loops = {}
        for k, v in self.loops.items():
            loops[k] = [(k, v, 'au')]
        return loops

    def circuits(self):
        self.assemble()
        for step in self.scan():
            for k, v in self.mapping.items():
                self.set(k, step.kwds[v])
            yield step

    def dependencies(self):
        deps = []
        for k, v in self.mapping.items():
            if isinstance(self[v], str):
                deps.append(f'<{k}>="{self[v]}"')
            elif isinstance(self[v], dict):
                for _k, _v in flattenDictIter(self[v]):
                    if isinstance(_v, str):
                        deps.append(f'<{k}.{_k}>="{_v}"')
                    else:
                        deps.append(f'<{k}.{_k}>={_v}')
            else:
                deps.append(f'<{k}>={self[v]}')
        return deps


class Scanner(_Scanner, TaskMixin):
    def __init__(self, name: str, qubits: list[int], scanner_name: str = '', **kw):
        super().__init__(name, qubits, scanner_name, **kw)

    def variables(self):
        loops = {}
        for k, v in self.sweep_setting.items():
            if isinstance(k, tuple):
                loops['temp'] = list(zip(k, v, ['au']*len(k)))
            else:
                loops[k] = [(k, v, 'au')]
        return loops

    def circuits(self):
        for step in self.scan():
            # self.update({v_dict['addr']: step.kwds[k]
            #              for k, v_dict in self.sweep_config.items()})
            yield step

    def dependencies(self):
        return super().dependencies()
