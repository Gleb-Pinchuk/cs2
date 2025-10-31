from vacancy_app.api.hh_api import HeadHunterAPI
from vacancy_app.models.vacancy import Vacancy
from vacancy_app.storage.json_saver import JSONSaver
from vacancy_app.utils.filters import (
    filter_vacancies_by_keyword,
    sort_vacancies_by_salary,
    filter_vacancies_by_salary_range,
)


def user_interaction():
    print("=== Поиск вакансий hh.ru ===")
    api = HeadHunterAPI()
    saver = JSONSaver()

    while True:
        print("\n1. Загрузить вакансии с hh.ru")
        print("2. Показать сохранённые вакансии")
        print("3. Топ N по зарплате")
        print("4. Фильтр по ключевым словам")
        print("5. Фильтр по диапазону зарплат")
        print("6. Удалить вакансию")
        print("7. Выход")

        choice = input("Выберите действие: ").strip()
        if choice == "1":
            query = input("Введите запрос: ").strip()
            raw = api.get_vacancies(query)
            vacancies = Vacancy.cast_to_object_list(raw)
            for v in vacancies:
                saver.add_vacancy(v)
            print(f"Сохранено {len(vacancies)} вакансий.")
        elif choice == "2":
            for v in saver.get_vacancies():
                print(f"{v.title} | {v.average_salary():.0f} {v.currency or ''} | {v.url}")
        elif choice == "3":
            n = int(input("Введите N: "))
            vacs = saver.get_vacancies()
            for v in sort_vacancies_by_salary(vacs)[:n]:
                print(f"{v.title} | {v.average_salary():.0f} {v.currency or ''} | {v.url}")
        elif choice == "4":
            kw = input("Введите ключевые слова: ").split()
            vacs = saver.get_vacancies()
            filtered = filter_vacancies_by_keyword(vacs, kw)
            for v in filtered:
                print(f"{v.title} | {v.url}")
        elif choice == "5":
            min_s = input("Мин. зарплата: ")
            max_s = input("Макс. зарплата: ")
            min_val = int(min_s) if min_s else None
            max_val = int(max_s) if max_s else None
            vacs = saver.get_vacancies()
            filtered = filter_vacancies_by_salary_range(vacs, min_val, max_val)
            for v in filtered:
                print(f"{v.title} | {v.average_salary():.0f} {v.currency or ''} | {v.url}")
        elif choice == "6":
            ident = input("Введите URL или название для удаления: ").strip()
            print("Удалено." if saver.delete_vacancy(ident) else "Не найдено.")
        elif choice == "7":
            break
        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    user_interaction()
