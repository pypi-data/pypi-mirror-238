"""Zurich Instruments LabOne SeqC Compiler."""
from typing import (
    List,
    Union,
    Any,
    Dict,
    Optional,
    Tuple,
)

def compile_seqc(
    code: str,
    devtype: str,
    options: Union[str, List[str]],
    index: int,
    samplerate: Optional[float] = None,
    sequencer: Optional[str] = None,
    wavepath: Optional[str] = None,
    waveforms: Optional[str] = None,
    filename: Optional[str] = None,
) -> Tuple[bytes, Dict[str, Any]]:
    """Compile the sequencer code.

    This function is a purely static function that does not require an
    active connection to a Data Server.

    .. versionadded:: 22.08

    Args:
        code: SeqC input
        devtype: target device type, e.g., HDAWG8, SHFQC
        options: list of device options, or string of
            options separated by newlines as returned by node
            /dev.../features/options.
        index: index of the AWG core
        samplerate: target sample rate of the sequencer
            Mandatory and only respected for HDAWG. Should match the
            value set on the device:
            `/dev.../system/clocks/sampleclock/freq`.
        sequencer: one of 'qa', 'sg', or 'auto'.
            Mandatory for SHFQC.
        wavepath: path to directory with waveforms. Defaults to
            path used by LabOne UI or AWG Module.
        waveforms: list of CSV waveform files separated by ';'.
            Defaults to an empty list. Set to `None` to include
            all CSV files in `wavepath`.
        filename: name of embedded ELF filename.

    Returns:
        Tuple (elf, extra) of binary ELF data for sequencer and extra
        dictionary with compiler output."""
