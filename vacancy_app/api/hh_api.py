import requests
from typing import List, Dict, Any
from .base_api import BaseJobsAPI


class HeadHunterAPI(BaseJobsAPI):
    """Реализация API для hh.ru"""

    BASE_URL = "https://api.hh.ru/vacancies"


    def __init__(self, area: int = 113, user_agent: str = "hh-python-client/1.0"):
        self.area = area
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})


    def get_vacancies(self, query: str, per_page: int = 20, pages: int = 1) -> List[Dict[str, Any]]:
        results = []
        for page in range(pages):
            params = {"text": query, "area": self.area, "per_page": per_page, "page": page}
            resp = self.session.get(self.BASE_URL, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            items = data.get("items", [])
            results.extend(items)
            if page >= data.get("pages", 0) - 1:
                break
        return results
