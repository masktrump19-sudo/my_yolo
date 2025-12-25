# 🔧 环境搭建详细指南

本文档提供了 my_yolo 项目的完整环境搭建步骤，包括 Conda 环境创建、依赖安装和常见问题解决。

## 📋 系统要求

### 硬件要求
- **CPU**: Intel i5 或更高（推荐 i7/i9）
- **内存**: 最少 8GB RAM（推荐 16GB+）
- **存储**: 至少 5GB 可用空间
- **GPU**: 可选，NVIDIA GPU with CUDA support（强烈推荐，可加速10-100倍）

### 软件要求
- **操作系统**: Windows 10/11, macOS, Ubuntu 18.04+
- **Python**: 3.8, 3.9, 3.10, 或 3.11
- **Conda**: Anaconda 或 Miniconda

---

## 🚀 快速开始（推荐流程）

### 步骤 1: 安装 Anaconda/Miniconda

如果尚未安装 Conda，请选择以下方式之一：

#### 选项 A: Anaconda（完整版，包含常用工具）
```bash
# Windows
# 访问 https://www.anaconda.com/download 下载安装器

# macOS/Linux
wget https://repo.anaconda.com/archive/Anaconda3-latest-Linux-x86_64.sh
bash Anaconda3-latest-Linux-x86_64.sh
```

#### 选项 B: Miniconda（轻量版，推荐）
```bash
# Windows
# 访问 https://docs.conda.io/en/latest/miniconda.html 下载安装器

# macOS/Linux
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

**验证安装**：
```bash
conda --version
# 应输出类似: conda 23.x.x
```

---

### 步骤 2: 创建虚拟环境 `my_yolo`

```bash
# 创建名为 my_yolo 的 Python 3.10 环境
conda create -n my_yolo python=3.10 -y

# 激活环境
conda activate my_yolo

# 验证 Python 版本
python --version
# 应输出: Python 3.10.x
```

> **💡 提示**: 使用 Python 3.10 是因为它与 PyTorch 和 YOLOv8 兼容性最好。

---

### 步骤 3: 安装项目依赖

#### 3.1 基础安装（CPU版本）

```bash
# 确保已激活 my_yolo 环境
conda activate my_yolo

# 进入项目目录
cd my_yolo

# 安装所有依赖
pip install -r requirements.txt
```

#### 3.2 GPU加速安装（推荐，如有NVIDIA GPU）

```bash
# 首先检查CUDA版本
nvidia-smi
# 查看 CUDA Version

# 根据CUDA版本安装对应的PyTorch
# CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# CUDA 12.1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# 然后安装其他依赖
pip install -r requirements.txt
```

**验证GPU可用性**：
```python
python -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'CUDA Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"
```

#### 3.3 开发模式安装（可编辑安装）

```bash
# 以开发模式安装项目
pip install -e .

# 这样可以直接使用命令行工具
yolo-detect --help
yolo-train --help
```

---

### 步骤 4: 初始化项目结构

```bash
# 运行初始化脚本，自动创建所有必需目录
python scripts/init_project.py
```

预期输出：
```
🚀 开始初始化项目目录结构...
✅ 创建目录: data/custom_dataset/images/train
✅ 创建目录: results/task1/images
...
✨ 项目目录结构初始化完成！
```

---

### 步骤 5: 验证安装

运行环境验证脚本（Task 1 的一部分）：

```bash
python src/task1_basic_detection.py --verify-only
```

这将检查：
- ✅ Python 版本
- ✅ PyTorch 安装
- ✅ YOLO 库
- ✅ OpenCV
- ✅ GPU 可用性（如果有）

---

## 📦 依赖包说明

### 核心依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| `ultralytics` | ≥8.0.0 | YOLOv8 官方实现 |
| `torch` | ≥2.0.0 | 深度学习框架 |
| `torchvision` | ≥0.15.0 | 计算机视觉工具 |
| `opencv-python` | ≥4.8.0 | 图像/视频处理 |
| `numpy` | ≥1.24.0 | 数值计算 |
| `pillow` | ≥10.0.0 | 图像处理 |

### 可视化依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| `matplotlib` | ≥3.7.0 | 绘图 |
| `seaborn` | ≥0.12.0 | 统计可视化 |
| `plotly` | ≥5.14.0 | 交互式图表 |
| `pandas` | ≥2.0.0 | 数据分析 |

### Web应用依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| `streamlit` | ≥1.28.0 | Web UI（Task 4） |
| `gradio` | ≥4.0.0 | ML Web UI（可选） |

### 工具依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| `pyyaml` | ≥6.0 | 配置文件解析 |
| `tqdm` | ≥4.65.0 | 进度条 |
| `python-dotenv` | ≥1.0.0 | 环境变量管理 |

---

## 🔧 常见问题解决

### 问题 1: `conda: command not found`

**原因**: Conda 未添加到环境变量

**解决方案**:
```bash
# macOS/Linux
export PATH="$HOME/anaconda3/bin:$PATH"
# 或
export PATH="$HOME/miniconda3/bin:$PATH"

