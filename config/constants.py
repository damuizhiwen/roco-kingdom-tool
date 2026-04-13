# 个体值显示名称与内部键名的映射
STAT_OPTIONS = {
    "❤️ 生命": "hp",
    "⚔️ 物攻": "atk",
    "🛡️ 物防": "def",
    "🔮 魔攻": "spa",
    "✨ 魔防": "spd",
    "💨 速度": "spe"
}

# 性格修正的能力显示名称与内部键名映射
DISPLAY_TO_KEY = {
    "❤️ 生命": "hp",
    "⚔️ 物攻": "attack",
    "🛡️ 物防": "defense",
    "🔮 魔攻": "sp_atk",
    "✨ 魔防": "sp_def",
    "💨 速度": "speed"
}

# 能力选择列表（用于下拉菜单）
STAT_CHOICES = list(DISPLAY_TO_KEY.keys())

# 成长值档位映射
GROWTH_OPTIONS_HP = [0, 20, 40, 60, 80, 100]
GROWTH_OPTIONS_OTHER = [0, 10, 20, 30, 40, 50]
GROWTH_MAPPING = dict(zip(GROWTH_OPTIONS_HP, GROWTH_OPTIONS_OTHER))