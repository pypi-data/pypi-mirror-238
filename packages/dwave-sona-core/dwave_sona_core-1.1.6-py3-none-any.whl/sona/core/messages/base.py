from __future__ import annotations

from pydantic import BaseModel


class MessageBase(BaseModel):
    def mutate(self, **kwargs) -> MessageBase:
        kwargs = {**self.model_dump(), **kwargs}
        return self.__class__(**kwargs)

    def to_message(self) -> str:
        return self.model_dump_json()

    class Config:
        frozen = False
