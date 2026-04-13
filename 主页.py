# 主页.py

import streamlit as st

st.set_page_config(
    page_title="洛克王国工具箱",
    page_icon="🧰",
    layout="centered"
)

st.title("🧰 洛克王国工具箱")
st.caption("一个集能力值计算、速度排行、队伍配置、伤害模拟于一体的辅助工具")

st.markdown("---")

# -------------------- 工具卡片区（四列） --------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    ### 🐉 能力值计算器
    精确计算六维能力值，支持自定义种族、个体、性格、成长值。
    """)
    st.page_link("pages/1_能力值计算器.py", label="进入工具 →", icon="🐉")

with col2:
    st.markdown("""
    ### ⚡ 速度榜
    60级速度排行榜，对比极速、满速、平速、慢速四种配置。
    """)
    st.page_link("pages/2_速度榜.py", label="进入工具 →", icon="⚡")

with col3:
    st.markdown("""
    ### ⚔️ 伤害计算器
    基于攻防双方能力与技能参数，预估战斗伤害。
    """)
    st.page_link("pages/3_伤害计算器.py", label="进入工具 →", icon="⚔️")

with col4:
    st.markdown("""
    ### 📋 队伍配置器
    *开发中，敬请期待*
    """)
    st.button("进入工具 →", disabled=True, key="team")

st.markdown("---")

# -------------------- 致谢 --------------------
st.markdown(
    """
    <div style='text-align: center; color: #888; font-size: 14px;'>
        数据来源：Biligame Wiki · 洛克王国精灵图鉴<br>
        公式来源：B站专栏 · 洛克王国能力值计算
    </div>
    """,
    unsafe_allow_html=True
)