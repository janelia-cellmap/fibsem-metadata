from pydantic import BaseModel, Extra


class Base(BaseModel):
    class Config:
        extra = Extra.forbid
        orm_mode = True