# Windows: 重新运行 Anaconda 安装器，勾选 "Add to PATH"
```

---

### 问题 2: PyTorch GPU 版本不可用

**解决方案**:
```bash
# 卸载现有 PyTorch
pip uninstall torch torchvision

# 重新安装 GPU 版本
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

---

### 问题 3: `ImportError: DLL load failed` (Windows)

**原因**: 缺少 Visual C++ Runtime

**解决方案**:
下载并安装 [Microsoft Visual C++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist)

---

### 问题 4: OpenCV 报错 `cv2.imshow()` 不工作

**解决方案**:
```bash
# 卸载并重新安装 opencv-python
pip uninstall opencv-python opencv-python-headless
pip install opencv-python
```

---

### 问题 5: 安装速度慢

**解决方案**: 使用国内镜像源

```bash
# 临时使用清华镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或永久配置
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

**Conda 镜像**:
```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --set show_channel_urls yes
```

---

## 🎯 不同操作系统的特殊说明

### Windows

1. **使用 Anaconda Prompt**（而非 CMD）
2. 确保安装了 Visual Studio Build Tools
3. 摄像头权限：设置 → 隐私 → 摄像头 → 允许桌面应用访问

### macOS

1. **摄像头权限**: 系统偏好设置 → 安全性与隐私 → 摄像头 → 勾选终端
2. 如果使用 Apple Silicon (M1/M2)，PyTorch 会自动使用 MPS 加速

### Linux (Ubuntu)

```bash
# 安装系统依赖
sudo apt-get update
sudo apt-get install -y python3-dev python3-pip libgl1-mesa-glx libglib2.0-0
```

---

## ✅ 验证清单

完成环境搭建后，请检查以下各项：

- [ ] Conda 环境 `my_yolo` 已创建并激活
- [ ] Python 版本为 3.8-3.11
- [ ] 所有依赖包安装成功（`pip list` 查看）
- [ ] PyTorch 可以正常导入
- [ ] GPU 可用（如有 NVIDIA GPU）
- [ ] 项目目录结构已初始化
- [ ] 可以运行 `python src/task1_basic_detection.py --help`

---

## 📚 下一步

环境搭建完成后，可以开始：

1. [任务1：基础检测](../README.md#任务1基础检测预训练模型) - 测试预训练模型
2. [任务2：自定义训练](../README.md#任务2自定义训练) - 训练自己的模型
3. [任务3：性能测试](../README.md#任务3性能测试) - 对比不同模型
4. [任务4：Web应用](../README.md#任务4应用开发) - 开发交互式应用

---

## 🆘 获取帮助

如遇问题，请：

1. 查看本文档的"常见问题"部分
2. 查阅 [Ultralytics YOLOv8 文档](https://docs.ultralytics.com/)
3. 查看项目 `logs/` 目录下的日志文件
4. 提交 Issue 到项目 GitHub

---

**祝你实验顺利！** 🎉
