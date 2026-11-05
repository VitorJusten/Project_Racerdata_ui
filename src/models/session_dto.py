from typing import Optional
from pydantic import BaseModel, ConfigDict


class SessionDto(BaseModel):
    id: str
    session_key: int
    meeting_key: Optional[int] = None
    session_name: Optional[str] = None
    session_type: Optional[str] = None
    year: Optional[int] = None
    country_name: Optional[str] = None
    location: Optional[str] = None
    circuit_short_name: Optional[str] = None
    date_start: Optional[str] = None
    date_end: Optional[str] = None
    is_cancelled: bool = False

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_entity(cls, entity) -> "SessionDto":
        return cls(
            id=str(entity.id),
            session_key=entity.session_key,
            meeting_key=entity.meeting_key,
            session_name=entity.session_name,
            session_type=entity.session_type,
            year=entity.year,
            country_name=entity.country_name,
            location=entity.location,
            circuit_short_name=entity.circuit_short_name,
            date_start=entity.date_start,
            date_end=entity.date_end,
            is_cancelled=bool(entity.is_cancelled),
        )
