from pydantic import BaseModel,Field


class Author(BaseModel):
    id: int = Field(default=None,exclude=True)
    name: str
    lastname: str
    surname: str


class Publisher(BaseModel):
    id:int = Field(default=None,exclude=True)
    publisher: str
    city: str


class Book(BaseModel):
    id:int = Field(default=None,exclude=True)
    title:str
    author:Author
    publisher:Publisher
    kind:str
    year:int