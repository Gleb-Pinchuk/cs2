import json
import os
from typing import List, Callable, Any
from vacancy_app.models.vacancy import Vacancy
from .base_saver import BaseSaver


class JSONSaver(BaseSaver):
    """
    Класс для сохранения и управления вакансиями в JSON-файле.
    Поддерживает добавление, фильтрацию, чтение и удаление вакансий.
    """


    def __init__(self, filepath: str = "vacancies.json"):
        """Инициализация класса, создаёт файл, если он отсутствует."""
        self.__filepath = filepath  # приватный атрибут
        if not os.path.exists(self.__filepath):
            with open(self.__filepath, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)


    def __read(self) -> List[dict]:
        """Приватный метод чтения данных из файла JSON."""
        if not os.path.exists(self.__filepath):
            return []
        with open(self.__filepath, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def __write(self, data: List[dict]) -> None:
        """Приватный метод записи данных в JSON-файл."""
        with open(self.__filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Добавляет вакансию в файл.
        Если вакансия с таким URL уже существует — обновляет её.
        """
        data = self.__read()

        updated = False
        for i, v in enumerate(data):
            if v.get("url") == vacancy.url:
                data[i] = vacancy.to_dict()
                updated = True
                break

        if not updated:
            data.append(vacancy.to_dict())

        self.__write(data)


    def get_vacancies(self, filter_func: Callable[[Vacancy], bool] = None) -> List[Vacancy]:
        """
        Возвращает список вакансий.
        Можно применить фильтр в виде функции.
        """
        data = self.__read()
        vacancies = [
            Vacancy(**{k: v for k, v in item.items() if k in Vacancy.__dataclass_fields__})
            for item in data
        ]
        if filter_func:
            vacancies = [v for v in vacancies if filter_func(v)]
        return vacancies


    def delete_vacancy(self, identifier: Any) -> bool:
        """
        Удаляет вакансию по URL, названию или объекту Vacancy.
        """
        data = self.__read()
        before_count = len(data)

        if isinstance(identifier, str):
            data = [v for v in data if v.get("url") != identifier and v.get("title") != identifier]
        elif isinstance(identifier, Vacancy):
            data = [v for v in data if v.get("url") != identifier.url]

        self.__write(data)
        return len(data) < before_count


    @property
    def filepath(self) -> str:
        """Возвращает путь к текущему файлу."""
        return self.__filepath
