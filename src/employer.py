class Employer:
    """
    Класс для работы с работодателями
    """
    def __init__(self, employer_id: str, name: str, url: str, open_vacancies: int):
        self.employer_id = employer_id
        self.name = name
        self.url = url
        self.open_vacancies = open_vacancies

    def __str__(self):
        return (
            f"ID: {self.employer_id}\n"
            f"Наименование: {self.name}\n"
            f"URL: {self.url}\n"
            f"Открытых вакансий: {self.open_vacancies}"
        )

    @classmethod
    def create_object(cls, *args, **kwargs):
        """ Метод для альтернативного способа создания объекта"""
        return cls(*args, **kwargs)

    @classmethod
    def cast_to_object_list(cls, list_employers_json: list) -> list:
        """ Метод для преобразования набора данных из JSON в список объектов"""
        list_employers = []
        for e in list_employers_json:
            employer = cls.create_object(
                e['id'],
                e['name'],
                e['alternate_url'],
                e['open_vacancies'],
            )

            list_employers.append(employer)
        return list_employers
