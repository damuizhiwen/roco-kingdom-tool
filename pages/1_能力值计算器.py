# app.py

import streamlit as st
from components.sidebar import render_sidebar
from components.main_display import render_main_display
from config.constants import STAT_OPTIONS, DISPLAY_TO_KEY, STAT_CHOICES

# -------------------- 页面配置 --------------------
st.set_page_config(page_title="能力值计算器", page_icon="🐉", layout="centered")

# -------------------- 自定义 CSS：统一样式与精确对齐 --------------------
st.markdown(
    """
    <style>
        /* ---------- 侧边栏宽度调整 ---------- */
        section[data-testid="stSidebar"] {
            width: 400px !important;
        }
        section[data-testid="stSidebar"] + div {
            margin-left: 0px;
        }

        /* ---------- 主界面文字居中 ---------- */
        .main > div {
            text-align: center;
        }
        h1, h2, h3, .caption {
            text-align: center !important;
        }
        [data-testid="stMetric"] {
            text-align: center;
        }
        [data-testid="stMetric"] label {
            justify-content: center;
        }
        [data-testid="column"] {
            text-align: center;
        }

        /* ---------- 精确对齐：移除列默认内边距 ---------- */
        [data-testid="column"] {
            padding-left: 0 !important;
            padding-right: 0 !important;
        }

        /* 等级列微调（若侧边栏无等级可忽略） */
        [data-testid="column"]:first-child {
            padding-left: 1rem !important;
        }

        /* 个体值三列之间加一点间隙 */
        .stHorizontalBlock [data-testid="column"] {
            padding-right: 8px !important;
        }

        /* 性格修正容器左对齐微调 */
        .nature-align-container {
            margin-left: -12px;  /* 根据实际视觉可微调 */
        }

        /* 性格修正内部第一列（下拉框）去除多余边距 */
        .nature-align-container [data-testid="column"]:first-child {
            padding-left: 0 !important;
            margin-left: 0 !important;
        }

        /* 下拉框与输入框宽度自适应 */
        .nature-align-container .stSelectbox div[data-baseweb="select"] {
            width: 100%;
        }

        .nature-align-container .stSlider,
        .nature-align-container .stNumberInput {
            width: 100%;
        }

        /* 防止下拉框文字溢出 */
        .stSelectbox [data-baseweb="select"] span {
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        /* 能力值平行展示的额外样式（已在 main_display 中定义，此处保留全局备用） */
        .stat-row {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 12px 0;
        }
        .stat-label {
            font-size: 22px;
            font-weight: 500;
            margin-right: 20px;
            min-width: 100px;
            text-align: right;
        }
        .stat-value {
            font-size: 32px;
            font-weight: bold;
            color: #1f77b4;
            min-width: 70px;
            text-align: left;
        }
        .stats-container {
            display: flex;
            justify-content: center;
            gap: 60px;
            margin-top: 20px;
            margin-bottom: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------- 标题与说明 --------------------
st.title("🐉 洛克王国 · 能力值计算器")
st.caption("基于等级、种族、个体、性格与成长值计算六维能力")

# -------------------- 侧边栏：等级、种族值、成长值 --------------------
base_params = render_sidebar()

# -------------------- 主界面顶部：个体值、性格修正 --------------------
st.header("⚙️ 训练参数")

col_iv, col_nature = st.columns([2, 1])  # 个体值占2份，性格修正占1份

with col_iv:
    st.caption("✨ 个体值 (0~60，勾选三项有效)")
    selected_stats = st.multiselect(
        "选择三项有效个体值",
        options=list(STAT_OPTIONS.keys()),
        default=["❤️ 生命", "⚔️ 物攻", "💨 速度"],
        max_selections=3,
        label_visibility="collapsed"
    )
    iv_values = {"hp": 0, "atk": 0, "def": 0, "spa": 0, "spd": 0, "spe": 0}
    iv_cols = st.columns(3)
    for i, display_name in enumerate(selected_stats):
        key = STAT_OPTIONS[display_name]
        with iv_cols[i]:
            iv_values[key] = st.number_input(
                display_name,
                min_value=0,
                max_value=60,
                value=60,
                step=1,
                key=f"iv_{key}"
            )

with col_nature:
    st.caption("🌀 性格修正")
    with st.container():
        st.markdown('<div class="nature-align-container">', unsafe_allow_html=True)

        # 增幅行
        boost_col1, boost_col2 = st.columns([2, 1])
        with boost_col1:
            boost_stat = st.selectbox(
                "增幅能力", STAT_CHOICES, index=1, key="boost", label_visibility="collapsed"
            )
        with boost_col2:
            boost_val = st.slider(
                "增幅系数", 1.1, 1.2, 1.2, 0.01, key="boost_val", label_visibility="collapsed"
            )

        # 减幅行
        nerf_col1, nerf_col2 = st.columns([2, 1])
        with nerf_col1:
            nerf_stat = st.selectbox(
                "减幅能力", STAT_CHOICES, index=3, key="nerf", label_visibility="collapsed"
            )
        with nerf_col2:
            nerf_val = 0.9
            st.number_input(
                "减幅系数",
                value=nerf_val,
                step=0.01,
                format="%.2f",
                disabled=True,
                key="nerf_val_display",
                label_visibility="collapsed"
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # 冲突检测
    if boost_stat == nerf_stat:
        st.warning("⚠️ 增幅与减幅不能相同")
        nature_info = 1.0
    else:
        nature_info = {
            "hp": 1.0, "attack": 1.0, "defense": 1.0,
            "sp_atk": 1.0, "sp_def": 1.0, "speed": 1.0
        }
        nature_info[DISPLAY_TO_KEY[boost_stat]] = boost_val
        nature_info[DISPLAY_TO_KEY[nerf_stat]] = nerf_val

# -------------------- 整合所有参数 --------------------
params = {
    **base_params,  # 包含 level, base_*, growth_*
    "iv_hp": iv_values["hp"],
    "iv_atk": iv_values["atk"],
    "iv_def": iv_values["def"],
    "iv_spa": iv_values["spa"],
    "iv_spd": iv_values["spd"],
    "iv_spe": iv_values["spe"],
    "nature_info": nature_info
}

# -------------------- 主界面：能力值展示 --------------------
render_main_display(params)