from typing import List, Optional
import requests
from api_config import API_BASE_URL, API_TIMEOUT
from models.driver_dto import DriverDto


class DriverService:
    """Serviço para consulta dos pilotos cadastrados no sistema."""

    BASE_PATH = f"{API_BASE_URL}/drivers"

    @classmethod
    def get_all(cls, filter_text: Optional[str] = None) -> List[DriverDto]:
        params = {}
        if filter_text:
            params["filter"] = filter_text

        response = requests.get(cls.BASE_PATH, params=params, timeout=API_TIMEOUT)
        response.raise_for_status()
        return [DriverDto.model_validate(item) for item in response.json()]

    @classmethod
    def get_by_id(cls, driver_id: str) -> DriverDto:
        url = f"{cls.BASE_PATH}/{driver_id}"
        response = requests.get(url, timeout=API_TIMEOUT)
        response.raise_for_status()
        return DriverDto.model_validate(response.json())
