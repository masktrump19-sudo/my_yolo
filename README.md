# 🎯 my_yolo: 基于 YOLOv8 的端到端目标检测实验项目

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-green)](https://github.com/ultralytics/ultralytics)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 📋 项目简介

**my_yolo** 是一个工程化标准的目标检测实验项目，旨在指导用户从零构建基于 YOLOv8 的计算机视觉应用。本项目涵盖了环境搭建、模型推理、迁移学习训练、性能基准测试以及交互式 Web 应用开发的全流程。

---

## 📂 项目结构

```
my_yolo/
├── data/                       # 数据集根目录
│   ├── image/                  # Task 1 测试图片
│   ├── video/                  # Task 1 测试视频
│   └── custom_dataset/         # Task 2 自定义数据集 (需标注)
|—— dataset/
|   └── coco128/                  # Task 3 测试图片
|         ├── images/             
│         └── labels/
│   
├── docs/                       # 项目文档
│   ├── environment_setup.md    # 环境安装指南
│   └── data_annotation_guide.md# 数据标注指南
├── models/                     # 模型权重文件
├── results/                    # 实验结果输出
│   ├── detect/                 # Task 1 推理结果
│   ├── task2/                  # Task 2 训练结果
│   └── task3/                  # Task 3 性能报告
├── scripts/                    # 辅助脚本
│   └── init_project.py         # 初始化脚本
├── src/                        # 源代码
│   ├── task1.py                # 阶段1：基础检测
│   ├── task2.py                # 阶段2：自定义训练
│   ├── task3.py                # 阶段3：性能测试
│   └── task4.py                # 阶段4：Web 应用
├── config.yaml                 # 项目配置 (可选)
├── requirements.txt            # 依赖包列表
└── README.md                   # 项目主文档
```

---

## 🚀 快速开始

### 1. 环境搭建

强烈推荐使用 Conda 管理环境。详细指南请参考 [docs/environment_setup.md](docs/environment_setup.md)。

```bash
# 创建环境
conda create -n my_yolo python=3.10 -y
conda activate my_yolo

# 安装依赖
pip install -r requirements.txt
```

### 2. 运行任务

#### ✅ 阶段 1：环境搭建与模型体验

功能：自动下载模型，支持图片、视频及摄像头实时检测。

```bash
# 图片批量检测
python src/task1.py --mode image --source data/image

# 视频检测 (自动截取30秒)
python src/task1.py --mode video --source data/video/test.mp4

# 摄像头实时检测
python src/task1.py --mode camera
```

#### ✅ 阶段 2：自定义对象检测

功能：加载预训练权重进行迁移学习，自动绘制 Loss 曲线。

**前置条件**：请阅读 [docs/data_annotation_guide.md](docs/data_annotation_guide.md) 准备数据集。

```bash
# 训练模型
python src/task2.py --mode train --data data/custom_dataset/dataset.yaml --epochs 50

# 验证模型
python src/task2.py --mode predict --weights results/task2/train/weights/best.pt --source data/custom_dataset/images/test
```

#### ✅ 阶段 3：性能基准测试

功能：在同一数据集上对比 YOLOv8n/s/m 的性能（FPS, mAP, Params），生成对比报告。

```bash
# 执行基准测试
python src/task3.py --data coco128.yaml
```

**输出示例**：会自动生成 `results/task3/benchmark_report.md`。

| Model      | Size (MB) | Params (M) | mAP 50-95 | FPS   |
|:-----------|:----------|:-----------|:----------|:------|
| yolov8n.pt | 6.2       | 3.2        | 0.642     | 145.2 |
| yolov8s.pt | 22.5      | 11.2       | 0.715     | 85.6  |

#### ✅ 阶段 4：简单应用开发

功能：启动 Streamlit Web 应用，提供交互式检测体验。

```bash
# 启动 Web App
streamlit run src/task4.py
```

---

## 📊 实验结果展示 (Result Placeholders)

在此处展示你的实验成果截图：

### Task 1: 基础检测
| 图片检测 | 视频检测 |
|:---:|:---:|
| ![Task 1 Image](https://via.placeholder.com/400x300?text=Task1+Result) | ![Task 1 Video](https://via.placeholder.com/400x300?text=Task1+Demo) |

### Task 2: 训练曲线
![Loss Curve](https://via.placeholder.com/800x200?text=Loss+Curve+Placeholder)

### Task 4: Web 应用
![Web App](https://via.placeholder.com/800x400?text=Streamlit+App+Interface)

---

## 🤝 贡献指南 (Contributing)

1. Clone 本项目
2. 创建新的 Feature 分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request