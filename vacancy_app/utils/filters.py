import re
from typing import List, Optional
from vacancy_app.models.vacancy import Vacancy


def filter_vacancies_by_keyword(vacancies: List[Vacancy], keywords: Optional[List[str]] = None) -> List[Vacancy]:
    """
    Фильтрует вакансии по наличию ключевых слов в названии или описании.
    """
    if not vacancies:
        return []

    if not keywords:
        return vacancies

    pattern = re.compile("|".join(map(re.escape, keywords)), flags=re.IGNORECASE)
    return [
        v for v in vacancies
        if pattern.search(v.title) or pattern.search(v.description)
    ]


def filter_vacancies_by_salary_range(
    vacancies: List[Vacancy],
    min_salary: Optional[int] = None,
    max_salary: Optional[int] = None
) -> List[Vacancy]:
    """
    Фильтрует вакансии по диапазону зарплат.
    """
    if not vacancies:
        return []

    result = []
    for v in vacancies:
        avg = v.average_salary()
        if min_salary is not None and avg < min_salary:
            continue
        if max_salary is not None and avg > max_salary:
            continue
        result.append(v)
    return result


def sort_vacancies_by_salary(vacancies: List[Vacancy], reverse: bool = True) -> List[Vacancy]:
    """
    Сортирует вакансии по средней зарплате.
    """
    if not vacancies:
        return []
    return sorted(vacancies, key=lambda v: v.average_salary(), reverse=reverse)

