import streamlit as st
from components.sidebar import render_sidebar
from components.main_display import render_main_display

# -------------------- 页面配置 --------------------
st.set_page_config(page_title="洛克王国能力值计算器", page_icon="🐉")
st.title("🐉 洛克王国 · 能力值计算器")
st.caption("基于等级、种族、个体、性格与成长值计算六维能力")

# -------------------- 渲染侧边栏并获取参数 --------------------
params = render_sidebar()

# -------------------- 渲染主界面 --------------------
render_main_display(params)