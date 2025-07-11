from sqlalchemy import Column, Integer, String, Date, Boolean
from .database import Base


# TODO: It make sense to use a separate book and author schemas, but for simplicity I will use one schema
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    author = Column(String, index=True)
    date_published = Column(Date, nullable=False)
    genre = Column(String, nullable=False)
    file_path = Column(String, nullable=False, unique=True)
    is_denied = Column(Boolean, default=False, nullable=False)
