import pytest
from vacancy_app.models.vacancy import Vacancy
from vacancy_app.utils.filters import (
    filter_vacancies_by_keyword,
    filter_vacancies_by_salary_range,
    sort_vacancies_by_salary,
)
from vacancy_app.storage.json_saver import JSONSaver


@pytest.fixture
def sample_vacancies():
    """Создаёт набор тестовых вакансий."""
    return [
        Vacancy("Python Dev", "url1", "desc python", salary_from=100000, salary_to=150000, currency="RUR"),
        Vacancy("QA Engineer", "url2", "testing job", salary_from=50000, salary_to=70000, currency="RUR"),
        Vacancy("Java Developer", "url3", "Spring", salary_from=120000, salary_to=140000, currency="RUR"),
    ]


def test_filter_by_keyword(sample_vacancies):
    res = filter_vacancies_by_keyword(sample_vacancies, ["python"])
    assert len(res) == 1
    assert res[0].title == "Python Dev"


def test_filter_by_keyword_empty(sample_vacancies):
    res = filter_vacancies_by_keyword(sample_vacancies, [])
    assert len(res) == len(sample_vacancies)


def test_filter_by_salary_range(sample_vacancies):
    res = filter_vacancies_by_salary_range(sample_vacancies, 90000, 130000)
    assert all(90000 <= v.average_salary() <= 130000 for v in res)
    assert any("Python" in v.title for v in res)


def test_sort_vacancies_by_salary(sample_vacancies):
    sorted_v = sort_vacancies_by_salary(sample_vacancies)
    assert sorted_v[0].average_salary() >= sorted_v[-1].average_salary()
    assert sorted_v[0].title == "Python Dev"


def test_sort_vacancies_by_salary_reverse_false(sample_vacancies):
    sorted_v = sort_vacancies_by_salary(sample_vacancies, reverse=False)
    assert sorted_v[0].average_salary() <= sorted_v[-1].average_salary()
    assert sorted_v[-1].title == "Python Dev"


def test_json_saver_add_and_get(tmp_path, sample_vacancies):
    file_path = tmp_path / "vacancies.json"
    saver = JSONSaver(str(file_path))

    v = sample_vacancies[0]
    saver.add_vacancy(v)

    all_vacancies = saver.get_vacancies()
    assert len(all_vacancies) == 1
    assert all_vacancies[0].title == "Python Dev"


def test_json_saver_prevent_duplicate(tmp_path, sample_vacancies):
    file_path = tmp_path / "vacancies.json"
    saver = JSONSaver(str(file_path))

    v = sample_vacancies[0]
    saver.add_vacancy(v)
    saver.add_vacancy(v)

    all_vacancies = saver.get_vacancies()
    assert len(all_vacancies) == 1


def test_json_saver_delete_by_url(tmp_path, sample_vacancies):
    file_path = tmp_path / "vacancies.json"
    saver = JSONSaver(str(file_path))

    v = sample_vacancies[0]
    saver.add_vacancy(v)

    assert saver.delete_vacancy("url1") is True
    assert saver.get_vacancies() == []


def test_json_saver_delete_nonexistent(tmp_path):
    file_path = tmp_path / "vacancies.json"
    saver = JSONSaver(str(file_path))
    assert saver.delete_vacancy("not_exist") is False
