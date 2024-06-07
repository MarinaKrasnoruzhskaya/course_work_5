from src.employer import Employer
from src.hh import HH
from src.utils import get_companies
from src.vacancy import Vacancy


def main():
    companies = get_companies()
    print("Привет! Для этих 10 работодателей:")
    print(*[name for name in companies.keys()], sep='\n')
    hh_api = HH()
    hh_employers = hh_api.get_employers(companies)
    print(hh_employers[2])
    employers_list = Employer.cast_to_object_list(hh_employers)
    print(employers_list[2])
    hh_vacancies = hh_api.get_vacancies_from_employers(companies)
    print(f'С hh.ru запросим вакансии, в которых указанна зарплата.\n'
          f'Прилетело: {len(hh_vacancies)} вакансий')
    print(len(hh_vacancies))

    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
    print(vacancies_list[0])


if __name__ == "__main__":
    main()
