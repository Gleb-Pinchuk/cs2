from typing import List, Dict, Any
from .base_api import BaseJobsAPI


class HeadHunterAPI(BaseJobsAPI):
    """Реализация API для получения вакансий с hh.ru"""

    BASE_URL = "https://api.hh.ru"  # базовый URL API hh.ru


    def __init__(self, area: int = 113, user_agent: str = "hh-python-client/1.0"):
        """
        :param area: код региона (по умолчанию 113 — Россия)
        :param user_agent: строка User-Agent для идентификации клиента
        """
        self.area = area
        self.user_agent = user_agent


    def _connect(self, endpoint: str = "", params: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """
        Приватный метод подключения к API hh.ru.
        """
        import requests

        if not self.BASE_URL:
            raise ValueError("BASE_URL не определён в классе HeadHunterAPI.")

        url = f"{self.BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"
        headers = {"User-Agent": self.user_agent}

        response = requests.get(url, params=params or {}, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()


    def get_vacancies(self, query: str, per_page: int = 20, pages: int = 1) -> List[Dict[str, Any]]:
        """
        Получает список вакансий по запросу с hh.ru.
        """
        results = []

        for page in range(pages):
            params = {
                "text": query,
                "area": self.area,
                "per_page": per_page,
                "page": page
            }

            data = self._connect("/vacancies", params=params)
            results.extend(data.get("items", []))

            if page >= data.get("pages", 0) - 1:
                break

        return results
