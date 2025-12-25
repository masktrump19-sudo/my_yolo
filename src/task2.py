# -*- coding: utf-8 -*-
"""
Task 2: 自定义对象检测 (Custom Object Detection)

功能描述:
    1. 加载预训练权重进行迁移学习 (Transfer Learning)
    2. 支持自定义数据集训练
    3. 自动绘制并保存 Loss 曲线与性能指标图表
    4. 加载最佳权重进行新图片验证

使用方法:
    # 模式1: 训练模型
    python task2.py --mode train --data data/custom_dataset/dataset.yaml --epochs 50

    # 模式2: 使用训练好的模型进行预测
    python task2.py --mode predict --source data/test_images --weights results/task2/train/weights/best.pt

作者: my_yolo Team
日期: 2023-12-22
"""

import os
import sys
import argparse
import logging
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Optional

try:
    from ultralytics import YOLO
except ImportError:
    print("❌ Error: 'ultralytics' not found. Please install requirements.")
    sys.exit(1)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class YOLOTrainer:
    """YOLOv8 自定义训练管理器"""

    def __init__(self, model_name: str = 'yolov8n.pt', results_dir: str = 'results/task2'):
        self.model_name = model_name
        self.results_dir = Path(results_dir)
        self.train_dir = self.results_dir / 'train'
        self.predict_dir = self.results_dir / 'predict'
        
        # 确保目录存在
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def train(self, data_yaml: str, epochs: int = 50, batch_size: int = 16, imgsz: int = 640):
        """
        执行模型训练
        
        Args:
            data_yaml (str): 数据集配置文件路径
            epochs (int): 训练轮数
            batch_size (int): 批次大小
            imgsz (int): 输入图片尺寸
        """
        if not os.path.exists(data_yaml):
            logger.error(f"❌ Dataset config not found: {data_yaml}")
            logger.info("👉 Please refer to docs/data_annotation_guide.md to prepare your dataset.")
            return

        logger.info(f"🚀 Starting training with model: {self.model_name}")
        logger.info(f"📂 Data config: {data_yaml}")
        
        try:
            # 加载预训练模型
            model = YOLO(self.model_name)
            
            # 开始训练
            # project: 保存的根目录
            # name: 本次训练的子目录名
            results = model.train(
                data=data_yaml,
                epochs=epochs,
                batch=batch_size,
                imgsz=imgsz,
                project=str(self.results_dir),
                name='train',
                exist_ok=True,  # 允许覆盖，方便调试
                pretrained=True, # 明确开启迁移学习
                plots=True       # 自动生成图表
            )
            
            logger.info(f"🎉 Training complete!")
            logger.info(f"💾 Best weights saved to: {self.train_dir / 'weights' / 'best.pt'}")
            
            # 手动绘制自定义分析图表（增强分析）
            self.plot_training_metrics()
            
        except Exception as e:
            logger.error(f"❌ Training failed: {e}")
            raise e

    def plot_training_metrics(self):
        """读取训练日志并绘制 Loss 曲线"""
        csv_path = self.train_dir / 'results.csv'
        if not csv_path.exists():
            logger.warning("⚠️ No results.csv found, skipping custom plotting.")
            return

        try:
            # 读取数据
            df = pd.read_csv(csv_path)
            # 清理列名空格
            df.columns = [c.strip() for c in df.columns]
            
            plt.figure(figsize=(12, 5))
            
            # 绘制 Box Loss
            plt.subplot(1, 2, 1)
            plt.plot(df['epoch'], df['train/box_loss'], label='Train Box Loss')
            plt.plot(df['epoch'], df['val/box_loss'], label='Val Box Loss')
            plt.title('Box Loss Curve')
            plt.xlabel('Epochs')
            plt.ylabel('Loss')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # 绘制 mAP50
            plt.subplot(1, 2, 2)
            plt.plot(df['epoch'], df['metrics/mAP50(B)'], label='mAP@50', color='orange')
            plt.title('mAP@50 metric')
            plt.xlabel('Epochs')
            plt.ylabel('mAP')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            output_plot = self.train_dir / 'custom_loss_curve.png'
            plt.tight_layout()
            plt.savefig(output_plot, dpi=300)
            plt.close()
            
            logger.info(f"📊 Custom loss curve saved to: {output_plot}")
            
        except Exception as e:
            logger.error(f"❌ Failed to plot metrics: {e}")

    def predict(self, weights_path: str, source: str, conf: float = 0.25):
        """
        使用训练好的权重进行推理验证
        
        Args:
            weights_path (str):权重文件路径 (.pt)
            source (str): 待检测图片或文件夹路径
        """
        if not os.path.exists(weights_path):
            logger.error(f"❌ Weights not found: {weights_path}")
            return
        
        if not os.path.exists(source):
            logger.error(f"❌ Source not found: {source}")
            return

        logger.info(f"🔍 Loading weights: {weights_path}")
        try:
            model = YOLO(weights_path)
            
            logger.info(f"🖼️ Predicting on: {source}")
            model.predict(
                source=source,
                conf=conf,
                save=True,
                project=str(self.results_dir),
                name='predict',
                exist_ok=True
            )
            logger.info(f"✅ Prediction results saved to: {self.predict_dir}")
            
        except Exception as e:
            logger.error(f"❌ Prediction failed: {e}")


def main():
    parser = argparse.ArgumentParser(description="Task 2: Custom YOLOv8 Training")
    parser.add_argument('--mode', type=str, required=True, choices=['train', 'predict'],
                        help="运行模式: train(训练), predict(验证)")
    
    # 训练参数
    parser.add_argument('--data', type=str, default='data/custom_dataset/dataset.yaml',
                        help="数据集配置文件路径 (yaml)")
    parser.add_argument('--epochs', type=int, default=50, help="训练轮数")
    parser.add_argument('--batch', type=int, default=16, help="Batch size")
    
    # 预测/通用参数
    parser.add_argument('--model', type=str, default='yolov8n.pt', help="预训练模型 (for train)")
    parser.add_argument('--weights', type=str, default=None, help="训练好的权重路径 (for predict)")
    parser.add_argument('--source', type=str, default=None, help="预测输入源 (for predict)")
    
    args = parser.parse_args()
    
    trainer = YOLOTrainer(model_name=args.model)
    
    if args.mode == 'train':
        trainer.train(data_yaml=args.data, epochs=args.epochs, batch_size=args.batch)
        
    elif args.mode == 'predict':
        if not args.weights:
            # 尝试自动寻找最近一次训练的最佳权重
            potential_weights = Path('results/task2/train/weights/best.pt')
            if potential_weights.exists():
                args.weights = str(potential_weights)
                logger.info(f"ℹ️ Auto-selected best weights: {args.weights}")
            else:
                logger.error("❌ Please specify --weights path/to/best.pt")
                sys.exit(1)
        
        if not args.source:
             logger.error("❌ Please specify --source path/to/images")
             sys.exit(1)
             
        trainer.predict(weights_path=args.weights, source=args.source)

if __name__ == "__main__":
    main()
