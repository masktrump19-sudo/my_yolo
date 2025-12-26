<div align="center">

# 🎯 my_yolo

### 基于 YOLOv8 的端到端目标检测实验项目

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-00DFA2?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDJMMiA3TDEyIDEyTDIyIDdMMTIgMloiIGZpbGw9IndoaXRlIi8+CjxwYXRoIGQ9Ik0yIDEyTDEyIDE3TDIyIDEyIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiLz4KPC9zdmc+)](https://github.com/ultralytics/ultralytics)
[![License](https://img.shields.io/badge/License-MIT-FFC107?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)

---

### 👨‍💻 作者信息

<table>
  <tr>
    <td align="center">
      <img src="https://img.shields.io/badge/👤_作者-黄永庆-blue?style=for-the-badge" alt="Author"/>
    </td>
    <td align="center">
      <img src="https://img.shields.io/badge/🎓_学校-中山大学-green?style=for-the-badge" alt="University"/>
    </td>
  </tr>
</table>

</div>

---

## 📋 项目简介

**my_yolo** 是一个工程化标准的目标检测实验项目，旨在指导用户从零构建基于 YOLOv8 的计算机视觉应用。本项目涵盖了环境搭建、模型推理、迁移学习训练、性能基准测试以及交互式 Web 应用开发的全流程。

### ✨ 核心特性

- 🔧 **开箱即用** - 一键环境配置，快速上手
- 🎨 **多模态检测** - 支持图片、视频、实时摄像头
- 🚀 **迁移学习** - 自定义数据集训练
- 📊 **性能对比** - 多模型基准测试
- 🌐 **Web 应用** - Streamlit 交互式界面

---

## 📂 项目结构

```
my_yolo/
├── 📁 data/                       # 数据集根目录
│   ├── 🖼️  image/                  # Task 1 测试图片
│   ├── 🎥 video/                  # Task 1 测试视频
│   └── 📦 custom_dataset/         # Task 2 自定义数据集 (需标注)
├── 📁 dataset/
│   └── 🗂️  coco128/                # Task 3 测试数据集
│         ├── images/             
│         └── labels/
├── 📚 docs/                       # 项目文档
│   ├── 📖 environment_setup.md    # 环境安装指南
│   └── 📝 data_annotation_guide.md# 数据标注指南
├── 🤖 models/                     # 模型权重文件
├── 📊 results/                    # 实验结果输出
│   ├── detect/                   # Task 1 推理结果
│   ├── task2/                    # Task 2 训练结果
│   └── task3/                    # Task 3 性能报告
├── 🔧 scripts/                    # 辅助脚本
│   └── init_project.py           # 初始化脚本
├── 💻 src/                        # 源代码
│   ├── task1.py                  # 阶段1：基础检测
│   ├── task2.py                  # 阶段2：自定义训练
│   ├── task3.py                  # 阶段3：性能测试
│   └── task4.py                  # 阶段4：Web 应用
├── ⚙️  config.yaml                 # 项目配置 (可选)
├── 📋 requirements.txt            # 依赖包列表
└── 📄 README.md                   # 项目主文档
```

---

## 🚀 快速开始

### 1️⃣ 环境搭建

<details>
<summary><b>💡 点击展开详细步骤</b></summary>

强烈推荐使用 Conda 管理环境。详细指南请参考 [docs/environment_setup.md](docs/environment_setup.md)。

```bash
# 创建环境
conda create -n my_yolo python=3.10 -y
conda activate my_yolo

# 安装依赖
pip install -r requirements.txt
```

</details>

---

### 2️⃣ 运行任务

#### 📷 阶段 1：环境搭建与模型体验

> **功能**：自动下载模型，支持图片、视频及摄像头实时检测。

```bash
# 🖼️ 图片批量检测
python src/task1.py --mode image --source data/image

# 🎬 视频检测 (自动截取30秒)
python src/task1.py --mode video --source data/video/test.mp4

# 📹 摄像头实时检测
python src/task1.py --mode camera
```

---

#### 🎯 阶段 2：自定义对象检测

> **功能**：加载预训练权重进行迁移学习，自动绘制 Loss 曲线。

⚠️ **前置条件**：请阅读 [docs/data_annotation_guide.md](docs/data_annotation_guide.md) 准备数据集。

```bash
# 🏋️ 训练模型
python src/task2.py --mode train --data data/custom_dataset/dataset.yaml --epochs 50

# 🔍 验证模型
python src/task2.py --mode predict --weights results/task2/train/weights/best.pt --source data/custom_dataset/images/test
```

---

#### 📊 阶段 3：性能基准测试

> **功能**：在同一数据集上对比 YOLOv8n/s/m 的性能（FPS, mAP, Params），生成对比报告。

```bash
# ⚡ 执行基准测试
python src/task3.py --data coco128.yaml
```

**输出示例**：会自动生成 `results/task3/benchmark_report.md`。

<table>
  <thead>
    <tr>
      <th>🤖 Model</th>
      <th>💾 Size (MB)</th>
      <th>🔢 Params (M)</th>
      <th>🎯 mAP 50-95</th>
      <th>⚡ FPS</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>yolov8n.pt</td>
      <td>6.2</td>
      <td>3.2</td>
      <td>0.642</td>
      <td>145.2</td>
    </tr>
    <tr>
      <td>yolov8s.pt</td>
      <td>22.5</td>
      <td>11.2</td>
      <td>0.715</td>
      <td>85.6</td>
    </tr>
  </tbody>
</table>

---

#### 🌐 阶段 4：简单应用开发

> **功能**：启动 Streamlit Web 应用，提供交互式检测体验。

```bash
# 🚀 启动 Web App
streamlit run src/task4.py
```

浏览器将自动打开 `http://localhost:8501`

---

## 📊 实验结果展示

### 🖼️ Task 1: 基础检测
<div align="center">

| 图片检测 | 视频检测 |
|:---:|:---:|
| ![Task 1 Image](https://via.placeholder.com/400x300?text=Task1+Result) | ![Task 1 Video](https://via.placeholder.com/400x300?text=Task1+Demo) |

</div>

### 📈 Task 2: 训练曲线
<div align="center">

![Loss Curve](https://via.placeholder.com/800x200?text=Loss+Curve+Placeholder)

</div>

### 💻 Task 4: Web 应用
<div align="center">

![Web App](https://via.placeholder.com/800x400?text=Streamlit+App+Interface)

</div>

---

## 🛠️ 技术栈

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)

</div>

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！

1. 🍴 Fork 本项目
2. 🌿 创建新的 Feature 分支 (`git checkout -b feature/AmazingFeature`)
3. 💾 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 📤 推送到分支 (`git push origin feature/AmazingFeature`)
5. 🎉 提交 Pull Request

---

## 📝 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

---

<div align="center">

### ⭐ 如果这个项目对你有帮助，请给一个 Star！

**Made with ❤️ by 黄永庆 @ 中山大学**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:masktrump19@gmail.com)

</div>

