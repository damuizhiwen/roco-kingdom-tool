# data/loader.py

import json
import os

# 获取当前文件所在目录的绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "sprites_stats.json")

# 加载 JSON 数据
with open(JSON_PATH, "r", encoding="utf-8") as f:
    POKEMON_BASE_STATS = json.load(f)


def get_all_pokemon_names():
    """返回所有精灵名称列表（按字母/拼音排序）"""
    return sorted(POKEMON_BASE_STATS.keys())


def get_pokemon_stats(name):
    """
    根据精灵名称获取种族值字典。
    若不存在则返回 None。
    """
    return POKEMON_BASE_STATS.get(name)


def search_pokemon(keyword):
    """
    根据关键词模糊搜索精灵名称（不区分大小写）。
    返回匹配的名称列表。
    """
    keyword = keyword.lower()
    return [name for name in POKEMON_BASE_STATS if keyword in name.lower()]