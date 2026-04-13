# components/main_display.py

import streamlit as st
from utils.formulas import calculate_hp_roco, calculate_other_roco
from utils.helpers import get_nature_modifier


def render_main_display(params):
    """根据参数字典渲染主界面能力值展示"""
    st.header("📋 当前能力值计算结果")

    # 解包参数
    level = params["level"]
    base_hp, base_atk, base_def = params["base_hp"], params["base_atk"], params["base_def"]
    base_spa, base_spd, base_spe = params["base_spa"], params["base_spd"], params["base_spe"]
    iv_hp, iv_atk, iv_def = params["iv_hp"], params["iv_atk"], params["iv_def"]
    iv_spa, iv_spd, iv_spe = params["iv_spa"], params["iv_spd"], params["iv_spe"]
    nature_info = params["nature_info"]
    growth_hp, growth_other = params["growth_hp"], params["growth_other"]

    # 计算六项能力值
    hp_mod = get_nature_modifier("hp", nature_info)
    hp_val = calculate_hp_roco(base_hp, iv_hp, level, hp_mod, growth_hp)

    atk_mod = get_nature_modifier("attack", nature_info)
    atk_val = calculate_other_roco(base_atk, iv_atk, level, atk_mod, growth_other)

    def_mod = get_nature_modifier("defense", nature_info)
    def_val = calculate_other_roco(base_def, iv_def, level, def_mod, growth_other)

    spa_mod = get_nature_modifier("sp_atk", nature_info)
    spa_val = calculate_other_roco(base_spa, iv_spa, level, spa_mod, growth_other)

    spd_mod = get_nature_modifier("sp_def", nature_info)
    spd_val = calculate_other_roco(base_spd, iv_spd, level, spd_mod, growth_other)

    spe_mod = get_nature_modifier("speed", nature_info)
    spe_val = calculate_other_roco(base_spe, iv_spe, level, spe_mod, growth_other)

    # -------------------- 能力值展示（标签与数值平行居中）--------------------
    st.markdown(
        f"""
        <style>
            .stat-row {{
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 12px 0;
            }}
            .stat-label {{
                font-size: 22px;
                font-weight: 500;
                margin-right: 20px;
                min-width: 100px;
                text-align: right;
            }}
            .stat-value {{
                font-size: 32px;
                font-weight: bold;
                color: #1f77b4;
                min-width: 70px;
                text-align: left;
            }}
            .stats-container {{
                display: flex;
                justify-content: center;
                gap: 60px;
                margin-top: 20px;
                margin-bottom: 20px;
            }}
        </style>
        <div class="stats-container">
            <div>
                <div class="stat-row"><span class="stat-label">❤️ 生命</span><span class="stat-value">{hp_val}</span></div>
                <div class="stat-row"><span class="stat-label">⚔️ 物攻</span><span class="stat-value">{atk_val}</span></div>
                <div class="stat-row"><span class="stat-label">🛡️ 物防</span><span class="stat-value">{def_val}</span></div>
            </div>
            <div>
                <div class="stat-row"><span class="stat-label">🔮 魔攻</span><span class="stat-value">{spa_val}</span></div>
                <div class="stat-row"><span class="stat-label">✨ 魔防</span><span class="stat-value">{spd_val}</span></div>
                <div class="stat-row"><span class="stat-label">💨 速度</span><span class="stat-value">{spe_val}</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # -------------------- 致谢栏 --------------------
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #888; font-size: 14px; padding: 20px 0;'>
            🙏 致谢<br>
            能力值计算公式来源：
            <a href='https://www.bilibili.com/opus/1190129562213679105#reply298637760656' target='_blank' style='color: #aaa; text-decoration: none;'>
                B站专栏 · 洛克王国能力值计算
            </a><br>
            精灵图鉴数据来源：
            <a href='https://wiki.biligame.com/rocom/%E7%B2%BE%E7%81%B5%E5%9B%BE%E9%89%B4' target='_blank' style='color: #aaa; text-decoration: none;'>
                Biligame Wiki · 洛克王国精灵图鉴
            </a><br>
            <span style='font-size: 12px;'>—— 本工具仅供学习交流，数据更新于 2026.04 ——</span>
        </div>
        """,
        unsafe_allow_html=True
    )