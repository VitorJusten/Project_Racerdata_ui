from typing import Optional, List
from pydantic import BaseModel


class LineChartPointDto(BaseModel):
    x: Optional[str] = None  # date_end
    y: Optional[int] = None  # driver_position
    driver_id: str
    driver_name: str
    dashboard_driver_id: str
    dashboard_driver_description: str
    dashboard_driver_tag_color: str


class SessionDriverLineChartDto(BaseModel):
    dashboard_driver_id: str
    driver_id: str
    driver_name: str
    tag_color: str
    description: str
    points_dto: List[LineChartPointDto]
