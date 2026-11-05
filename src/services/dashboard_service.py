from typing import Optional
import requests
from api_config import API_BASE_URL, API_TIMEOUT
from dto.dashboard_dto import CollectDataSummaryDto


class DashboardService:
    """Serviço para operações de dashboard e coleta de dados OpenF1."""

    @staticmethod
    def collect_data(year: Optional[int] = None) -> CollectDataSummaryDto:
        url = f"{API_BASE_URL}/dashboard/collect-data"
        params = {}
        if year:
            params["year"] = year

        response = requests.post(url, params=params, timeout=API_TIMEOUT * 30)
        response.raise_for_status()
        return CollectDataSummaryDto.model_validate(response.json())
