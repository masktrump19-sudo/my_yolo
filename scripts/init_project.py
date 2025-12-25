"""
项目初始化脚本
自动创建所有必需的目录结构

用法:
    python scripts/init_project.py
"""

import os
from pathlib import Path


def create_directory_structure():
    """创建完整的项目目录结构"""
    
    # 定义目录结构
    directories = [
        # 数据目录
        "data/image",
        "data/video", 
        "data/custom_dataset/images/train",
        "data/custom_dataset/images/val",
        "data/custom_dataset/labels/train",
        "data/custom_dataset/labels/val",
        
        # 模型目录
        "models/weights",
        "models/checkpoints",
        
        # 结果目录
        "results/task1/images",
        "results/task1/videos",
        "results/task2/train",
        "results/task2/predict",
        "results/task3",
        "results/task4",
        
        # 输出目录
        "outputs",
        
        # 日志目录
        "logs",
        
        # 文档目录
        "docs",
        
        # 脚本目录（已存在但确保）
        "scripts",
        
        # 源代码目录
        "src",
    ]
    
    print("🚀 开始初始化项目目录结构...")
    print()
    
    created_count = 0
    existed_count = 0
    
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ 创建目录: {directory}")
            created_count += 1
        else:
            print(f"⏭️  目录已存在: {directory}")
            existed_count += 1
    
    print()
    print(f"📊 统计信息:")
    print(f"   - 新创建: {created_count} 个目录")
    print(f"   - 已存在: {existed_count} 个目录")
    print()
    print("✨ 项目目录结构初始化完成！")


def create_placeholder_files():
    """创建必要的占位文件"""
    
    print("\n📝 创建占位文件...")
    
    placeholder_files = {
        "data/README.md": "# 数据目录\n\n请将测试图片放在 `image/` 目录下，测试视频放在 `video/` 目录下。\n",
        "models/README.md": "# 模型目录\n\n预训练模型和训练好的模型权重将保存在此目录。\n",
        "results/README.md": "# 结果目录\n\n所有任务的检测结果将保存在对应的子目录中。\n",
        "outputs/README.md": "# 输出目录\n\n临时输出文件和中间结果。\n",
        "logs/README.md": "# 日志目录\n\n程序运行日志。\n",
    }
    
    for file_path, content in placeholder_files.items():
        path = Path(file_path)
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 创建文件: {file_path}")
        else:
            print(f"⏭️  文件已存在: {file_path}")


def check_required_files():
    """检查必需的项目文件"""
    
    print("\n🔍 检查必需文件...")
    
    required_files = [
        "README.md",
        "requirements.txt",
        "config.yaml",
        "setup.py",
        ".gitignore",
        "src/__init__.py",
        "src/utils.py",
    ]
    
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
            print(f"❌ 缺失: {file}")
        else:
            print(f"✅ 存在: {file}")
    
    if missing_files:
        print(f"\n⚠️  警告: {len(missing_files)} 个必需文件缺失")
        print("   请确保这些文件被正确创建")
    else:
        print("\n✅ 所有必需文件都存在")


def main():
    """主函数"""
    
    print("=" * 60)
    print("🎯 YOLO目标检测项目 - 初始化脚本")
    print("=" * 60)
    print()
    
    # 确保在项目根目录运行
    if not Path("src").exists() and not Path("README.md").exists():
        print("❌ 错误: 请在项目根目录下运行此脚本！")
        print("   cd my_yolo")
        print("   python scripts/init_project.py")
        return
    
    # 创建目录结构
    create_directory_structure()
    
    # 创建占位文件
    create_placeholder_files()
    
    # 检查必需文件
    check_required_files()
    
    print()
    print("=" * 60)
    print("🎉 项目初始化完成！")
    print("=" * 60)
    print()
    print("📌 下一步:")
    print("   1. 创建虚拟环境: conda create -n my_yolo python=3.10 -y")
    print("   2. 激活环境: conda activate my_yolo")
    print("   3. 安装依赖: pip install -r requirements.txt")
    print("   4. 查看文档: docs/ 目录")
    print()


if __name__ == "__main__":
    main()
