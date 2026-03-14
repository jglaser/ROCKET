
import os
import sys

# --- NVIDIA PyTorch NVRTC Path Fix ---
try:
    import site
    try:
        site_pkgs = site.getsitepackages()
    except AttributeError:
        import sysconfig
        site_pkgs = [sysconfig.get_path("purelib")]
        
    added_paths = []
    for sp in site_pkgs:
        nvidia_base = os.path.join(sp, "nvidia")
        if os.path.exists(nvidia_base):
            # Support both new unified cu13/cu12 folders and legacy individual packages
            for lib in ["cu13", "cu12", "cuda_nvrtc", "nvjitlink", "cublas", "cudnn"]:
                lib_path = os.path.join(nvidia_base, lib, "lib")
                if os.path.exists(lib_path) and lib_path not in added_paths:
                    added_paths.append(lib_path)
                
    if added_paths:
        current_ld = os.environ.get("LD_LIBRARY_PATH", "")
        missing_paths = [p for p in added_paths if p not in current_ld.split(":")]
        
        if missing_paths:
            new_ld = ":".join(missing_paths) + (":" + current_ld if current_ld else "")
            os.environ["LD_LIBRARY_PATH"] = new_ld
            os.execv(sys.executable, [sys.executable] + sys.argv)
except Exception:
    pass
# ---------------------------------------

# Top Level API
# Submodules
from rocket import base, coordinates, cryo, refinement_utils, utils, xtal
from rocket.base import MSABiasAFv1, MSABiasAFv2, MSABiasAFv3, TemplateBiasAF
from rocket.helper import make_processed_dict_from_template
from rocket.msa_cluster import run_msa_cluster
from rocket.msa_score import run_msa_score
from rocket.mse import MSEloss, MSElossBB
from rocket.xtal.targets import LLGloss

__all__ = [
    # List submodules you want to expose
    "base",
    "coordinates",
    "xtal",
    "cryo",
    "utils",
    "refinement_utils",
    # List specific classes/functions you want to expose directly
    "MSABiasAFv1",
    "MSABiasAFv2",
    "MSABiasAFv3",
    "TemplateBiasAF",
    "make_processed_dict_from_template",
    "LLGloss",
    "MSEloss",
    "MSElossBB",
    "run_msa_cluster",
    "run_msa_score",
]