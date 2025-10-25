import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import time
import urllib.request
import urllib.error

import torch
import tensorrt
from trt_utilities import Engine
import folder_paths

print("TensorRT version:", tensorrt.__version__)

# -----------------------------------------------------------------------------
# Paths (ComfyUI conventions)
# -----------------------------------------------------------------------------
# Target directories inside ComfyUI/models
engine_dir = os.path.join(folder_paths.models_dir, "tensorrt", "rife")
onnx_dir   = os.path.join(folder_paths.models_dir, "onnx")
os.makedirs(engine_dir, exist_ok=True)
os.makedirs(onnx_dir, exist_ok=True)

# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------

def _download_file(url: str, dst_path: str, retries: int = 3, timeout: int = 60) -> None:
    """Download a file with basic retries and a reasonable User-Agent.
    Overwrites if the file already exists and the size differs or is 0 bytes.
    """
    # If a non-empty file already exists, skip downloading
    if os.path.exists(dst_path) and os.path.getsize(dst_path) > 0:
        print(f"[SKIP] Exists: {dst_path}")
        return

    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            print(f"[DL] {url} -> {dst_path} (try {attempt}/{retries})")
            with urllib.request.urlopen(req, timeout=timeout) as resp, open(dst_path, "wb") as out:
                chunk = resp.read(8192)
                total = 0
                while chunk:
                    out.write(chunk)
                    total += len(chunk)
                    chunk = resp.read(8192)
            if os.path.getsize(dst_path) > 0:
                print(f"[OK] {dst_path} ({os.path.getsize(dst_path)} bytes)")
                return
            else:
                last_err = RuntimeError("Downloaded file has zero size")
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, RuntimeError) as e:
            last_err = e
            print(f"[WARN] Download failed: {e}")
            time.sleep(1.5)
    raise last_err if last_err else RuntimeError("Unknown download error")


def export_trt(trt_path: str, onnx_path: str, use_fp16: bool = True):
    engine = Engine(trt_path)
    torch.cuda.empty_cache()

    s = time.time()
    ret = engine.build(
        onnx_path,
        use_fp16,
        enable_preview=True,
        input_profile=[
            {
                # any sizes from 256x256 to 3840x3840, batch size 1
                "img0": [(1, 3, 256, 256), (1, 3, 512, 512), (1, 3, 3840, 3840)],
                "img1": [(1, 3, 256, 256), (1, 3, 512, 512), (1, 3, 3840, 3840)],
            },
        ],
    )
    e = time.time()
    print(f"Time taken to build: {e - s:.2f} seconds")
    print(f"TensorRT engine saved at: {trt_path}")
    return ret


def run_all_sequential(models, use_fp16: bool = True):
    for trt_path, onnx_path in models:
        print("\n==== Building ====")
        print("ONNX:", onnx_path)
        print("ENGINE:", trt_path)
        if not os.path.exists(onnx_path):
            print(f"[SKIP] ONNX not found: {onnx_path}")
            continue
        try:
            export_trt(trt_path=trt_path, onnx_path=onnx_path, use_fp16=use_fp16)
        except Exception as ex:
            print(f"[ERROR] Failed to build {trt_path}: {ex}")


# -----------------------------------------------------------------------------
# Download all required ONNX files first
# -----------------------------------------------------------------------------
urls = {
    "rife49_ensemble_True_scale_1_sim.onnx": "https://huggingface.co/yuvraj108c/rife-onnx/resolve/main/rife49_ensemble_True_scale_1_sim.onnx",
    "rife48_ensemble_True_scale_1_sim.onnx": "https://huggingface.co/yuvraj108c/rife-onnx/resolve/main/rife48_ensemble_True_scale_1_sim.onnx",
    "rife47_ensemble_True_scale_1_sim.onnx": "https://huggingface.co/yuvraj108c/rife-onnx/resolve/main/rife47_ensemble_True_scale_1_sim.onnx",
}

all_ok = True
local_paths = {}
for fname, url in urls.items():
    dst = os.path.join(onnx_dir, fname)
    try:
        _download_file(url, dst)
        local_paths[fname] = dst
    except Exception as e:
        all_ok = False
        print(f"[ERROR] Failed to download {fname}: {e}")

# -----------------------------------------------------------------------------
# Build engines only if ALL downloads completed successfully
# -----------------------------------------------------------------------------
if all_ok:
    models = [
        (os.path.join(engine_dir, "rife49_ensemble_True_scale_1_sim.engine"), local_paths["rife49_ensemble_True_scale_1_sim.onnx"]),
        (os.path.join(engine_dir, "rife48_ensemble_True_scale_1_sim.engine"), local_paths["rife48_ensemble_True_scale_1_sim.onnx"]),
        (os.path.join(engine_dir, "rife47_ensemble_True_scale_1_sim.engine"), local_paths["rife47_ensemble_True_scale_1_sim.onnx"]),
    ]
    run_all_sequential(models, use_fp16=True)
else:
    print("[ABORT] Not all ONNX files were downloaded. Engine build is skipped.")
