def calculate_hp_roco(base, iv, level, nature=1.0, growth=0):
    """
    生命值公式（四舍五入规则）：
    生命 = round(  round( (等级/25 + 1) * (种族值 + 个体值/2) / 2 ) + 等级 + 10 ） * 性格修正 ) + 成长值
    """
    part1 = level / 25 + 1
    iv_half = iv / 2
    inner_bracket = round((part1 * (base + iv_half)) / 2)
    before_nature = inner_bracket + level + 10
    after_nature = before_nature * nature
    return round(after_nature) + growth


def calculate_other_roco(base, iv, level, nature=1.0, growth=0):
    """
    其他能力值公式（四舍五入规则）：
    Stat = round(  round( (种族值 + 个体值/2) / 2 ) * (1 + 等级/50) + 10 ） * 性格修正 ) + 成长值
    """
    iv_half = iv / 2
    inner_bracket = (base + iv_half) / 2
    mid = round(inner_bracket * (1 + level / 50))
    before_nature = mid + 10
    after_nature = before_nature * nature
    return round(after_nature) + growth

def calculate_damage(
    attack_stat: float,
    defense_stat: float,
    power: float,
    stab: float = 1.0,
    type_multiplier: float = 1.0,
    ability_multiplier: float = 1.0,
    other_multiplier: float = 1.0,
    base_factor: float = 0.9
) -> int:
    """
    伤害计算公式：floor( (攻击/防御) * 威力 * 本系 * 属性克制 * 特性 * 其他 * 0.9 )
    """
    raw = (attack_stat / defense_stat) * power * stab * type_multiplier * ability_multiplier * other_multiplier * base_factor
    return max(1, int(raw))