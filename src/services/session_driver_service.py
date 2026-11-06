from typing import List, Optional
import requests
from api_config import API_BASE_URL, API_TIMEOUT
from models.session_driver_dto import SessionDriverDto
from models.session_driver_line_chart_dto import SessionDriverLineChartDto
from models.session_driver_results_dto import SessionDriverResultsDto


class SessionDriverService:
    """Servico para consulta de participacoes e resultados de pilotos em sessoes."""

    BASE_PATH = f"{API_BASE_URL}/session-drivers"

    @classmethod
    def get_by_id(cls, session_driver_id: str) -> SessionDriverDto:
        url = f"{cls.BASE_PATH}/{session_driver_id}"
        response = requests.get(url, timeout=API_TIMEOUT)
        response.raise_for_status()
        return SessionDriverDto.model_validate(response.json())

    @classmethod
    def get_all(cls, filter_text: Optional[str] = None) -> List[SessionDriverDto]:
        params = {}
        if filter_text:
            params["filter_text"] = filter_text

        response = requests.get(cls.BASE_PATH, params=params, timeout=API_TIMEOUT)
        response.raise_for_status()
        return [SessionDriverDto.model_validate(item) for item in response.json()]

    @classmethod
    def get_drivers_for_line_chart(
        cls,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        session_type: Optional[str] = None
    ) -> List[SessionDriverLineChartDto]:
        url = f"{cls.BASE_PATH}/line-chart"
        params = {}
        if date_from:
            params["date_from"] = date_from
        if date_to:
            params["date_to"] = date_to
        if session_type:
            params["session_type"] = session_type

        response = requests.get(url, params=params, timeout=API_TIMEOUT)
        response.raise_for_status()
        return [SessionDriverLineChartDto.model_validate(item) for item in response.json()]

    @classmethod
    def get_all_results(
        cls,
        year: Optional[int] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        session_type: Optional[str] = None
    ) -> List[SessionDriverResultsDto]:
        url = f"{cls.BASE_PATH}/results"
        params = {}
        if year:
            params["year"] = year
        if date_from:
            params["date_from"] = date_from
        if date_to:
            params["date_to"] = date_to
        if session_type:
            params["session_type"] = session_type

        response = requests.get(url, params=params, timeout=API_TIMEOUT)
        response.raise_for_status()
        return [SessionDriverResultsDto.model_validate(item) for item in response.json()]
