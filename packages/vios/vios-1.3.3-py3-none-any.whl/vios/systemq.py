# 与systemq交互的接口


from copy import deepcopy

from lib import stdlib
from lib.arch import baqisArchitecture
from lib.arch.baqis import assembly_code
from lib.arch.baqis_config import QuarkLocalConfig
from qlisp.kernel_utils import get_all_channels, sample_waveform
from waveforms import wave_eval
from waveforms.namespace import DictDriver
from waveforms.qlisp import get_arch, register_arch
from waveforms.scan_iter import StepStatus
from waveforms.waveform import Waveform, WaveVStack

try:
    from qlisp import Capture
except Exception as e:
    from qlisp import MeasurementTask as Capture

from qlisp import Signal
from qlisp import compile as _compile


class CompilerContext(QuarkLocalConfig):
    def __init__(self, data) -> None:
        super().__init__(data)
        self.reset(data)
        self.initial = {}
        self.bypass = {}
        self._keys = []

    def reset(self, snapshot):
        if isinstance(snapshot, dict):
            self._QuarkLocalConfig__driver = DictDriver(deepcopy(snapshot))
        else:
            self._QuarkLocalConfig__driver = snapshot

    def snapshot(self):
        return self._QuarkLocalConfig__driver

    def export(self):
        return self._QuarkLocalConfig__driver()


def _form_signal(sig):
    """signal类型
    """
    sig_tab = {
        'trace': Signal.trace,
        'iq': Signal.iq,
        'state': Signal.state,
        'count': Signal.count,
        'diag': Signal.diag,
        'population': Signal.population,
        'trace_avg': Signal.trace_avg,
        'iq_avg': Signal.iq_avg,
        'remote_trace_avg': Signal.remote_trace_avg,
        'remote_iq_avg': Signal.remote_iq_avg,
        'remote_state': Signal.remote_state,
        'remote_population': Signal.remote_population,
        'remote_count': Signal.remote_count,
    }
    if isinstance(sig, str):
        if sig == 'raw':
            sig = 'iq'
        try:
            return sig_tab[sig]
        except KeyError:
            pass
    elif isinstance(sig, Signal):
        return sig
    raise ValueError(f'unknow type of signal "{sig}".'
                     f" optional signal types: {list(sig_tab.keys())}")
