-- Создание таблицы companies
CREATE TABLE companies (
            company_id int primary key,
            company_name varchar unique not null
            )

-- Создание таблицы vacancies
CREATE TABLE vacancies (
                vacancy_id serial primary key,
                vacancy_name text not null,
                salary int,
                company_name text not null,
                vacancy_url varchar not null
                )

-- Связь между таблицами по внешнему ключу company_name
alter table vacancies add constraint fk_company_name foreign key(company_name) references companies(company_name)

-- Посмотреть всю таблицу vacancies
select * from vacancies

-- Показать среднюю зарплату в таблице vacancies
select avg(salary) from vacancies

-- получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
select vacancy_name from vacancies where salary > (select avg(salary) from vacancies)

-- получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”
select vacancy_name from vacancies where vacancy_name like '%{keyword}%'
select vacancy_name from vacancies where vacancy_name like '%python%'
