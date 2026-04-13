# components/skill_selector.py

import streamlit as st


def render_skill_selector(default_power=80, default_stab=True):
    """
    渲染技能参数输入区域（手动填写版本）
    返回技能参数字典
    """
    st.subheader("✨ 技能参数")

    col1, col2, col3 = st.columns(3)

    with col1:
        power = st.number_input("技能威力", min_value=1, value=default_power, step=5)

    with col2:
        stab = st.checkbox("本系加成 (×1.25)", value=default_stab)
        stab_multiplier = 1.25 if stab else 1.0

    with col3:
        type_multiplier = st.selectbox(
            "属性克制倍率",
            options=[ 0.25, 0.5, 1.0, 2.0, 3.0],
            index=3,
            format_func=lambda x: f"×{x}"
        )

    col4, col5 = st.columns(2)
    with col4:
        ability_multiplier = st.number_input("特性加成", 0.0, 3.0, 1.0, 0.1, format="%.2f")
    with col5:
        other_multiplier = st.number_input("其他加成 (天气/道具)", 0.0, 3.0, 1.0, 0.1, format="%.2f")

    return {
        "power": power,
        "stab_multiplier": stab_multiplier,
        "type_multiplier": type_multiplier,
        "ability_multiplier": ability_multiplier,
        "other_multiplier": other_multiplier
    }