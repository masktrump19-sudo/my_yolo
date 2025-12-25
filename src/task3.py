# -*- coding: utf-8 -*-
"""
Task 3: 性能基准测试 (Performance Benchmark)

功能描述:
    1. 自动下载并对比 YOLOv8n, YOLOv8s, YOLOv8m 三个不同尺寸的模型
    2. 在同一测试集上循环测试
    3. 记录并计算：FPS（推理速度）、mAP50-95（准确率）、模型参数量 (Params)、模型大小 (Size)
    4. 生成 Markdown 格式的性能对比报告
    5. 智能分析并推荐最佳模型

使用方法:
    python task3.py --data data/custom_dataset/dataset.yaml

作者: my_yolo Team
日期: 2023-12-22
"""

import os
import sys
import time
import argparse
import logging
import torch
import pandas as pd
from pathlib import Path
from typing import List, Dict

try:
    from ultralytics import YOLO
except ImportError:
    print("❌ Error: 'ultralytics' not found. Please install requirements.")
    sys.exit(1)

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ModelBenchmark:
    """YOLOv8 模型性能基准测试器"""

    def __init__(self, data_yaml: str, results_dir: str = 'results/task3'):
        self.data_yaml = data_yaml
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # 定义要对比的模型列表
        self.models_to_test = ['yolov8n.pt', 'yolov8s.pt', 'yolov8m.pt']
        
        # 结果存储
        self.benchmark_results = []

    def run_benchmark(self):
        """执行基准测试主循环"""
        if not os.path.exists(self.data_yaml):
            logger.warning(f"⚠️ Dataset config not found: {self.data_yaml}")
            logger.warning("⚠️ Switching to 'coco128.yaml' for demonstration purposes.")
            self.data_yaml = 'coco128.yaml'  # 降级方案

        logger.info(f"🚀 Starting benchmark on dataset: {self.data_yaml}")
        
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        logger.info(f"💻 Compute Device: {device.upper()}")

        for model_name in self.models_to_test:
            self._test_single_model(model_name, device)
            
        # 生成报告
        self._generate_report()

    def _test_single_model(self, model_name: str, device: str):
        """测试单个模型"""
        logger.info(f"\n🧪 Testing model: {model_name}...")
        
        try:
            # 1. 加载模型
            model = YOLO(model_name)
            
            # 2. 获取模型基础信息
            # model.info() 返回 (layers, params, gradients, flops)
            # 但我们需要更直观的属性，部分可以通过 model.model.parameters() 计算
            params_cnt = sum(p.numel() for p in model.model.parameters()) / 1e6  # Million
            
            # 计算模型文件大小 (MB)
            # 如果是自动下载的，权重通常在当前目录
            if os.path.exists(model_name):
                model_size = os.path.getsize(model_name) / 1e6 # MB
            else:
                model_size = 0.0 # 无法获取

            # 3. 评估准确率 (mAP)
            logger.info("   Running validation to measure mAP...")
            val_results = model.val(data=self.data_yaml, split='val', verbose=False, device=device)
            map50_95 = val_results.box.map    # mAP50-95
            map50 = val_results.box.map50     # mAP50

            # 4. 评估推理速度 (FPS)
            # 使用 val 模式的 speed 属性，或者手动跑 predict
            # val_results.speed 包含 {'preprocess': t1, 'inference': t2, 'loss': t3, 'postprocess': t4} (ms)
            inference_time_ms = val_results.speed['inference']
            fps = 1000.0 / (inference_time_ms + val_results.speed['preprocess'] + val_results.speed['postprocess'])

            logger.info(f"   ✅ {model_name} Results: mAP={map50_95:.3f}, FPS={fps:.1f}")

            # 记录结果
            self.benchmark_results.append({
                'Model': model_name,
                'Size (MB)': round(model_size, 2),
                'Params (M)': round(params_cnt, 2),
                'mAP 50-95': round(map50_95, 3),
                'mAP 50': round(map50, 3),
                'Inference (ms)': round(inference_time_ms, 2),
                'FPS': round(fps, 1)
            })
            
            # 清理显存
            del model
            if device == 'cuda':
                torch.cuda.empty_cache()

        except Exception as e:
            logger.error(f"❌ Failed to test {model_name}: {e}")

    def _generate_report(self):
        """生成 Markdown 报告和分析建议"""
        if not self.benchmark_results:
            logger.error("❌ No results to report.")
            return

        df = pd.DataFrame(self.benchmark_results)
        
        # 1. 生成 Markdown 表格
        md_table = df.to_markdown(index=False)
        
        # 2. 智能分析
        best_acc_model = df.loc[df['mAP 50-95'].idxmax()]
        fastest_model = df.loc[df['FPS'].idxmax()]
        
        # 简单推荐逻辑：首先满足实时性(FPS>30)，然后选mAP最高的
        realtime_models = df[df['FPS'] >= 30]
        if not realtime_models.empty:
            recommended_model = realtime_models.loc[realtime_models['mAP 50-95'].idxmax()]
            reason = "它在保持实时性能 (FPS > 30) 的同时提供了最高的准确率。"
        else:
            recommended_model = fastest_model
            reason = "当前没有模型满足 30 FPS，推荐最快的模型以保证流畅度。"

        report_content = f"""# 📊 YOLOv8 性能基准测试报告

**测试时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}
**测试数据集**: `{self.data_yaml}`
**计算设备**: `{'CUDA (GPU)' if torch.cuda.is_available() else 'CPU'}`

## 1. 性能对比表格

{md_table}

## 2. 详细指标说明
*   **mAP 50-95**: 平均精度均值（IoU在此范围内），综合反映检测准确率。
*   **FPS**: 每秒处理帧数，反映推理速度。大于 30 通常视为实时。
*   **Params**: 模型参数量，反映模型复杂度。

## 3. 🏆 最佳模型推荐

**推荐模型**: **{recommended_model['Model']}**

**推荐理由**: {reason}

*   如果你追求**极致精度**，可以选择 **{best_acc_model['Model']}** (mAP: {best_acc_model['mAP 50-95']})。
*   如果你追求**极致速度**，可以选择 **{fastest_model['Model']}** (FPS: {fastest_model['FPS']})。
"""
        
        report_path = self.results_dir / 'benchmark_report.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
            
        logger.info(f"\n📝 Report generated successfully: {report_path}")
        print("\n" + report_content) # 同时打印到控制台


def main():
    parser = argparse.ArgumentParser(description="Task 3: YOLOv8 Performance Benchmark")
    parser.add_argument('--data', type=str, default='data/custom_dataset/dataset.yaml',
                        help="数据集配置文件路径 (yaml)")
    args = parser.parse_args()
    
    benchmark = ModelBenchmark(data_yaml=args.data)
    benchmark.run_benchmark()

if __name__ == "__main__":
    main()
