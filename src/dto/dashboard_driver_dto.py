from typing import Optional
from pydantic import BaseModel, ConfigDict


class DashboardDriverDto(BaseModel):
    id: str
    driver_id: str
    driver_name: str
    description: str
    tag_color: str
    isActive: bool

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_entity(cls, entity) -> "DashboardDriverDto":
        driver_name = entity.driver.driver_name if entity.driver else ""
        return cls(
            id=str(entity.id),
            driver_id=str(entity.driver_id),
            driver_name=driver_name,
            description=entity.description or "",
            tag_color=entity.tag_color or "#E10600",
            isActive=bool(entity.isActive),
        )
