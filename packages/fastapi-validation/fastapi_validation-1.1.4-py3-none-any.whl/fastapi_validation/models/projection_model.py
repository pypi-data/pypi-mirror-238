from uuid import UUID

from pydantic import BaseModel


class ProjectionModel(BaseModel):
    id: UUID
