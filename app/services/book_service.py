import os
import shutil
from typing import List, Optional
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.db import models
from app.schemas import book as book_schema

UPLOAD_DIRECTORY = "uploads" # Directory for book files

# Make sure the upload directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


def save_book_file(file: UploadFile) -> str:
    """
    Saves the uploaded book file and returns the file path.
    """
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path


def create_book(db: Session, book_data: book_schema.BookCreate, file_path: str) -> models.Book:
    """
    Saves a new book to the database.
    """
    db_book = models.Book(**book_data.model_dump(), file_path=file_path)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book_by_id(db: Session, book_id: int) -> Optional[models.Book]:
    """
    Gets a book by its ID.
    """
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_books(db: Session, name: str | None, author: str | None, date_published: str | None, genre: str | None) -> List[
    models.Book]:
    """
    Returns a list of books filtered by optional parameters.
    """
    query = db.query(models.Book)
    if name:
        query = query.filter(models.Book.name.ilike(f"%{name}%"))
    if author:
        query = query.filter(models.Book.author.ilike(f"%{author}%"))
    if date_published:
        query = query.filter(models.Book.date_published == date_published)
    if genre:
        query = query.filter(models.Book.genre.ilike(f"%{genre}%"))
    return query.all()


def update_denylist(db: Session, names: List[str], authors: List[str]) -> int:
    """
    Args:
        db (Session): db session.
        names (List[str]): List of book names to block.
        authors (List[str]): List of book authors to block.

    Returns:
        int: Quantity of updated books.
    """
    if not names and not authors:
        return 0

    query = db.query(models.Book).filter(
        (models.Book.name.in_(names)) | (models.Book.author.in_(authors))
    )

    updated_count = query.update({"is_denied": True}, synchronize_session=False)

    db.commit()

    return updated_count