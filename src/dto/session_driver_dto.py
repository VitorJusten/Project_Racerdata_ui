from typing import Optional
from pydantic import BaseModel, ConfigDict


class SessionDriverDto(BaseModel):
    id: str
    session_id: str
    driver_id: str
    car_number: Optional[int] = None
    team_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_entity(cls, entity) -> "SessionDriverDto":
        return cls(
            id=str(entity.id),
            session_id=str(entity.session_id),
            driver_id=str(entity.driver_id),
            car_number=entity.car_number,
            team_name=entity.team_name,
        )
