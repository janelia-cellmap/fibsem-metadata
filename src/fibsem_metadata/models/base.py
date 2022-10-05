from pydantic import BaseModel, Extra


def camelize(string: str) -> str:
    """
    Convert from snake case to camel case
    """
    parts = string.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


class Base(BaseModel):
    class Config:
        extra = Extra.forbid
        orm_mode = True
        alias_generator = camelize
        allow_population_by_field_name = True
