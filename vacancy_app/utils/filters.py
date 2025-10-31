import re
from typing import List, Optional
from vacancy_app.models.vacancy import Vacancy


def filter_vacancies_by_keyword(vacancies: List[Vacancy], keywords: List[str]) -> List[Vacancy]:
    if not keywords:
        return vacancies
    pattern = re.compile("|".join(map(re.escape, keywords)), flags=re.IGNORECASE)
    return [v for v in vacancies if pattern.search(v.title) or pattern.search(v.description)]


def filter_vacancies_by_salary_range(vacancies: List[Vacancy], min_salary: Optional[int], max_salary: Optional[int]) -> List[Vacancy]:
    result = []
    for v in vacancies:
        avg = v.average_salary()
        if min_salary and avg < min_salary:
            continue
        if max_salary and avg > max_salary:
            continue
        result.append(v)
    return result


def sort_vacancies_by_salary(vacancies: List[Vacancy], reverse: bool = True) -> List[Vacancy]:
    return sorted(vacancies, key=lambda v: v.average_salary(), reverse=reverse)
