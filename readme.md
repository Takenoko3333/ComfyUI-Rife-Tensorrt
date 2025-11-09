<div align="center">

# ComfyUI Rife TensorRT ⚡

[![python](https://img.shields.io/badge/python-3.11.6-green)](https://www.python.org/downloads/release/python-3116/)
[![cuda](https://img.shields.io/badge/cuda-12.8-green)](https://developer.nvidia.com/cuda-downloads)
[![trt](https://img.shields.io/badge/TRT-10.12.0.36-green)](https://developer.nvidia.com/tensorrt)
[![by-nc-sa/4.0](https://img.shields.io/badge/license-CC--BY--NC--SA--4.0-lightgrey)](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en)

![node](https://github.com/user-attachments/assets/5fd6d529-300c-42a5-b9cf-46e031f0bcb5)


</div>

This project provides a [TensorRT](https://github.com/NVIDIA/TensorRT) implementation of [RIFE](https://github.com/hzwer/ECCV2022-RIFE) for ultra fast frame interpolation inside ComfyUI

This project is licensed under [CC BY-NC-SA](https://creativecommons.org/licenses/by-nc-sa/4.0/), everyone is FREE to access, use, modify and redistribute with the same license.

If you like the project, please give me a star! ⭐

---

## ⭐ About this Repository

This is a modified version forked from ComfyUI Rife TensorRT, primarily optimized for easy implementation on the RTX 4000 series.<br>
Additionally, it describes the installation procedures for both the venv version and the portable version.<br>
This repository installs TensorRT 10.12.0.36.

## 🔔 Additional information

The optimal TensorRT version varies depending on Python, PyTorch, CUDA, and GPU generation.<br>
This repository is configured to install a TensorRT version that is generally suitable for the RTX 4000 series, but you may need to change the version depending on your environment.<br>
This is just one example, but in relatively older environments, "tensorrt 10.4.0" may be an option, while in relatively newer environments, "tensorrt 10.13.3" may be an option.

## ⏱️ Performance

_Note: The following results were benchmarked on FP16 engines inside ComfyUI, using 2000 frames consisting of 2 alternating similar frames, averaged 2-3 times_

| Device | Rife Engine | Resolution| Multiplier | FPS |
| :----: | :-: | :-: | :-: | :-: |
|  H100  | rife49_ensemble_True_scale_1_sim | 512 x 512  | 2 | 45 |
|  H100  | rife49_ensemble_True_scale_1_sim | 512 x 512  | 4 | 57 |
|  H100  | rife49_ensemble_True_scale_1_sim | 1280 x 1280  | 2 | 21 |

## 🚀 Installation for venv Environment
1. Navigate to the `/ComfyUI/custom_nodes` directory

```bash
git clone https://github.com/Takenoko3333/ComfyUI-Rife-Tensorrt.git
```
2. venv activate first, Move the directory and install

```bash
<your path>\ComfyUI\venv\Scripts\activate
cd .\ComfyUI-Rife-Tensorrt
python -m pip install -r requirements.txt
```
- Some environments (especially portable) may fail automatic install.<br>
  In that case, follow the manual installation commands below.<br>
  If no errors occur, skip it.
```bash
python -m pip install -i https://pypi.org/simple --extra-index-url https://pypi.nvidia.com tensorrt-cu12==10.12.0.36 tensorrt-cu12-bindings==10.12.0.36 tensorrt-cu12-libs==10.12.0.36
python -m pip install cuda-python==12.8.0
```
3. Building Tensorrt Engine<br>
The following command will automatically download onnx from huggingface, build the engine, and save the model to a directory.<br>
Processes 3 files. It will take a few minutes to complete.
```bash
python -u export_trt.py
```
> **Note:** Replace `<your path>` with your actual folder path (e.g., `D:\ai`).

## 💼 Installation for Portable Environment
1. Navigate to the `/ComfyUI/custom_nodes` directory

```bash
git clone https://github.com/Takenoko3333/ComfyUI-Rife-Tensorrt.git
```
2. Move the directory and install
```bash
cd .\ComfyUI-Rife-Tensorrt
<your path>\ComfyUI_windows_portable\python_embeded\python.exe -m pip install -r requirements.txt
```
- Some environments (especially portable) may fail automatic install.<br>
  In that case, follow the manual installation commands below.<br>
  If no errors occur, skip it.
```bash
<your path>\ComfyUI_windows_portable\python_embeded\python.exe -m pip install -i https://pypi.org/simple --extra-index-url https://pypi.nvidia.com tensorrt-cu12==10.12.0.36 tensorrt-cu12-bindings==10.12.0.36 tensorrt-cu12-libs==10.12.0.36
<your path>\ComfyUI_windows_portable\python_embeded\python.exe -m pip install cuda-python==12.8.0
```
3. Building Tensorrt Engine<br>
The following command will automatically download onnx from huggingface, build the engine, and save the model to a directory.<br>
Processes 3 files. It will take a few minutes to complete.
```bash
<your path>\ComfyUI_windows_portable\python_embeded\python.exe -u export_trt.py
```
> **Note:** Replace `<your path>` with your actual folder path (e.g., `D:\ai`).

## ☀️ Usage

- Insert node by `Right Click -> tensorrt -> Rife Tensorrt`
- Image resolutions between `256x256` and `3840x3840` will work with the tensorrt engines 

## 🤖 Environment tested

- Ubuntu 22.04 LTS
- Windows 10, Pytorch 2.7.1+cu128(Cuda 12.8), Tensorrt 10.12.0.36, Python 3.11.6, RTX 4080SUPER GPU
- Windows 10, Pytorch 2.7.1+cu128(Cuda 12.8), Tensorrt 10.12.0.36, Python 3.12.9, RTX 4080SUPER GPU
- Windows 10, Pytorch 2.8.0+cu128(Cuda 12.8), Tensorrt 10.12.0.36, Python 3.12.10, RTX 4080SUPER GPU
- Windows 11, Pytorch 2.7.1+cu128(Cuda 12.8), Tensorrt 10.12.0.36, Python 3.12.9, RTX 4080SUPER GPU

## 📅 Update
### 2025-11-10
- Update README
### 2025-11-08
- Fixed the folder path to enable importing in both venv environments and portable environments
### 2025-10-26
- Fork the repository
- primarily optimized for easy implementation on the RTX 4000 series
- Added Installation Guide 
- Building Tensorrt Engine : Download onnx from huggingface and build engine, save models dir

## 👏 Credits

- https://github.com/styler00dollar/VSGAN-tensorrt-docker
- https://github.com/Fannovel16/ComfyUI-Frame-Interpolation
- https://github.com/hzwer/ECCV2022-RIFE

## License

[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
