import psycopg2

from config import config
from src.employer import Employer
from src.vacancy import Vacancy


class DBManager:
    """
    Класс для работы с БД
    """
    def __init__(self):
        self.__params = config()
        self.db_name = "hh"
        self.conn = psycopg2.connect(**self.__params)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def create_database(self):
        """ Метод для создания БД """
        self.cur.execute(f"DROP DATABASE IF EXISTS {self.db_name}")
        self.cur.execute(f"CREATE DATABASE {self.db_name}")

    def create_tables(self):
        """ Метод для создания таблиц"""
        conn = psycopg2.connect(dbname=self.db_name, **self.__params)
        with conn.cursor() as cur:
            cur.execute("""
                        CREATE TABLE employers (
                            employer_id VARCHAR(10) PRIMARY KEY,
                            name VARCHAR(255) NOT NULL,
                            employer_url TEXT,
                            open_vacancies INT
                        )
                    """)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE vacancies (
                    id SERIAL PRIMARY KEY,
                    vacancy_id VARCHAR(15),
                    name VARCHAR(255) NOT NULL,
                    vacancy_url TEXT,
                    published_at DATE,
                    salary_from INT,
                    salary_to INT,
                    employer_id VARCHAR(10) REFERENCES employers(employer_id)
                )
            """)
        conn.commit()
        conn.close()

    def save_employers_to_database(self, data: list[Employer]) -> None:
        """ Метод для сохранения данных о работодателях """
        conn = psycopg2.connect(dbname=self.db_name, **self.__params)
        with conn.cursor() as cur:
            for e in data:
                cur.execute("""
                INSERT INTO employers (employer_id, name, employer_url, open_vacancies) 
                VALUES (%s, %s, %s, %s)
                RETURNING *
                """,
                            (e.employer_id, e.name, e.url, e.open_vacancies)
                            )

        conn.commit()
        conn.close()

    def save_vacancies_to_database(self, data: list[Vacancy]) -> None:
        """ Метод для сохранения данных о вакансиях """
        conn = psycopg2.connect(dbname=self.db_name, **self.__params)
        with conn.cursor() as cur:
            for v in data:
                cur.execute("""
                INSERT INTO vacancies (vacancy_id, name, vacancy_url, published_at, salary_from, salary_to, employer_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING *
                """,
                            (v.id, v.name, v.url, v.published_at, v.salary['from'], v.salary['to'], v.employer_id)
                            )

        conn.commit()
        conn.close()

    def execute(self, query):
        """ Метод выполняет запрос и получает результат"""
        conn = psycopg2.connect(dbname=self.db_name, **self.__params)
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

        conn.commit()
        conn.close()

        return rows

    def get_companies_and_vacancies_count(self):
        """ Метод получает список всех компаний и количество вакансий у каждой компании"""
        query = f"""
            SELECT employers.name, COUNT(vacancy_id) as count_vacancies FROM employers
            FULL JOIN vacancies USING(employer_id)
            GROUP BY employers.name"""

        return self.execute(query)

    def get_all_vacancies(self):
        """ Метод получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты
        и ссылки на вакансию"""
        query = f"""SELECT employers.name, vacancies.name, salary_from, salary_to, vacancy_url FROM vacancies
        JOIN employers USING(employer_id)"""

        return self.execute(query)

    def get_avg_salary(self):
        """ Метод получает среднюю зарплату по вакансиям"""
        query = f"""SELECT avg(salary) FROM
        (SELECT vacancies.name as name, salary_from, salary_to, (salary_from + salary_to)/2 as salary 
        FROM vacancies
        WHERE salary_from != 0 and salary_to != 0
        UNION
        SELECT vacancies.name as name, salary_from, salary_to, salary_from as salary FROM vacancies
        WHERE salary_from != 0 and salary_to = 0
        UNION
        SELECT vacancies.name as name, salary_from, salary_to, salary_to as salary FROM vacancies
        WHERE salary_from = 0 and salary_to != 0)"""

        return self.execute(query)

    def get_vacancies_with_higher_salary(self, avg_salary):
        """Метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям """
        query =f"""SELECT name, salary FROM
        (SELECT vacancies.name as name, salary_from, salary_to, (salary_from + salary_to)/2 as salary FROM vacancies
        WHERE salary_from != 0 and salary_to != 0
        UNION
        SELECT vacancies.name as name, salary_from, salary_to, salary_from as salary FROM vacancies
        WHERE salary_from != 0 and salary_to = 0
        UNION
        SELECT vacancies.name as name, salary_from, salary_to, salary_to as salary FROM vacancies
        WHERE salary_from = 0 and salary_to != 0)
        WHERE salary > {avg_salary}"""

        return self.execute(query)

    def get_vacancies_with_keyword(self, key_word):
        """ Метод получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        query = f"""select * from vacancies 
        WHERE name LIKE '%{key_word}%' OR name LIKE  '%{key_word.title()}%'"""

        return self.execute(query)
