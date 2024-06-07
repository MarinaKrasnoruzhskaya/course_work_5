from abc import ABC, abstractmethod


class Parser(ABC):
    """
    Абстрактный класс для работы с API сервиса с вакансиями
    """
    @abstractmethod
    def get_vacancies(self, *args, **kwargs):
        pass
