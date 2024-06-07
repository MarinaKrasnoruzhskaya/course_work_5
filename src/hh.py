import requests

from src.parser import Parser


class HH(Parser):
    """
    Класс для работы с API HeadHunter
    """
    def __init__(self):
        self.__url = 'https://api.hh.ru/'
        self.headers = {'User-Agent': 'HH-User-Agent'}

    @property
    def url(self):
        return self.__url

    def get_vacancies(self, id_employer: int) -> list[dict]:
        """ Метод возвращает список вакансий заданного работодателя"""
        params = {'page': 0, 'per_page': 100, 'area': 113, 'employer_id': id_employer,
                  'only_with_salary': True}
        data_vacancies = []
        page = 0
        while True:
            response = requests.get(f'{self.url}vacancies', headers=self.headers, params=params)

            if response.status_code == 200:
                vacancies = response.json()['items']
                data_vacancies.extend(vacancies)
                page += 1

            if page >= response.json().get('pages'):
                break

        return data_vacancies

    def get_vacancies_from_employers(self, employers: dict) -> list[dict]:
        """ Метод возвращает список вакансий всех работодателей"""
        data_vacancies_from_employers = []
        for id_employer in employers.values():
            data = self.get_vacancies(id_employer)
            data_vacancies_from_employers.extend(data)
        return data_vacancies_from_employers

    def get_employers(self, employers: dict) -> list[dict]:
        """Метод возвращает информацию о работодателях"""
        data_employers = []
        for name_employer, id_employer in employers.items():
            params = {'text': name_employer, 'page': 0, 'per_page': 1, 'id': id_employer}
            response = requests.get(f'{self.url}employers/{id_employer}', headers=self.headers, params=params)
            if response.status_code == 200:
                data = response.json()
                data_employers.append(data)

        return data_employers
