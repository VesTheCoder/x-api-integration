from pydantic import BaseModel


class ErrorDTO(BaseModel):
    query: str
    exc: str
