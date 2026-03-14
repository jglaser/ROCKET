# --- NVIDIA PyTorch NVRTC Path Fix ---
# PyTorch pip packages do not automatically expose their CUDA libraries to the linker.
# This iterates sys.path (catching lib64 and venvs) and seamlessly re-executes.
import os
import sys

try:
    added_paths = []
    # sys.path natively understands lib vs lib64 in the active environment
    for p in sys.path:
        nvidia_base = os.path.join(p, "nvidia")
        if os.path.isdir(nvidia_base):
            for lib in ["cuda_nvrtc", "nvjitlink", "cublas", "cudnn"]:
                lib_path = os.path.join(nvidia_base, lib, "lib")
                if os.path.isdir(lib_path) and lib_path not in added_paths:
                    added_paths.append(lib_path)
                    
    if added_paths:
        current_ld = os.environ.get("LD_LIBRARY_PATH", "")
        missing_paths = [p for p in added_paths if p not in current_ld]
        
        if missing_paths:
            new_ld = ":".join(missing_paths) + (":" + current_ld if current_ld else "")
            os.environ["LD_LIBRARY_PATH"] = new_ld
            # Restart the process with the new environment variables intact
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
