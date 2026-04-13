# components/sidebar.py

import streamlit as st
from config.constants import (
    STAT_OPTIONS, DISPLAY_TO_KEY, STAT_CHOICES,
    GROWTH_OPTIONS_HP, GROWTH_OPTIONS_OTHER, GROWTH_MAPPING
)
from data.loader import get_all_pokemon_names, get_pokemon_stats


def render_sidebar():
    """渲染侧边栏并返回所有输入参数"""
    st.sidebar.header("⚙️ 训练参数设置")

    # 1. 等级
    level = st.sidebar.number_input("📈 等级", min_value=1, max_value=100, value=60, step=1)

    # --- 预设精灵加载 ---
    st.sidebar.subheader("📚 预设精灵")
    all_pokemon = get_all_pokemon_names()
    selected_pokemon = st.sidebar.selectbox("选择精灵加载种族值", ["（手动输入）"] + all_pokemon)

    # 初始化 session_state 中的种族值存储
    if "base_stats" not in st.session_state:
        st.session_state.base_stats = {
            "hp": 100, "attack": 100, "defense": 100,
            "sp_atk": 100, "sp_def": 100, "speed": 100
        }

    # 当选择预设精灵时，显示预览并提供应用按钮
    if selected_pokemon != "（手动输入）":
        stats = get_pokemon_stats(selected_pokemon)
        if stats:
            st.sidebar.caption(
                f"生命:{stats['hp']} 物攻:{stats['attack']} 物防:{stats['defense']} "
                f"魔攻:{stats['sp_atk']} 魔防:{stats['sp_def']} 速度:{stats['speed']}"
            )
            if st.sidebar.button("应用此种族值"):
                st.session_state.base_stats = stats.copy()
                st.rerun()
    else:
        # 当用户切回手动输入时，不自动覆盖已修改的值，保持当前 session_state 不变
        pass

    # 2. 种族值（手动输入，默认值从 session_state 读取）
    st.sidebar.subheader("📊 种族值")
    base_hp = st.sidebar.number_input(
        "❤️ 生命种族值", min_value=1,
        value=st.session_state.base_stats["hp"], step=1
    )
    base_atk = st.sidebar.number_input(
        "⚔️ 物攻种族值", min_value=1,
        value=st.session_state.base_stats["attack"], step=1
    )
    base_def = st.sidebar.number_input(
        "🛡️ 物防种族值", min_value=1,
        value=st.session_state.base_stats["defense"], step=1
    )
    base_spa = st.sidebar.number_input(
        "🔮 魔攻种族值", min_value=1,
        value=st.session_state.base_stats["sp_atk"], step=1
    )
    base_spd = st.sidebar.number_input(
        "✨ 魔防种族值", min_value=1,
        value=st.session_state.base_stats["sp_def"], step=1
    )
    base_spe = st.sidebar.number_input(
        "💨 速度种族值", min_value=1,
        value=st.session_state.base_stats["speed"], step=1
    )

    # 3. 个体值（自由选择三项有效，其余为0）
    st.sidebar.subheader("✨ 个体值 (0~60)")
    st.sidebar.caption("勾选三项以启用个体值，未勾选的能力个体值固定为0")

    selected_stats = st.sidebar.multiselect(
        "选择三项有效个体值",
        options=list(STAT_OPTIONS.keys()),
        default=["❤️ 生命", "⚔️ 物攻", "💨 速度"],
        max_selections=3
    )

    iv_values = {"hp": 0, "atk": 0, "def": 0, "spa": 0, "spd": 0, "spe": 0}
    for display_name in selected_stats:
        key = STAT_OPTIONS[display_name]
        iv_values[key] = st.sidebar.number_input(
            f"{display_name}个体值",
            min_value=0, max_value=60, value=60, step=1,
            key=f"iv_{key}"
        )

    iv_hp = iv_values["hp"]
    iv_atk = iv_values["atk"]
    iv_def = iv_values["def"]
    iv_spa = iv_values["spa"]
    iv_spd = iv_values["spd"]
    iv_spe = iv_values["spe"]

    # 4. 性格修正（自定义增幅/减幅）
    st.sidebar.subheader("🌀 性格修正")
    col1, col2 = st.sidebar.columns(2)

    with col1:
        boost_stat_display = st.selectbox("增幅能力", STAT_CHOICES, index=1)
        boost_value = st.slider("增幅系数", min_value=1.1, max_value=1.2, value=1.2, step=0.01)

    with col2:
        nerf_stat_display = st.selectbox("减幅能力", STAT_CHOICES, index=3)
        nerf_value = 0.9
        st.metric("减幅系数", f"{nerf_value}")

    if boost_stat_display == nerf_stat_display:
        st.sidebar.warning("⚠️ 增幅与减幅不能选择同一项能力！请修改其中一项。")
        nature_info = 1.0
    else:
        boost_key = DISPLAY_TO_KEY[boost_stat_display]
        nerf_key = DISPLAY_TO_KEY[nerf_stat_display]
        nature_info = {
            "hp": 1.0, "attack": 1.0, "defense": 1.0,
            "sp_atk": 1.0, "sp_def": 1.0, "speed": 1.0
        }
        nature_info[boost_key] = boost_value
        nature_info[nerf_key] = nerf_value

    # 5. 成长值（生命与其他联动对应）
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

    # 将所有参数打包返回
    return {
        "level": level,
        "base_hp": base_hp, "base_atk": base_atk, "base_def": base_def,
        "base_spa": base_spa, "base_spd": base_spd, "base_spe": base_spe,
        "iv_hp": iv_hp, "iv_atk": iv_atk, "iv_def": iv_def,
        "iv_spa": iv_spa, "iv_spd": iv_spd, "iv_spe": iv_spe,
        "nature_info": nature_info,
        "growth_hp": growth_hp, "growth_other": growth_other
    }