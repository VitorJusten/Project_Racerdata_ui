from typing import List, Optional, Union
import requests
from api_config import API_BASE_URL, API_TIMEOUT
from models.dashboard_driver_dto import DashboardDriverDto
from models.dashboard_driver_input_dto import DashboardDriverInputDto


class DashboardDriverService:
    """Serviço para gerenciamento dos pilotos selecionados para o dashboard."""

    BASE_PATH = f"{API_BASE_URL}/dashboard-drivers"

    @classmethod
    def get_all(cls, filter_text: Optional[str] = None) -> List[DashboardDriverDto]:
        params = {}
        if filter_text:
            params["filter"] = filter_text

        response = requests.get(cls.BASE_PATH, params=params, timeout=API_TIMEOUT)
        response.raise_for_status()
        return [DashboardDriverDto.model_validate(item) for item in response.json()]

    @classmethod
    def get_by_id(cls, dashboard_driver_id: str) -> DashboardDriverDto:
        url = f"{cls.BASE_PATH}/{dashboard_driver_id}"
        response = requests.get(url, timeout=API_TIMEOUT)
        response.raise_for_status()
        return DashboardDriverDto.model_validate(response.json())

    @classmethod
    def create(cls, data: Union[DashboardDriverInputDto, dict]) -> DashboardDriverDto:
        payload = data.model_dump() if isinstance(data, DashboardDriverInputDto) else data
        response = requests.post(cls.BASE_PATH, json=payload, timeout=API_TIMEOUT)
        response.raise_for_status()
        return DashboardDriverDto.model_validate(response.json())

    @classmethod
    def update(
        cls,
        dashboard_driver_id: str,
        data: Union[DashboardDriverInputDto, dict]
    ) -> DashboardDriverDto:
        payload = data.model_dump() if isinstance(data, DashboardDriverInputDto) else data
        url = f"{cls.BASE_PATH}/{dashboard_driver_id}"
        response = requests.put(url, json=payload, timeout=API_TIMEOUT)
        response.raise_for_status()
        return DashboardDriverDto.model_validate(response.json())

    @classmethod
    def delete(cls, dashboard_driver_id: str) -> bool:
        url = f"{cls.BASE_PATH}/{dashboard_driver_id}"
        response = requests.delete(url, timeout=API_TIMEOUT)
        response.raise_for_status()
        return True

    @classmethod
    def change_status(cls, dashboard_driver_id: str, is_active: bool) -> DashboardDriverDto:
        url = f"{cls.BASE_PATH}/{dashboard_driver_id}/status"
        params = {"isActive": is_active}
        response = requests.patch(url, params=params, timeout=API_TIMEOUT)
        response.raise_for_status()
        return DashboardDriverDto.model_validate(response.json())
