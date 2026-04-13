def get_nature_modifier(stat_name, nature_info):
    """
    从 nature_info 字典或数值中提取指定能力的修正系数。
    """
    if isinstance(nature_info, dict):
        return nature_info.get(stat_name, 1.0)
    else:
        return nature_info