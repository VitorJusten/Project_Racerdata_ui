from typing import Optional, List
from pydantic import BaseModel


class DriverPositionResultDto(BaseModel):
    session_driver_id: str
    driver_id: str
    driver_name: str
    team_name: Optional[str] = None
    car_number: Optional[int] = None
    driver_position: Optional[int] = None


class SessionResultDetailDto(BaseModel):
    session_id: str
    date_end: Optional[str] = None
    session_type: Optional[str] = None
    circuit_short_name: Optional[str] = None
    drivers_positions_dto: List[DriverPositionResultDto]


class SessionDriverResultsDto(BaseModel):
    year: Optional[int] = None
    result_dto: List[SessionResultDetailDto]
