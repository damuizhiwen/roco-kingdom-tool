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