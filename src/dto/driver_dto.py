from pydantic import BaseModel, ConfigDict


class DriverDto(BaseModel):
    id: str
    name: str

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_entity(cls, entity) -> "DriverDto":
        return cls(
            id=str(entity.id),
            name=entity.driver_name,
        )
