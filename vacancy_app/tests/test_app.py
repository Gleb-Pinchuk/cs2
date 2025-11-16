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


def test_filter_by_keyword_case_insensitive(sample_vacancies):
    res = filter_vacancies_by_keyword(sample_vacancies, ["PYTHON"])
    assert len(res) == 1
    assert res[0].title == "Python Dev"


def test_filter_by_keyword_no_matches(sample_vacancies):
    res = filter_vacancies_by_keyword(sample_vacancies, ["golang"])
    assert res == []


def test_filter_by_salary_range(sample_vacancies):
    res = filter_vacancies_by_salary_range(sample_vacancies, 90000, 130000)
    assert all(90000 <= v.average_salary() <= 130000 for v in res)
    assert any("Python" in v.title for v in res)


def test_filter_salary_range_empty(sample_vacancies):
    res = filter_vacancies_by_salary_range(sample_vacancies, 10, 20)
    assert res == []


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

    saver.add_vacancy(sample_vacancies[0])
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

    saver.add_vacancy(sample_vacancies[0])

    assert saver.delete_vacancy("url1") is True
    assert saver.get_vacancies() == []


def test_json_saver_delete_nonexistent(tmp_path):
    file_path = tmp_path / "vacancies.json"
    saver = JSONSaver(str(file_path))
    assert saver.delete_vacancy("not_exist") is False


def test_vacancy_average_salary():
    v = Vacancy("Test", "url", "desc", salary_from=100, salary_to=200)
    assert v.average_salary() == 150


def test_vacancy_average_salary_only_from():
    v = Vacancy("Test", "url", "desc", salary_from=100)
    assert v.average_salary() == 100


def test_vacancy_average_salary_only_to():
    v = Vacancy("Test", "url", "desc", salary_to=200)
    assert v.average_salary() == 200


def test_vacancy_validation_negative_salary():
    with pytest.raises(ValueError):
        Vacancy("Bad", "url", "desc", salary_from=-10)


def test_vacancy_str_representation():
    v = Vacancy("Python Dev", "url1", "desc", 100000, 150000, "RUR")
    assert "Python Dev" in str(v)
    assert "url1" in str(v)
    assert "100000" in str(v)


def test_vacancy_comparison(sample_vacancies):
    assert sample_vacancies[0] > sample_vacancies[1]
    assert sample_vacancies[1] < sample_vacancies[2]
