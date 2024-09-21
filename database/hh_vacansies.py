import os

import psycopg2
import requests
from config import config

params_db = config()  # Параметры для подключения к BD

password = os.getenv('Pass_Postgres')  # Если подключение к БД без database.ini.


class HH_api_db:

    """Класс для работы с API HH.ru и заполнение таблиц в BD"""

    # Список можно дополнить любыми компаниями.
    employers_dict = {'МегаФон': '3127',
                      'МТС': '3776',
                      'билайн': '4934',
                      'СБЕР': '3529',
                      'Банк ВТБ (ПАО)': '4181',
                      'Тинькофф': '78638',
                      'АШАН Ритейл Россия': '54979',
                      'ВкусВилл': '816144',
                      'Конфаэль, Компания': '1601',
                      'KFC (Интернэшнл Ресторант Брэндс)': '3093544'}

    def get_request(self, employer_id) -> dict:
        """Запрос списка работодателей, при наличии вакансий и заработной платы"""
        params = {
            "page": 1,
            "per_page": 100,
            "employer_id": employer_id,
            "only_with_salary": True,
            "area": 113,
            "only_with_vacancies": True
        }
        return requests.get("https://api.hh.ru/vacancies/", params=params).json()['items']

    def get_vacancies(self):
        """Получение списка работодателей"""
        vacancies_list = []
        for employer in self.employers_dict:
            emp_vacancies = self.get_request(self.employers_dict[employer])
            for vacancy in emp_vacancies:
                if vacancy['salary']['from'] is None:
                    salary = 0
                else:
                    salary = vacancy['salary']['from']
                vacancies_list.append(
                    {'url': vacancy['alternate_url'], 'salary': salary,
                     'vacancy_name': vacancy['name'], 'employer': employer})
        return vacancies_list

    def employers_to_db(self):
        """Сохранение работодателей в БД"""
        with psycopg2.connect(dbname='postgres', **params_db) as conn:
            with conn.cursor() as cur:
                for employer in self.employers_dict:
                    try:
                        cur.execute(f"INSERT INTO companies values ('{int(self.employers_dict[employer])}', '{employer}')")
                    except Exception:
                        pass
        conn.commit()
        conn.close()

    def vacancies_to_db(self):
        """Сохранение вакансий в БД"""
        with psycopg2.connect(dbname='postgres', **params_db) as conn:
            with conn.cursor() as cur:
                for vacancy in self.get_vacancies():
                    cur.execute(
                        f"INSERT INTO vacancies(vacancy_name, salary, company_name, vacancy_url) values "
                        f"('{vacancy['vacancy_name']}', '{int(vacancy['salary'])}', "
                        f"'{vacancy['employer']}', '{vacancy['url']}')")
        conn.commit()
        conn.close()
