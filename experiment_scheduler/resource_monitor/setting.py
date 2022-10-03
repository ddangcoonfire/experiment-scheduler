"""Imports pynvml to check gpu and check version of it"""

import os
import textwrap

pynvml = None
ALLOW_LEGACY_PYNVML = os.getenv("ALLOW_LEGACY_PYNVML", "")
ALLOW_LEGACY_PYNVML = ALLOW_LEGACY_PYNVML.lower() not in ('false', '0', '')

try:
    """Version of pynvml should be newer than 11.450.51 to avoid conflicts with other packages"""
    import pynvml
    if not (
        hasattr(pynvml, 'NVML_BRAND_NVIDIA_RTX') or
        hasattr(pynvml, 'nvmlDeviceGetComputeRunningProcesses_v2')
    ):
        raise RuntimeError("pynvml library is outdated.")
except (ImportError, SyntaxError, RuntimeError) as e:
    raise ImportError(textwrap.dedent(
        """\
        pynvml is missing or an outdated version is installed.
        Your pynvml installation: """ + repr(pynvml))) from e

__all__ = ['pynvml']