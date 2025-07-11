from pydantic import BaseModel, Field
from datetime import date


# Base book schema
class BookBase(BaseModel):
    # FIXME: Divide book and author schemas?
    name: str = Field(..., max_length=255, description="Name of the book")
    author: str = Field(..., max_length=255, description="Author of the book")
    date_published: date = Field(..., description="Publication date of the book")
    genre: str = Field(..., max_length=100, description="Genre of the book")  # FIXME: Use Enum for genres? Use genre None


class BookCreate(BookBase):
    # No need for `id` - it will be automatically crated by database
    pass


class Book(BookBase):
    """
    Represents a book in the system.
    Schema for retrieving book details, including all the fields we want return to the user.
    """
    id: int = Field(..., description="Unique identifier of the book")
    is_denied: bool

    class Config:
        from_attributes = True  # ORM mode for compatibility with SQAlchemy models


