from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Vacancy:
    title: str
    url: str
    description: str
    employer: Optional[str] = None
    salary_from: Optional[int] = field(default=0)
    salary_to: Optional[int] = field(default=0)
    currency: Optional[str] = field(default=None)
    raw: Optional[dict] = field(default=None, repr=False)

    def __post_init__(self):
        self.title = (self.title or "").strip()
        self.url = (self.url or "").strip()
        self.description = (self.description or "").strip()
        self.salary_from = int(self.salary_from or 0)
        self.salary_to = int(self.salary_to or 0)
        if self.salary_from < 0:
            self.salary_from = 0
        if self.salary_to < 0:
            self.salary_to = 0

    def average_salary(self) -> float:
        if self.salary_from and self.salary_to:
            return (self.salary_from + self.salary_to) / 2
        return float(self.salary_from or self.salary_to or 0)

    def __lt__(self, other: "Vacancy") -> bool:
        return self.average_salary() < other.average_salary()

    def __gt__(self, other: "Vacancy") -> bool:
        return self.average_salary() > other.average_salary()

    def to_dict(self) -> dict:
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
    def from_hh_json(item: dict) -> "Vacancy":
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
        return Vacancy(title, url, description, employer, salary_from, salary_to, currency, item)

    @staticmethod
    def cast_to_object_list(items: List[dict]) -> List["Vacancy"]:
        return [Vacancy.from_hh_json(i) for i in items]
