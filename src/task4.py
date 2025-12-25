# -*- coding: utf-8 -*-
"""
Task 4: YOLOv8 深度学习作业展示平台 (Final V8 - Cyberpunk No-Image Edition)
Author: 黄永庆
Features: 纯代码生成粒子流星 | 零外部图片依赖 | 赛博朋克霓虹UI
"""

import sys
import tempfile
import time
import random
from pathlib import Path
import cv2
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

# ================= 1. 页面基础配置 =================
st.set_page_config(
    page_title="深度学习作业展示 - 黄永庆",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= 2. 纯代码生成炫酷特效 (无需图片) =================
def set_tech_style():
    # --- Python 动态生成星星坐标 ---
    # 这段代码会生成几百个随机坐标，模拟星星，完全不依赖图片
    def create_stars(n):
        # 生成格式: "x坐标 y坐标 模糊度 颜色"
        stars = []
        for _ in range(n):
            x = random.randint(0, 2000)
            y = random.randint(0, 2000)
            stars.append(f"{x}px {y}px #FFF")
        return ", ".join(stars)

    small_stars = create_stars(700)
    medium_stars = create_stars(200)
    big_stars = create_stars(100)

    st.markdown(f"""
        <style>
        /* 引入科幻字体 (如果加载失败会自动回退到系统字体，不影响使用) */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Roboto:wght@300;400;700&display=swap');
        
        /* --- 1. 背景基调：深空黑紫渐变 --- */
        .stApp {{
            background: radial-gradient(ellipse at bottom, #0d1d31 0%, #0c0d13 100%);
            overflow-x: hidden;
        }}

        /* --- 2. 纯 CSS 粒子流动动画 (核心特效) --- */
        @keyframes animStar {{
            from {{ transform: translateY(0px); }}
            to {{ transform: translateY(-2000px); }}
        }}

        /* 星星层 1 (小，慢) */
        .stApp::before {{
            content: " ";
            position: fixed;
            top: 0; left: 0;
            width: 1px; height: 1px;
            background: transparent;
            box-shadow: {small_stars};
            animation: animStar 50s linear infinite;
            z-index: -3; /* 确保在最底层 */
            opacity: 0.8;
        }}
        
        /* 星星层 2 (中，快) */
        .stApp::after {{
            content: " ";
            position: fixed;
            top: 0; left: 0;
            width: 2px; height: 2px;
            background: transparent;
            box-shadow: {medium_stars};
            animation: animStar 100s linear infinite;
            z-index: -2;
            opacity: 0.6;
        }}

        /* --- 3. 侧边栏极致高亮 (赛博朋克风格) --- */
        [data-testid="stSidebar"] {{
            background: rgba(10, 15, 30, 0.85); /* 半透明深色 */
            backdrop-filter: blur(20px); /* 强力磨砂 */
            border-right: 2px solid #00FFFF; /* 霓虹边框 */
            box-shadow: 10px 0 30px rgba(0, 255, 255, 0.15);
        }}
        
        /* 侧边栏标题 */
        .sidebar-header {{
            font-family: 'Orbitron', sans-serif;
            font-size: 1.8rem;
            /* 渐变流光字体 */
            background: linear-gradient(90deg, #00FFFF, #FF00FF); 
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 900;
            text-align: center;
            margin: 20px 0;
            text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            padding-bottom: 10px;
        }}

        /* 强制高亮侧边栏所有文字 */
        [data-testid="stSidebar"] label {{
            color: #00FFFF !important; /* 荧光青 */
            font-weight: bold !important;
            font-family: 'Orbitron', sans-serif !important;
            text-shadow: 0 0 5px rgba(0, 255, 255, 0.6);
            font-size: 1rem !important;
        }}
        [data-testid="stSidebar"] p {{
            color: #E0E0E0 !important;
            font-size: 0.95rem;
        }}
        /* 单选框选中状态 */
        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"] p {{
            color: #FF00FF !important; /* 洋红高亮 */
            font-weight: bold !important;
            text-shadow: 0 0 10px #FF00FF;
        }}

        /* --- 4. 作者卡片 (全息投影质感) --- */
        .author-card {{
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid #00FFFF;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.2), inset 0 0 20px rgba(0, 255, 255, 0.1);
            margin-bottom: 30px;
            position: relative;
            overflow: hidden;
        }}
        /* 扫描线特效 */
        .author-card::after {{
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 5px;
            background: rgba(0, 255, 255, 0.5);
            box-shadow: 0 0 10px #00FFFF;
            animation: scan 3s linear infinite;
            opacity: 0.3;
        }}
        @keyframes scan {{ 0% {{top: 0%;}} 100% {{top: 100%;}} }}

        .author-item {{
            color: #FFF; margin: 8px 0; font-size: 1.05rem;
            display: flex; align-items: center;
        }}
        .author-label {{
            color: #FFD700; font-weight: bold; margin-right: 10px; min-width: 60px;
            text-shadow: 0 0 5px #FFD700;
        }}

        /* --- 5. 主界面组件 --- */
        /* 霓虹标题 */
        .main-title {{
            font-family: 'Orbitron', sans-serif;
            text-align: center;
            font-size: 3.8rem;
            color: #fff;
            text-shadow: 
                0 0 10px #00FFFF,
                0 0 20px #00FFFF,
                0 0 40px #00FFFF,
                0 0 80px #00FFFF;
            margin-bottom: 10px;
        }}
        .sub-title {{
            text-align: center; color: #FF00FF; margin-bottom: 40px; font-size: 1.5rem;
            text-shadow: 0 0 10px rgba(255, 0, 255, 0.6);
            letter-spacing: 3px;
            font-weight: 300;
        }}

        /* 磨砂玻璃容器 */
        .glass-container {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
            margin-bottom: 20px;
        }}

        /* 赛博朋克按钮 */
        .stButton>button {{
            background: transparent;
            color: #00FFFF;
            border: 2px solid #00FFFF;
            border-radius: 5px;
            padding: 0.5rem 2rem;
            font-family: 'Orbitron', sans-serif;
            font-size: 1.2rem;
            font-weight: bold;
            transition: 0.3s;
            box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
            width: 100%;
        }}
        .stButton>button:hover {{
            background: #00FFFF;
            color: #000;
            box-shadow: 0 0 30px #00FFFF, 0 0 60px #00FFFF;
            transform: scale(1.02);
        }}
        </style>
    """, unsafe_allow_html=True)

set_tech_style()

# 检查依赖
try:
    from ultralytics import YOLO
except ImportError:
    st.error("❌ 错误: 未安装 'ultralytics' 库。")
    st.stop()

# ================= 3. 侧边栏：作者与控制 =================
with st.sidebar:
    # --- 全息作者卡片 ---
    st.markdown("""
        <div class="author-card">
            <h3 style="color:#FFF; border-bottom:2px solid #00FFFF; padding-bottom:10px; margin-top:0; text-align:center; font-family:'Orbitron';">👤 作者贡献</h3>
            <div class="author-item"><span class="author-label">🎓 姓名</span> 黄永庆</div>
            <div class="author-item"><span class="author-label">🆔 学号</span> 23354076</div>
            <div class="author-item"><span class="author-label">🏛️ 学校</span> 中山大学</div>
            <div class="author-item"><span class="author-label">🔬 学院</span> 智能工程学院</div>
            <div class="author-item"><span class="author-label">📚 课程</span> 深度学习</div>
            <div class="author-item"><span class="author-label">👨‍🏫 指导</span> 曾海鹏</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-header">⚙️ 系统配置</div>', unsafe_allow_html=True)
    
    # 模型选择
    model_source = st.radio("模型来源 (Source)", ["官方预训练 (COCO)", "自定义权重 (My Best)"])
    
    if model_source == "官方预训练 (COCO)":
        model_name = st.selectbox("选择版本 (Version)", ["yolov8n.pt", "yolov8s.pt", "yolov8m.pt"], index=2)
        model_path = model_name
    else:
        st.info("💡 提示：请上传 Task 2 训练好的 best.pt")
        uploaded_model = st.file_uploader("上传权重文件 (.pt)", type=['pt'])
        if uploaded_model:
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.pt')
            tfile.write(uploaded_model.read())
            model_path = tfile.name
        else:
            model_path = None

    st.markdown("---")
    st.markdown("### 🎛️ 参数微调")
    conf_thres = st.slider("置信度 (Confidence)", 0.0, 1.0, 0.40, 0.05)
    iou_thres = st.slider("IoU 阈值 (NMS)", 0.0, 1.0, 0.45, 0.05)

# 加载模型
@st.cache_resource
def load_yolo_model(path):
    return YOLO(path)

# ================= 4. 主界面逻辑 =================

st.markdown('<div class="main-title">YOLOv8 视觉系统</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">INTELLIGENT ENGINEERING SCHOOL PROJECT</div>', unsafe_allow_html=True)

if not model_path:
    st.warning("👈 请在左侧加载模型以开始。")
    st.stop()

try:
    with st.spinner("💾 系统初始化中..."):
        model = load_yolo_model(model_path)
except Exception as e:
    st.error(f"模型加载失败: {e}")
    st.stop()

tab1, tab2, tab3 = st.tabs(["🖼️ 图片分析", "🎥 视频分析", "📷 实时拍摄"])

# --- 图片检测 ---
with tab1:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("上传图片", type=['jpg', 'png', 'jpeg', 'bmp', 'webp'])
    
    if uploaded_file:
        col1, col2 = st.columns([1, 1])
        image = Image.open(uploaded_file)
        
        # 结果缓存
        if 'res_img' not in st.session_state:
            st.session_state['res_img'] = None

        with col1:
            st.image(image, caption="原始输入")

        with col2:
            if st.button("🚀 启动神经网路 (Analyze)", key="btn_img", use_container_width=True):
                with st.spinner("🌌 正在进行张量运算..."):
                    start_time = time.time()
                    res = model.predict(image, conf=conf_thres, iou=iou_thres)
                    end_time = time.time()
                    
                    st.session_state['res_img'] = res
                    
                    res_plotted = res[0].plot()
                    st.image(res_plotted, caption="分析结果")
                    
                    fps = 1 / (end_time - start_time)
                    st.success(f"⚡ 耗时: {(end_time - start_time)*1000:.1f}ms | FPS: {fps:.1f}")

        # 统计图表
        if st.session_state['res_img']:
            res = st.session_state['res_img']
            boxes = res[0].boxes
            if len(boxes) > 0:
                st.markdown("---")
                st.markdown('<h4 style="color:#FF00FF; text-align:center; font-family:Orbitron;">📊 目标检测统计</h4>', unsafe_allow_html=True)
                cls_ids = boxes.cls.cpu().numpy().astype(int)
                names = model.model.names
                detected_counts = pd.Series([names[i] for i in cls_ids]).value_counts()
                
                # 炫酷配色的图表
                st.bar_chart(detected_counts, color="#00FFFF")
            else:
                st.info("背景干净，未检测到目标。")
            st.session_state['res_img'] = None

    st.markdown('</div>', unsafe_allow_html=True)

# --- 视频检测 ---
with tab2:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    video_file = st.file_uploader("上传视频", type=['mp4', 'avi', 'mov'])
    
    if video_file:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(video_file.read())
        
        st.video(tfile.name)
        
        if st.button("▶️ 启动视频流分析", key="btn_video", use_container_width=True):
            cap = cv2.VideoCapture(tfile.name)
            st_frame = st.empty()
            st_progress = st.progress(0)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            current_frame = 0
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret: break
                
                current_frame += 1
                if total_frames > 0:
                    st_progress.progress(current_frame / total_frames)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = model.predict(frame, conf=conf_thres, verbose=False)
                res_plotted = results[0].plot()
                st_frame.image(res_plotted, caption=f"Frame: {current_frame}/{total_frames}")
            
            cap.release()
            st.success("🎉 分析完成！")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 摄像头 ---
with tab3:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    col_cam, col_info = st.columns([2, 1])
    with col_info:
        st.markdown("### 📸 实时捕获")
        st.info("数据将上传至 A6000 进行实时推理。")
    
    with col_cam:
        img_file_buffer = st.camera_input("拍照")

    if img_file_buffer:
        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        frame_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        
        with st.spinner("🤖 正在识别..."):
            res = model.predict(frame_rgb, conf=conf_thres)
            res_plotted = res[0].plot()
            st.image(res_plotted, caption="实时结果")
            
            if len(res[0].boxes) > 0:
                st.balloons()
                st.success(f"🎯 发现 {len(res[0].boxes)} 个目标！")
            else:
                st.warning("未检测到目标。")
    st.markdown('</div>', unsafe_allow_html=True)