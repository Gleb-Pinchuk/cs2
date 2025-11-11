from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import requests


class BaseJobsAPI(ABC):
    """
    Абстрактный класс для работы с API платформ вакансий.
    """

    BASE_URL: Optional[str] = None


    def _connect(self, endpoint: str = "", params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Приватный метод подключения к API.
        """
        if not self.BASE_URL:
            raise ValueError("BASE_URL не определён в дочернем классе API.")

        url = f"{self.BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"
        response = requests.get(url, params=params or {})
        response.raise_for_status()
        return response.json()


    @abstractmethod
    def get_vacancies(self, query: str, per_page: int = 20, pages: int = 1) -> List[Dict[str, Any]]:
        """
        Абстрактный метод для получения списка вакансий.
        """
        raise NotImplementedError("Метод get_vacancies() должен быть реализован в подклассе.")
