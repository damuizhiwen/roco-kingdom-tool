# components/sidebar.py

import streamlit as st
from config.constants import (
    GROWTH_OPTIONS_HP, GROWTH_OPTIONS_OTHER, GROWTH_MAPPING
)
from data.loader import get_all_pokemon_names, get_pokemon_stats


def render_sidebar():
    """渲染侧边栏，包含等级、种族值、成长值，返回基础参数字典"""
    st.sidebar.header("⚙️ 基础参数")

    # --- 1. 等级---
    level = st.sidebar.number_input("📈 等级", min_value=1, max_value=100, value=60, step=1)

    # --- 2. 预设精灵加载 ---
    with st.sidebar.expander("📚 预设精灵（点击展开）", expanded=False):
        all_pokemon = get_all_pokemon_names()
        selected_pokemon = st.selectbox("选择精灵加载种族值", ["（手动输入）"] + all_pokemon)

        if "base_stats" not in st.session_state:
            st.session_state.base_stats = {
                "hp": 100, "attack": 100, "defense": 100,
                "sp_atk": 100, "sp_def": 100, "speed": 100
            }

        if selected_pokemon != "（手动输入）":
            stats = get_pokemon_stats(selected_pokemon)
            if stats:
                st.caption(
                    f"生命:{stats['hp']} 物攻:{stats['attack']} 物防:{stats['defense']} "
                    f"魔攻:{stats['sp_atk']} 魔防:{stats['sp_def']} 速度:{stats['speed']}"
                )
                if st.button("应用此种族值"):
                    st.session_state.base_stats = stats.copy()
                    st.rerun()

    # --- 3. 种族值输入（两列布局）---
    st.sidebar.subheader("📊 种族值")
    col_base1, col_base2 = st.sidebar.columns(2)

    with col_base1:
        base_hp = st.number_input("❤️ 生命", min_value=1, value=st.session_state.base_stats["hp"], step=1)
        base_atk = st.number_input("⚔️ 物攻", min_value=1, value=st.session_state.base_stats["attack"], step=1)
        base_def = st.number_input("🛡️ 物防", min_value=1, value=st.session_state.base_stats["defense"], step=1)

    with col_base2:
        base_spa = st.number_input("🔮 魔攻", min_value=1, value=st.session_state.base_stats["sp_atk"], step=1)
        base_spd = st.number_input("✨ 魔防", min_value=1, value=st.session_state.base_stats["sp_def"], step=1)
        base_spe = st.number_input("💨 速度", min_value=1, value=st.session_state.base_stats["speed"], step=1)

    # --- 4. 成长值联动 ---
    st.sidebar.subheader("📈 成长值")

    if "growth_hp" not in st.session_state:
        st.session_state.growth_hp = 100
    if "growth_other" not in st.session_state:
        st.session_state.growth_other = 50

    def sync_growth_from_hp():
        st.session_state.growth_other = GROWTH_MAPPING[st.session_state.growth_hp]

    def sync_growth_from_other():
        selected_other = st.session_state.growth_other
        for hp_val, other_val in GROWTH_MAPPING.items():
            if other_val == selected_other:
                st.session_state.growth_hp = hp_val
                break

    growth_hp = st.sidebar.selectbox(
        "❤️ 生命成长值",
        options=GROWTH_OPTIONS_HP,
        index=GROWTH_OPTIONS_HP.index(st.session_state.growth_hp),
        key="growth_hp",
        on_change=sync_growth_from_hp
    )

    growth_other = st.sidebar.selectbox(
        "⚔️ 其他成长值",
        options=GROWTH_OPTIONS_OTHER,
        index=GROWTH_OPTIONS_OTHER.index(st.session_state.growth_other),
        key="growth_other",
        on_change=sync_growth_from_other
    )

    return {
        "level": level,
        "base_hp": base_hp, "base_atk": base_atk, "base_def": base_def,
        "base_spa": base_spa, "base_spd": base_spd, "base_spe": base_spe,
        "growth_hp": growth_hp, "growth_other": growth_other
    }