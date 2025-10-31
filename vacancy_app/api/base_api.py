from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseJobsAPI(ABC):
    """Абстрактный класс для работы с API платформ вакансий."""

    @abstractmethod
    def get_vacancies(self, query: str, per_page: int = 20, pages: int = 1) -> List[Dict[str, Any]]:
        """Возвращает список вакансий в формате JSON-словарей."""
        raise NotImplementedError
