from src.hh import HH
from src.utils import get_companies


def main():
    companies = get_companies()
    hh_api = HH()
    hh_employers = hh_api.get_employers(companies)
    print(hh_employers[2])
    hh_vacancies = hh_api.get_vacancies_from_employers(companies)
    print(len(hh_vacancies))


if __name__ == "__main__":
    main()
