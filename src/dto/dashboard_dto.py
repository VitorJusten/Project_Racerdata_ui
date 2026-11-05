from typing import Optional, List
from pydantic import BaseModel, Field

from dto.session_dto import SessionDto
from dto.session_driver_dto import SessionDriverDto


class CollectDataSummaryDto(BaseModel):
    sessions_found: int = 0
    sessions_new: int = 0
    sessions_updated: int = 0
    drivers_found: int = 0
    drivers_new: int = 0
    participations_created: int = 0
    participations_updated: int = 0
    errors_count: int = 0
    failed_sessions: List[int] = Field(default_factory=list)


class DashboardFilterDto(BaseModel):
    year: Optional[int] = None
    session_type: Optional[str] = None
    driver_id: Optional[str] = None
    team_name: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class PerformancePointDto(BaseModel):
    session_name: str
    session_date: str
    car_number: Optional[int] = None
    team_name: Optional[str] = None
    value: float | int | None = None


class DriverPerformanceDto(BaseModel):
    driver_id: str
    driver_name: str
    tag_color: str
    points: List[PerformancePointDto]


class DashboardOverviewDto(BaseModel):
    total_sessions: int
    total_drivers: int
    active_dashboard_drivers: int
    available_years: List[int]
    drivers_performance: List[DriverPerformanceDto]
