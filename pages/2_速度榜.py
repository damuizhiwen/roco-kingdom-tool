# pages/2_速度榜.py

import streamlit as st
from collections import defaultdict
from data.loader import get_all_pokemon_names, get_pokemon_stats
from utils.formulas import calculate_other_roco

st.set_page_config(page_title="速度榜", page_icon="⚡", layout="centered")

st.title("⚡ 洛克王国 · 速度总榜")
st.caption("60级 · 成长值50 · 四种配置混合排名")

# -------------------- 常量 --------------------
LEVEL = 60
GROWTH = 50

# -------------------- 配置选项 --------------------
CONFIGS = [
    {"suffix": "极速", "nature": 1.2, "iv": 60},
    {"suffix": "满速", "nature": 1.0, "iv": 60},
    {"suffix": "平速", "nature": 1.0, "iv": 0},
    {"suffix": "慢速", "nature": 0.9, "iv": 0},
]

# -------------------- 计算所有精灵+配置的速度数据（缓存） --------------------
@st.cache_data
def compute_all_speed_entries():
    entries = []
    all_names = get_all_pokemon_names()
    
    for name in all_names:
        stats = get_pokemon_stats(name)
        if not stats:
            continue
        base_speed = stats.get("speed", 0)
        
        for cfg in CONFIGS:
            speed_val = calculate_other_roco(
                base_speed,
                iv=cfg["iv"],
                level=LEVEL,
                nature=cfg["nature"],
                growth=GROWTH
            )
            entries.append({
                "精灵": f"{name} · {cfg['suffix']}",
                "原始精灵": name,
                "配置": cfg["suffix"],
                "种族值": base_speed,
                "速度值": speed_val
            })
    
    entries.sort(key=lambda x: x["速度值"], reverse=True)
    return entries

all_entries = compute_all_speed_entries()

# -------------------- 筛选控件 --------------------
col1, col2 = st.columns(2)
with col1:
    show_configs = st.multiselect(
        "筛选配置类型",
        options=["极速", "满速", "平速", "慢速"],
        default=["极速", "满速", "平速", "慢速"]
    )
with col2:
    search_name = st.text_input("🔍 搜索精灵名称", placeholder="输入精灵名...")

# 应用筛选
filtered_entries = [
    e for e in all_entries
    if e["配置"] in show_configs and (search_name.lower() in e["原始精灵"].lower() if search_name else True)
]

# -------------------- 按速度值分组 --------------------
speed_groups = defaultdict(list)
for entry in filtered_entries:
    speed_groups[entry["速度值"]].append(entry["精灵"])

sorted_speeds = sorted(speed_groups.keys(), reverse=True)
total_tiers = len(speed_groups)

# -------------------- 界面显示：统计与滑动条 --------------------
st.subheader(f"🏆 速度总榜 (共 {len(filtered_entries)} 条记录)")

# 显示总档位数
st.caption(f"📊 当前共有 **{total_tiers}** 个速度档位（去重）")

# 显示前 N 个速度档位
top_n = st.slider(
    "显示前 N 个速度档位",
    min_value=10,
    max_value=max(10, total_tiers),
    value=min(30, total_tiers),
    step=5
)

display_speeds = sorted_speeds[:top_n]

# -------------------- 渐变背景色函数 --------------------
def get_gradient_color(value, min_val, max_val):
    """根据数值在最小最大值之间的比例返回绿→红渐变颜色"""
    if max_val == min_val:
        ratio = 0.5
    else:
        ratio = (value - min_val) / (max_val - min_val)
    r = int(255 * ratio)
    g = int(255 * (1 - ratio))
    b = 0
    return f"#{r:02x}{g:02x}{b:02x}"

# -------------------- 表格渲染（同速合并、渐变背景） --------------------
if display_speeds:
    max_speed = display_speeds[0]
    min_speed = display_speeds[-1]
    
    html_table = "<table style='width:100%; border-collapse:collapse;'>"
    html_table += "<tr><th style='text-align:left; padding:8px;'>速度值</th><th style='text-align:left; padding:8px;'>精灵配置</th></tr>"
    
    for spd in display_speeds:
        names = speed_groups[spd]
        names_str = "、".join(names)
        bg_color = get_gradient_color(spd, max_speed, min_speed)
        html_table += f"<tr style='border-bottom:1px solid #eee;'>"
        html_table += f"<td style='padding:8px; vertical-align:top; background-color: {bg_color};'><b>{spd}</b></td>"
        html_table += f"<td style='padding:8px;'>{names_str}</td>"
        html_table += "</tr>"
    
    html_table += "</table>"
    st.markdown(html_table, unsafe_allow_html=True)
else:
    st.info("没有符合筛选条件的数据")

# -------------------- 说明 --------------------
with st.expander("📖 配置说明"):
    st.markdown("""
    - **等级**：固定为 60 级
    - **成长值**：固定为 50
    - **极速**：性格 ×1.2，个体 60
    - **满速**：性格 ×1.0，个体 60
    - **平速**：性格 ×1.0，个体 0
    - **慢速**：性格 ×0.9，个体 0
    - 每只精灵的四种配置作为独立条目参与总排名，相同速度值的条目合并展示。
    - 速度值背景色从 **绿（高速）** 渐变至 **红（低速）**。
    """)

st.caption("数据来源：Biligame Wiki · 洛克王国精灵图鉴")