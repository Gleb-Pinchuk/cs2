from abc import ABC, abstractmethod
from typing import List, Callable, Any
from vacancy_app.models.vacancy import Vacancy

class BaseSaver(ABC):
    """Абстрактный интерфейс для хранения вакансий."""


    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        pass


    @abstractmethod
    def get_vacancies(self, filter_func: Callable[[Vacancy], bool] = None) -> List[Vacancy]:
        pass


    @abstractmethod
    def delete_vacancy(self, identifier: Any) -> bool:
        pass


    def connect(self):
        pass


    def close(self):
        pass
