from pydantic import BaseModel, Field


class DashboardDriverInputDto(BaseModel):
    driver_id: str
    description: str = ""
    tag_color: str = "#E10600"
    isActive: bool = True


class DashboardDriverStatusDto(BaseModel):
    isActive: bool
