# pages/3_伤害计算器.py

import streamlit as st
from data.loader import get_all_pokemon_names, get_pokemon_stats
from utils.formulas import calculate_hp_roco, calculate_other_roco, calculate_damage

st.set_page_config(page_title="伤害计算器", page_icon="⚔️", layout="wide")

st.title("⚔️ 洛克王国 · 伤害计算器")
st.caption("左侧攻击方 · 右侧防御方 · 中间技能与击杀预估 | 可一键交换位置")

# -------------------- 常量 --------------------
GROWTH = 50
IV_OPTIONS = [0, 42, 48, 54, 60]
DEFAULT_IV = 60  # 默认个体值
NATURE_BOOST = 1.2
NATURE_NERF = 0.9

STAT_LABELS = {
    "hp": "❤️ HP",
    "attack": "⚔️ 物攻",
    "defense": "🛡️ 物防",
    "sp_atk": "🔮 魔攻",
    "sp_def": "✨ 魔防",
    "speed": "💨 速度"
}
STAT_KEYS = ["hp", "attack", "defense", "sp_atk", "sp_def", "speed"]

# -------------------- 精灵列表 --------------------
all_pokemon = get_all_pokemon_names()
if not all_pokemon:
    st.error("精灵数据加载失败，请检查 data/sprites_stats.json")
    st.stop()

def get_stat(base, iv, level, nature_mod, growth=GROWTH):
    return calculate_other_roco(base, iv, level, nature_mod, growth)

def get_hp(base, iv, level, nature_mod, growth=GROWTH):
    return calculate_hp_roco(base, iv, level, nature_mod, growth)

