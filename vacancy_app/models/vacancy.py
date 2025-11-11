from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class Vacancy:
    """
    Класс для представления вакансии.
    Поддерживает валидацию данных, методы сравнения по зарплате и преобразование данных из API hh.ru.
    """

    title: str
    url: str
    description: str
    employer: Optional[str] = None
    salary_from: Optional[int] = field(default=0)
    salary_to: Optional[int] = field(default=0)
    currency: Optional[str] = field(default=None)
    raw: Optional[Dict[str, Any]] = field(default=None, repr=False)

    def __post_init__(self):
        """Проводит валидацию и очистку данных после инициализации."""
        self.title = self._validate_str(self.title)
        self.url = self._validate_str(self.url)
        self.description = self._validate_str(self.description)
        self.employer = self._validate_str(self.employer)

        self.salary_from = self._validate_salary(self.salary_from)
        self.salary_to = self._validate_salary(self.salary_to)

        if not self.salary_from and self.salary_to:
            self.salary_from = self.salary_to
        elif not self.salary_to and self.salary_from:
            self.salary_to = self.salary_from


    @staticmethod
    def _validate_str(value: Optional[str]) -> str:
        """Проверяет, что значение — строка, и удаляет лишние пробелы."""
        if not isinstance(value, str) or not value:
            return ""
        return value.strip()


    @staticmethod
    def _validate_salary(value: Optional[int]) -> int:
        """Проверяет корректность зарплаты (отрицательные значения → 0)."""
        try:
            value = int(value or 0)
        except (TypeError, ValueError):
            value = 0
        return max(value, 0)


    def average_salary(self) -> float:
        """Возвращает среднюю зарплату, если указаны границы, иначе — одно из значений."""
        if self.salary_from and self.salary_to:
            return (self.salary_from + self.salary_to) / 2
        return float(self.salary_from or self.salary_to or 0)


    def __lt__(self, other: "Vacancy") -> bool:
        return self.average_salary() < other.average_salary()


    def __gt__(self, other: "Vacancy") -> bool:
        return self.average_salary() > other.average_salary()


    def __eq__(self, other: "Vacancy") -> bool:
        return self.average_salary() == other.average_salary()


    def to_dict(self) -> Dict[str, Any]:
        """Преобразует вакансию в словарь для сериализации."""
        return {
            "title": self.title,
            "url": self.url,
            "description": self.description,
            "employer": self.employer,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "currency": self.currency,
        }


    @staticmethod
    def from_hh_json(item: Dict[str, Any]) -> "Vacancy":
        """
        Преобразует словарь вакансии (формат hh.ru API) в объект Vacancy.
        """
        title = item.get("name", "")
        url = item.get("alternate_url") or item.get("url", "")
        employer = item.get("employer", {}).get("name") if item.get("employer") else None

        snippet = item.get("snippet", {}) or {}
        description = snippet.get("requirement") or snippet.get("responsibility") or ""

        salary = item.get("salary")
        salary_from = salary_to = 0
        currency = None
        if salary:
            salary_from = salary.get("from") or 0
            salary_to = salary.get("to") or 0
            currency = salary.get("currency")

        return Vacancy(
            title=title,
            url=url,
            description=description,
            employer=employer,
            salary_from=salary_from,
            salary_to=salary_to,
            currency=currency,
            raw=item
        )


    @staticmethod
    def cast_to_object_list(items: List[Dict[str, Any]]) -> List["Vacancy"]:
        """Преобразует список JSON-объектов (от hh.ru) в список объектов Vacancy."""
        return [Vacancy.from_hh_json(i) for i in items]
