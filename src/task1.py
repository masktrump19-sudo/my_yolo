# -*- coding: utf-8 -*-
"""
Task 1: 环境搭建与模型体验 (Environment Setup & Model Experience)

功能描述:
    1. 自动下载并加载 YOLOv8 预训练模型
    2. 对指定目录下的图片进行批量检测
    3. 支持摄像头或视频文件的实时检测
    4. 自动保存检测结果和30秒演示片段

使用方法:
    python task1.py --mode image --source data/image
    python task1.py --mode video --source data/video/test.mp4
    python task1.py --mode camera

作者: my_yolo Team
日期: 2023-12-22
"""

import os
import sys
import time
import logging
import argparse
from pathlib import Path
from typing import Union

# 尝试导入核心库
try:
    import cv2
except ImportError:
    print("❌ Error: 'opencv-python' not found. Please install requirements: pip install -r requirements.txt")
    sys.exit(1)

try:
    from ultralytics import YOLO
except ImportError:
    print("❌ Error: 'ultralytics' not found. Please install requirements: pip install -r requirements.txt")
    sys.exit(1)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class YOLODetector:
    """YOLOv8 检测器类，封装核心检测逻辑"""

    def __init__(self, model_name: str = 'yolov8n.pt', results_dir: str = 'results'):
        """
        初始化检测器
        
        Args:
            model_name (str): 模型名称，初次使用会自动下载
            results_dir (str): 结果保存的根目录
        """
        self.model_name = model_name
        self.results_dir = Path(results_dir)
        self.detect_img_dir = self.results_dir / 'task1' / 'images'
        self.detect_video_dir = self.results_dir / 'task1' / 'videos'
        
        # 确保输出目录存在
        self._ensure_dirs()
        
        logger.info(f"⏳ Loading model: {model_name}...")
        try:
            self.model = YOLO(model_name)
            logger.info("✅ Model loaded successfully.")
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            sys.exit(1)

    def _ensure_dirs(self):
        """创建必要的输出目录"""
        self.detect_img_dir.mkdir(parents=True, exist_ok=True)
        self.detect_video_dir.mkdir(parents=True, exist_ok=True)

    def check_source(self, source: str) -> bool:
        """检查输入源是否存在"""
        if source == '0' or source == 'camera':
            return True
        path = Path(source)
        if not path.exists():
            logger.error(f"❌ Source path does not exist: {source}")
            return False
        return True

    def detect_images(self, source_dir: str, conf: float = 0.25):
        """
        批量检测图片
        
        Args:
            source_dir (str): 图片目录路径
            conf (float): 置信度阈值
        """
        if not self.check_source(source_dir):
            return

        source_path = Path(source_dir)
        # 支持常见图片格式
        img_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
        images = [p for p in source_path.iterdir() if p.suffix.lower() in img_extensions]
        
        if not images:
            logger.warning(f"⚠️ No images found in {source_dir}")
            return
            
        logger.info(f"🔍 Found {len(images)} images. Starting detection...")
        
        for img_path in images:
            try:
                # 执行推理
                results = self.model.predict(
                    source=str(img_path),
                    conf=conf,
                    save=True,
                    project=str(self.detect_img_dir.parent),
                    name='images',
                    exist_ok=True,
                    verbose=False
                )
                logger.info(f"✅ Processed: {img_path.name}")
            except Exception as e:
                logger.error(f"❌ Error processing {img_path.name}: {e}")
        
        logger.info(f"🎉 Image detection complete. Results saved to: {self.detect_img_dir}")

    def detect_video_stream(self, source: Union[str, int], duration: int = 30, conf: float = 0.25):
        """
        视频流实时检测（支持文件和摄像头）
        
        Args:
            source (str|int): 视频文件路径或摄像头ID(0)
            duration (int): 录制时长（秒）
            conf (float): 置信度阈值
        """
        input_source = 0 if source in ['0', 'camera'] else source
        if not self.check_source(str(source)):
            return

        cap = cv2.VideoCapture(input_source)
        if not cap.isOpened():
            logger.error("❌ Failed to open video source.")
            return

        # 获取视频属性
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0 or fps is None:
            fps = 30  # 默认FPS

        # 设置保存路径
        source_name = 'camera' if input_source == 0 else Path(source).stem
        save_path = self.detect_video_dir / f"{source_name}_demo.mp4"
        
        # 初始化视频写入器 (使用 mp4v 编码，兼容性较好)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(save_path), fourcc, fps, (width, height))
        
        logger.info(f"🎥 Starting video detection (Duration: {duration}s)...")
        logger.info("👉 Press 'q' to stop early.")

        start_time = time.time()
        frame_count = 0

        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # 检查是否超时
                elapsed = time.time() - start_time
                if elapsed > duration:
                    logger.info("⏰ Time limit reached.")
                    break

                # 执行推理
                results = self.model.predict(frame, conf=conf, verbose=False)
                annotated_frame = results[0].plot()

                # 写入视频和显示
                out.write(annotated_frame)
                # 服务器环境下注释掉 imshow，否则会报错 Unable to init server
                # cv2.imshow('YOLOv8 Detection', annotated_frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    logger.info("🛑 User stopped manually.")
                    break
                
                frame_count += 1
                if frame_count % 30 == 0:
                     print(f"⏳ Recording... {int(elapsed)}/{duration}s", end='\r')

        except KeyboardInterrupt:
            logger.info("🛑 Interrupted by user.")
        finally:
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            logger.info(f"\n✅ Video detection complete. Saved to: {save_path}")


def main():
    """主函数入口"""
    parser = argparse.ArgumentParser(description="Task 1: YOLOv8 Basic Detection")
    parser.add_argument('--mode', type=str, required=True, choices=['image', 'video', 'camera'],
                        help="运行模式: image(图片批量), video(视频文件), camera(摄像头)")
    parser.add_argument('--source', type=str, default='data/image',
                        help="输入源路径 (图片目录 或 视频文件路径)")
    parser.add_argument('--model', type=str, default='yolov8n.pt',
                        help="YOLOv8 模型版本 (n/s/m/l/x)")
    parser.add_argument('--conf', type=float, default=0.25,
                        help="检测置信度阈值")
    
    args = parser.parse_args()

    # 初始化工程
    # 可以选择在这里调用 utils 里的初始化，但为了独立性，这里保持自包含
    
    # 实例化检测器
    detector = YOLODetector(model_name=args.model)
    
    # 根据模式执行
    if args.mode == 'image':
        detector.detect_images(args.source, args.conf)
    elif args.mode == 'video':
        if args.source == 'data/image': # 默认值修正
             logger.error("❌ For video mode, please specify --source path/to/video.mp4")
             sys.exit(1)
        detector.detect_video_stream(args.source, duration=30, conf=args.conf)
    elif args.mode == 'camera':
        detector.detect_video_stream('camera', duration=30, conf=args.conf)

if __name__ == "__main__":
    main()