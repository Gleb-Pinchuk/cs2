from vacancy_app.models.vacancy import Vacancy
from vacancy_app.utils.filters import filter_vacancies_by_keyword, sort_vacancies_by_salary
from vacancy_app.storage.json_saver import JSONSaver


def sample_vacancies():
    return [
        Vacancy("Python Dev", "url1", "desc python", salary_from=100000, salary_to=150000, currency="RUR"),
        Vacancy("QA", "url2", "testing job", salary_from=50000, salary_to=70000, currency="RUR"),
    ]


def test_filter_by_keyword():
    v = sample_vacancies()
    res = filter_vacancies_by_keyword(v, ["python"])
    assert len(res) == 1 and res[0].title == "Python Dev"


def test_sorting():
    v = sample_vacancies()
    sorted_v = sort_vacancies_by_salary(v)
    assert sorted_v[0].title == "Python Dev"


def test_json_saver(tmp_path):
    f = tmp_path / "vac.json"
    saver = JSONSaver(str(f))
    v = sample_vacancies()[0]
    saver.add_vacancy(v)
    allv = saver.get_vacancies()
    assert allv[0].title == "Python Dev"
    saver.delete_vacancy("url1")
    assert not saver.get_vacancies()
