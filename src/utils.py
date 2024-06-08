import csv
import json
import os

from config import ROOT_DIR


def get_companies(name_file='companies.json') -> dict:
    """Функция возвращает информацию о работадателях из json-файла"""
    all_name_file = os.path.join(ROOT_DIR, "data", name_file)
    with open(all_name_file, encoding="utf-8") as json_file:
        return json.load(json_file)


def write_to_csv_file(data, name_file):
    all_name_file = os.path.join(ROOT_DIR, "data", name_file)
    with open(all_name_file, 'w', encoding="utf-8") as csv_file:
        csvwriter = csv.writer(csv_file)
        for row in data:
            csvwriter.writerow(row)
