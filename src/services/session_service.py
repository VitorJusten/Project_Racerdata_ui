from typing import List, Optional
import requests
from api_config import API_BASE_URL, API_TIMEOUT
from dto.session_dto import SessionDto


class SessionService:
    """Serviço para consulta de sessões (corridas e treinos) da F1."""

    BASE_PATH = f"{API_BASE_URL}/sessions"

    @classmethod
    def get_all(cls, filter_text: Optional[str] = None) -> List[SessionDto]:
        params = {}
        if filter_text:
            params["filter"] = filter_text

        response = requests.get(cls.BASE_PATH, params=params, timeout=API_TIMEOUT)
        response.raise_for_status()
        return [SessionDto.model_validate(item) for item in response.json()]

    @classmethod
    def get_by_id(cls, session_id: str) -> SessionDto:
        url = f"{cls.BASE_PATH}/{session_id}"
        response = requests.get(url, timeout=API_TIMEOUT)
        response.raise_for_status()
        return SessionDto.model_validate(response.json())

    @classmethod
    def get_by_year(cls, year: int) -> List[SessionDto]:
        url = f"{cls.BASE_PATH}/by-year/{year}"
        response = requests.get(url, timeout=API_TIMEOUT)
        response.raise_for_status()
        return [SessionDto.model_validate(item) for item in response.json()]

    @classmethod
    def get_by_session_code(cls, session_key: int) -> SessionDto:
        url = f"{cls.BASE_PATH}/by-session-code/{session_key}"
        response = requests.get(url, timeout=API_TIMEOUT)
        response.raise_for_status()
        return SessionDto.model_validate(response.json())

    @classmethod
    def get_by_session_type(cls, session_type: str) -> List[SessionDto]:
        url = f"{cls.BASE_PATH}/by-session-type/{session_type}"
        response = requests.get(url, timeout=API_TIMEOUT)
        response.raise_for_status()
        return [SessionDto.model_validate(item) for item in response.json()]
