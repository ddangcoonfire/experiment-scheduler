import os
import textwrap

pynvml = None
ALLOW_LEGACY_PYNVML = os.getenv("ALLOW_LEGACY_PYNVML", "")
ALLOW_LEGACY_PYNVML = ALLOW_LEGACY_PYNVML.lower() not in ('false', '0', '')

try:
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
        We require nvidia-ml-py>=11.450.129; see GH-107 for more details.
        Your pynvml installation: """ + repr(pynvml))) from e

__all__ = ['pynvml']