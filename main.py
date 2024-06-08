from decimal import Decimal

from src.db_manager import DBManager
from src.employer import Employer
from src.hh import HH
from src.utils import get_companies, write_to_csv_file
from src.vacancy import Vacancy


def main():
    companies = get_companies()

    print("Привет! Для этих 10 работодателей:\n")
    print(*[name for name in companies.keys()], sep=', ')
    print(f'\nс hh.ru запросим вакансии, в которых указана зарплата.')

    hh_api = HH()
    hh_employers = hh_api.get_employers(companies)
    employers_list = Employer.cast_to_object_list(hh_employers)
    hh_vacancies = hh_api.get_vacancies_from_employers(companies)
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)

    print(f'\nПолучено: {len(hh_vacancies)} вакансий')

    db_hh = DBManager()
    db_hh.create_database()
    db_hh.create_tables()
    db_hh.save_employers_to_database(employers_list)
    db_hh.save_vacancies_to_database(vacancies_list)

    rows = db_hh.get_companies_and_vacancies_count()
    print('\nСписок всех компаний и количество вакансий у каждой компании:')
    for row in rows:
        print(f"{row[0]}: {row[1]}")

    rows = db_hh.get_all_vacancies()
    print(f'\nСписок всех {len(rows)} вакансий записан в файл all_vacancies.csv')
    write_to_csv_file(rows, 'all_vacancies.csv')

    rows = db_hh.get_avg_salary()
    avg_salary = rows[0][0].quantize(Decimal("1.00"))
    print(f'\nCредняя зарплата по вакансиям: {avg_salary} RUR')

    rows = db_hh.get_vacancies_with_higher_salary(avg_salary)
    print(f'\nСписок всех {len(rows)} вакансий, у которых зарплата выше средней по всем вакансиям, записан в файл '
          f'avg_vacancies.csv')
    write_to_csv_file(rows, 'avg_vacancies.csv')

    key_word = input('\nВведите ключевое слово для поиска в вакансиях: ').strip().lower()
    rows = db_hh.get_vacancies_with_keyword(key_word)
    if rows:
        print(f'Список всех {len(rows)} вакансий, в названии которых содержится ключевое слово, записан в файл '
              f'keyword_vacancies.csv')
        write_to_csv_file(rows, 'keyword_vacancies.csv')
    else:
        print('Поиск не дал результата')


if __name__ == "__main__":
    main()
