import psycopg2
from database.hh_vacansies import params_db


class DBManager:

    """Класс для работы с информацией из Базы Данных"""

    @staticmethod
    def get_companies_and_vacancies_count():
        """Получает список всех компаний и количество вакансий у каждой компании."""
        with psycopg2.connect(dbname='HH_vacancy', **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT company_name, COUNT(vacancy_name) from vacancies GROUP BY company_name')
                answer = cur.fetchall()
        conn.close()
        return answer

    @staticmethod
    def get_all_vacancies():
        """Получает список всех вакансий"""
        with psycopg2.connect(dbname='postgres', **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * from vacancies')
                answer = cur.fetchall()
        conn.close()
        return answer

    @staticmethod
    def get_avg_salary():
        """Получает среднюю зарплату по вакансиям"""
        with psycopg2.connect(dbname='postgres', **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT avg(salary) from vacancies')
                answer = cur.fetchall()
        conn.close()
        return answer

    @staticmethod
    def get_vacancies_with_higher_salary():
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        with psycopg2.connect(dbname='postgres', **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT vacancy_name from vacancies WHERE salary > (SELECT AVG(salary) from vacancies)')
                answer = cur.fetchall()
        conn.close()
        return answer

    @staticmethod
    def get_vacancies_with_keyword(keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        with psycopg2.connect(dbname='postgres', **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT vacancy_name from vacancies WHERE vacancy_name LIKE '%{keyword}%'")
                answer = cur.fetchall()
        conn.close()
        return answer