# -------------------- session_state 初始化 --------------------
def init_session():
    defaults = {
        # 攻击方
        "att_name": all_pokemon[0],
        "att_level": 60,
        "att_selected_ivs": ["❤️ HP", "⚔️ 物攻", "💨 速度"],
        "att_iv_hp": DEFAULT_IV, "att_iv_atk": DEFAULT_IV, "att_iv_def": 0,
        "att_iv_spa": 0, "att_iv_spd": 0, "att_iv_spe": DEFAULT_IV,
        "att_boost_stat": "⚔️ 物攻",
        "att_nerf_stat": "🔮 魔攻",
        # 防御方
        "def_name": all_pokemon[0],
        "def_level": 60,
        "def_selected_ivs": ["❤️ HP", "🛡️ 物防", "💨 速度"],
        "def_iv_hp": DEFAULT_IV, "def_iv_atk": 0, "def_iv_def": DEFAULT_IV,
        "def_iv_spa": 0, "def_iv_spd": 0, "def_iv_spe": DEFAULT_IV,
        "def_boost_stat": "🛡️ 物防",
        "def_nerf_stat": "🔮 魔攻",
        # 攻击类型
        "attack_type": "⚔️ 物理攻击",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session()

# -------------------- 性格修正构建函数 --------------------
def build_nature_dict(boost_display, nerf_display):
    display_to_key = {v: k for k, v in STAT_LABELS.items()}
    nature = {k: 1.0 for k in STAT_KEYS}
    if boost_display == nerf_display:
        return nature
    nature[display_to_key[boost_display]] = NATURE_BOOST
    nature[display_to_key[nerf_display]] = NATURE_NERF
    return nature

# -------------------- 个体值同步函数 --------------------
def label_to_iv_key(prefix, label):
    mapping = {
        "❤️ HP": "hp", "⚔️ 物攻": "atk", "🛡️ 物防": "def",
        "🔮 魔攻": "spa", "✨ 魔防": "spd", "💨 速度": "spe"
    }
    return f"{prefix}_iv_{mapping[label]}"

def sync_iv_values(prefix):
    selected = st.session_state[f"{prefix}_selected_ivs"]
    for label in STAT_LABELS.values():
        key = label_to_iv_key(prefix, label)
        if label not in selected:
            st.session_state[key] = 0
        else:
            # 如果之前是0，则恢复为默认值60
            if st.session_state[key] == 0:
                st.session_state[key] = DEFAULT_IV

# -------------------- 一键交换函数 --------------------
def swap_sides():
    # 精灵名称
    st.session_state.att_name, st.session_state.def_name = st.session_state.def_name, st.session_state.att_name
    # 等级
    st.session_state.att_level, st.session_state.def_level = st.session_state.def_level, st.session_state.att_level
    # 个体勾选列表
    st.session_state.att_selected_ivs, st.session_state.def_selected_ivs = st.session_state.def_selected_ivs, st.session_state.att_selected_ivs
    # 个体值
    for label in STAT_LABELS.values():
        att_key = label_to_iv_key("att", label)
        def_key = label_to_iv_key("def", label)
        st.session_state[att_key], st.session_state[def_key] = st.session_state[def_key], st.session_state[att_key]
    # 性格
    st.session_state.att_boost_stat, st.session_state.def_boost_stat = st.session_state.def_boost_stat, st.session_state.att_boost_stat
    st.session_state.att_nerf_stat, st.session_state.def_nerf_stat = st.session_state.def_nerf_stat, st.session_state.att_nerf_stat

# -------------------- 三列布局 --------------------
left_col, mid_col, right_col = st.columns([2, 2, 2], gap="medium")

# ==================== 左侧：攻击方 ====================
with left_col:
    st.header("⚔️ 攻击方")
    attacker_name = st.selectbox(
        "选择精灵", all_pokemon,
        index=all_pokemon.index(st.session_state.att_name) if st.session_state.att_name in all_pokemon else 0,
        key="att_name"
    )
    attacker_stats = get_pokemon_stats(attacker_name)

    attack_type = st.radio(
        "攻击类型",
        ["⚔️ 物理攻击", "🔮 魔法攻击"],
        horizontal=True,
        key="attack_type"
    )

    with st.expander("⚙️ 参数设置", expanded=True):
        st.number_input("等级", 1, 100, key="att_level")

        st.caption("✨ 个体值 (勾选三项有效，未勾选为0)")
        selected_ivs = st.multiselect(
            "选择三项有效个体值",
            options=list(STAT_LABELS.values()),
            default=st.session_state.att_selected_ivs,
            max_selections=3,
            key="att_selected_ivs",
            on_change=sync_iv_values,
            args=("att",),
            label_visibility="collapsed"
        )

        iv_cols = st.columns(3)
        for i, label in enumerate(STAT_LABELS.values()):
            key = label_to_iv_key("att", label)
            with iv_cols[i % 3]:
                if label in selected_ivs:
                    # 确保当前值在选项中（如果之前被置0后又勾选，则恢复默认60）
                    current_val = st.session_state[key]
                    if current_val not in IV_OPTIONS:
                        current_val = DEFAULT_IV
                        st.session_state[key] = DEFAULT_IV
                    st.selectbox(
                        label,
                        options=IV_OPTIONS,
                        key=key,
                        index=IV_OPTIONS.index(current_val) if current_val in IV_OPTIONS else 4,
                        label_visibility="collapsed",
                        placeholder=label
                    )
                else:
                    st.text_input(
                        label,
                        value="0",
                        disabled=True,
                        key=f"{key}_disabled",
                        label_visibility="collapsed",
                        placeholder=label
                    )

        st.caption("🌀 性格修正 (一项1.2，一项0.9，其余1.0)")
        stat_choices = list(STAT_LABELS.values())
        col_boost, col_nerf = st.columns(2)
        with col_boost:
            st.selectbox(
                "增幅能力", stat_choices,
                index=stat_choices.index(st.session_state.att_boost_stat) if st.session_state.att_boost_stat in stat_choices else 1,
                key="att_boost_stat"
            )
        with col_nerf:
            st.selectbox(
                "减幅能力", stat_choices,
                index=stat_choices.index(st.session_state.att_nerf_stat) if st.session_state.att_nerf_stat in stat_choices else 3,
                key="att_nerf_stat"
            )
        if st.session_state.att_boost_stat == st.session_state.att_nerf_stat:
            st.warning("增幅与减幅不能相同，当前性格修正无效")

    att_nature = build_nature_dict(st.session_state.att_boost_stat, st.session_state.att_nerf_stat)
    if attacker_stats:
        if attack_type == "⚔️ 物理攻击":
            base_attack = attacker_stats["attack"]
            iv_key = "att_iv_atk"
            nature_key = "attack"
        else:
            base_attack = attacker_stats["sp_atk"]
            iv_key = "att_iv_spa"
            nature_key = "sp_atk"
        attacker_attack = get_stat(
            base_attack,
            st.session_state[iv_key],
            st.session_state.att_level,
            att_nature[nature_key]
        )
        st.metric("💥 攻击力", attacker_attack)
    else:
        attacker_attack = 100
        st.warning("未找到该精灵数据")

# ==================== 右侧：防御方 ====================
with right_col:
    st.header("🛡️ 防御方")
    defender_name = st.selectbox(
        "选择精灵", all_pokemon,
        index=all_pokemon.index(st.session_state.def_name) if st.session_state.def_name in all_pokemon else 0,
        key="def_name"
    )
    defender_stats = get_pokemon_stats(defender_name)

    defense_type = "物防" if attack_type == "⚔️ 物理攻击" else "魔防"
    st.caption(f"防御类型：**{defense_type}**")

    with st.expander("⚙️ 参数设置", expanded=True):
        st.number_input("等级", 1, 100, key="def_level")

        st.caption("✨ 个体值 (勾选三项有效，未勾选为0)")
        selected_ivs_def = st.multiselect(
            "选择三项有效个体值",
            options=list(STAT_LABELS.values()),
            default=st.session_state.def_selected_ivs,
            max_selections=3,
            key="def_selected_ivs",
            on_change=sync_iv_values,
            args=("def",),
            label_visibility="collapsed"
        )

        iv_cols_def = st.columns(3)
        for i, label in enumerate(STAT_LABELS.values()):
            key = label_to_iv_key("def", label)
            with iv_cols_def[i % 3]:
                if label in selected_ivs_def:
                    current_val = st.session_state[key]
                    if current_val not in IV_OPTIONS:
                        current_val = DEFAULT_IV
                        st.session_state[key] = DEFAULT_IV
                    st.selectbox(
                        label,
                        options=IV_OPTIONS,
                        key=key,
                        index=IV_OPTIONS.index(current_val) if current_val in IV_OPTIONS else 4,
                        label_visibility="collapsed",
                        placeholder=label
                    )
                else:
                    st.text_input(
                        label,
                        value="0",
                        disabled=True,
                        key=f"{key}_disabled",
                        label_visibility="collapsed",
                        placeholder=label
                    )

        st.caption("🌀 性格修正 (一项1.2，一项0.9，其余1.0)")
        col_boost_def, col_nerf_def = st.columns(2)
        with col_boost_def:
            st.selectbox(
                "增幅能力", stat_choices,
                index=stat_choices.index(st.session_state.def_boost_stat) if st.session_state.def_boost_stat in stat_choices else 2,
                key="def_boost_stat"
            )
        with col_nerf_def:
            st.selectbox(
                "减幅能力", stat_choices,
                index=stat_choices.index(st.session_state.def_nerf_stat) if st.session_state.def_nerf_stat in stat_choices else 3,
                key="def_nerf_stat"
            )
        if st.session_state.def_boost_stat == st.session_state.def_nerf_stat:
            st.warning("增幅与减幅不能相同，当前性格修正无效")

    def_nature = build_nature_dict(st.session_state.def_boost_stat, st.session_state.def_nerf_stat)
    if defender_stats:
        if attack_type == "⚔️ 物理攻击":
            base_defense = defender_stats["defense"]
            iv_key = "def_iv_def"
            nature_key = "defense"
        else:
            base_defense = defender_stats["sp_def"]
            iv_key = "def_iv_spd"
            nature_key = "sp_def"
        defender_defense = get_stat(
            base_defense,
            st.session_state[iv_key],
            st.session_state.def_level,
            def_nature[nature_key]
        )
        st.metric("🛡️ 防御力", defender_defense)

        defender_hp = get_hp(
            defender_stats["hp"],
            st.session_state.def_iv_hp,
            st.session_state.def_level,
            def_nature["hp"]
        )
    else:
        defender_defense = 100
        defender_hp = 300
        st.warning("未找到该精灵数据")

# ==================== 中间：技能 & 伤害 ====================
with mid_col:
    st.header("✨ 技能 & 伤害")

    st.button("🔄 一键交换攻防位置", on_click=swap_sides, use_container_width=True)

    power = st.number_input("技能威力", min_value=1, value=80, step=5)

    col1, col2 = st.columns(2)
    with col1:
        stab = st.checkbox("本系加成 (×1.25)", value=True)
        stab_multiplier = 1.25 if stab else 1.0
    with col2:
        type_multiplier = st.selectbox(
            "属性克制",
            options=[0.25, 0.5, 1.0, 2.0, 3.0],
            index=2,
            format_func=lambda x: f"×{x}"
        )

    col3, col4 = st.columns(2)
    with col3:
        ability_multiplier = st.number_input("特性加成", 0.0, 3.0, 1.0, 0.1, format="%.2f")
    with col4:
        other_multiplier = st.number_input("其他加成", 0.0, 3.0, 1.0, 0.1, format="%.2f")

    damage = calculate_damage(
        attack_stat=attacker_attack,
        defense_stat=defender_defense,
        power=power,
        stab=stab_multiplier,
        type_multiplier=type_multiplier,
        ability_multiplier=ability_multiplier,
        other_multiplier=other_multiplier,
        base_factor=0.9
    )

    st.markdown("---")
    st.subheader("💥 单次伤害")
    st.metric("伤害值", damage)

    if damage > 0:
        hits_needed = (defender_hp + damage - 1) // damage
        st.metric("⚔️ 击杀所需次数", f"{hits_needed} 次")
        st.caption(f"（防御方生命值：{defender_hp}）")
    else:
        st.metric("⚔️ 击杀所需次数", "∞")

    with st.expander("📐 计算明细"):
        st.markdown(f"""
        - **攻击方**：{attacker_name} Lv.{st.session_state.att_level}，{attack_type}
        - 攻击力：{attacker_attack}
        - **防御方**：{defender_name} Lv.{st.session_state.def_level}，{defense_type}
        - 防御力：{defender_defense}，生命值：{defender_hp}
        - 技能威力：{power}
        - 本系加成：×{stab_multiplier}
        - 属性克制：×{type_multiplier}
        - 特性加成：×{ability_multiplier}
        - 其他加成：×{other_multiplier}
        - 基础系数：×0.9
        - **单次伤害**：{damage}
        - **击杀次数**：{hits_needed if damage > 0 else '∞'}
        """)

st.caption("伤害至少为1，计算结果已向下取整。")