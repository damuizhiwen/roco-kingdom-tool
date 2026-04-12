import streamlit as st

st.set_page_config(page_title="宝可梦能力值计算器")
st.title("🎮 宝可梦能力值计算器")

# --- 核心计算函数 ---
def calculate_hp(base, iv, ev, level):
    return ((2 * base) + iv + (ev // 4)) * level // 100 + level + 10

def calculate_other_stat(base, iv, ev, level, nature=1.0):
    return (((2 * base) + iv + (ev // 4)) * level // 100 + 5) * nature

# --- 界面布局：使用两列来组织内容 ---
col1, col2 = st.columns(2)

with col1:
    pokemon_name = st.selectbox("选择宝可梦", ["妙蛙种子", "小火龙", "杰尼龟"])
    level = st.slider("等级 (Lv.)", 1, 100, 50)

with col2:
    nature_dict = {"勤奋 (无修正)": 1.0, "固执 (+攻击, -特攻)": 1.1, "胆小 (+速度, -攻击)": 0.9}
    selected_nature = st.selectbox("选择性格", list(nature_dict.keys()))

# --- 模拟数据：在实际应用中，你需要从数据库或API中获取这些数据---
base_stats = {"hp": 45, "attack": 49, "defense": 49, "sp_atk": 65, "sp_def": 65, "speed": 45}
iv = {"hp": 31, "attack": 31, "defense": 31, "sp_atk": 31, "sp_def": 31, "speed": 31}
ev = {"hp": 0, "attack": 0, "defense": 0, "sp_atk": 0, "sp_def": 0, "speed": 0}

st.header(f"📊 {pokemon_name} 的能力值")

# 显示能力值表格
col1, col2 = st.columns(2)
with col1:
    st.metric("❤️ HP", calculate_hp(base_stats["hp"], iv["hp"], ev["hp"], level))
    st.metric("⚔️ 攻击", calculate_other_stat(base_stats["attack"], iv["attack"], ev["attack"], level, nature_dict[selected_nature]))
    st.metric("🛡️ 防御", calculate_other_stat(base_stats["defense"], iv["defense"], ev["defense"], level))

with col2:
    st.metric("🔮 特攻", calculate_other_stat(base_stats["sp_atk"], iv["sp_atk"], ev["sp_atk"], level, nature_dict[selected_nature]))
    st.metric("✨ 特防", calculate_other_stat(base_stats["sp_def"], iv["sp_def"], ev["sp_def"], level))
    st.metric("💨 速度", calculate_other_stat(base_stats["speed"], iv["speed"], ev["speed"], level, nature_dict[selected_nature]))