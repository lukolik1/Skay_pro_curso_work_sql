import psycopg2


def create_database(database_name, params):
    """Создание базы данных."""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()
    try:
        cur.execute(f'DROP DATABASE {database_name}')
    except psycopg2.errors.InvalidCatalogName:
        print('База данных не существует')

    cur.execute(f'CREATE DATABASE {database_name}')

    cur.close()
    conn.close()


def create_table(params):
    """Создание таблиц companies и vacancies в созданной базе данных - HH_vacancy"""

    conn = psycopg2.connect(dbname='postgres', **params)
    with conn.cursor() as cur:
        try:
            cur.execute("""
                CREATE TABLE companies (
                company_id int primary key,
                company_name varchar unique not null
             )
                """)
        except psycopg2.errors.DuplicateTable:
            print('Таблица уже существует')

    with conn.cursor() as cur:
        try:
            cur.execute("""
                CREATE TABLE vacancies (
                    vacancy_id serial primary key,
                    vacancy_name text not null,
                    salary int,
                    company_name text not null,
                    vacancy_url varchar not null
                    )
                    """)
        except Exception:
            print('Таблица уже существует')
    with conn.cursor() as cur:
        try:
            cur.execute("""alter table vacancies add constraint fk_company_name 
            foreign key(company_name) references companies(company_name)""")
        except Exception:
            print('Таблица уже существует')

    conn.commit()
    conn.close()
    