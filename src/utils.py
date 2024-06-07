import json
import os

from config import ROOT_DIR


def get_companies(name_file='companies.json') -> dict:
    """Функция возвращает информацию о работадателях из json-файла"""
    all_name_file = os.path.join(ROOT_DIR, "data", name_file)
    with open(all_name_file, encoding="utf-8") as json_file:
        return json.load(json_file)