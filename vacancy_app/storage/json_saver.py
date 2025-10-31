import json
import os
from typing import List, Callable, Any
from vacancy_app.models.vacancy import Vacancy
from .base_saver import BaseSaver


class JSONSaver(BaseSaver):
    def __init__(self, filepath: str = "vacancies.json"):
        self.filepath = filepath
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)


    def _read(self) -> List[dict]:
        with open(self.filepath, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []


    def _write(self, data: List[dict]):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


    def add_vacancy(self, vacancy: Vacancy):
        data = self._read()
        if any(v.get("url") == vacancy.url for v in data):
            data = [vacancy.to_dict() if v["url"] == vacancy.url else v for v in data]
        else:
            data.append(vacancy.to_dict())
        self._write(data)


    def get_vacancies(self, filter_func: Callable[[Vacancy], bool] = None) -> List[Vacancy]:
        data = self._read()
        vacancies = [
            Vacancy(**{k: v for k, v in item.items() if k in Vacancy.__dataclass_fields__})
            for item in data
        ]
        if filter_func:
            vacancies = [v for v in vacancies if filter_func(v)]
        return vacancies


    def delete_vacancy(self, identifier: Any) -> bool:
        data = self._read()
        before = len(data)
        if isinstance(identifier, str):
            data = [v for v in data if v.get("url") != identifier and v.get("title") != identifier]
        elif hasattr(identifier, "url"):
            data = [v for v in data if v.get("url") != identifier.url]
        self._write(data)
        return len(data) < before
