import pandas as pd
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from fastapi.responses import FileResponse, HTMLResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import book as book_schema
from app.services import book_service

router = APIRouter()


@router.post("/", response_model=book_schema.Book, status_code=status.HTTP_201_CREATED)
def create_book(
        name: str = Form(...),
        author: str = Form(...),
        date_published: str = Form(...),
        genre: str = Form(None),
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    """
    Create new book.
    - **name**: Book name (required)
    - **author**: Book author (required)
    - **date_published**: Publication date in format YYYY-MM-DD (required)
    - **genre**: Genre of the book (optional)
    - **file**: Book file (required, must be  .txt file)
    """
    file_path = book_service.save_book_file(file)
    book_data = book_schema.BookCreate(
        name=name,
        author=author,
        date_published=date_published,
        genre=genre
    )
    return book_service.create_book(db=db, book_data=book_data, file_path=file_path)


@router.get("/", response_model=List[book_schema.Book])
def read_books(
        name: str | None = None,
        author: str | None = None,
        date_published: str | None = None,
        genre: str | None = None,
        db: Session = Depends(get_db)
):
    """
    Retrieve a list of books with optional filters.
    """
    return book_service.get_books(db, name, author, date_published, genre)


@router.get("/{book_id}/download", response_class=FileResponse)
def download_book(book_id: int, db: Session = Depends(get_db)):
    """
    Download a book by its ID + check within denied list.
    """
    db_book = book_service.get_book_by_id(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    if db_book.is_denied:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This book is denied for download")
    return FileResponse(path=db_book.file_path, filename=db_book.name + ".txt", media_type='application/octet-stream')


@router.post("/denylist/upload", summary="Download and update denylist",)
def upload_denylist(
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    """
    Receive an XLSX file to update the denylist of books and authors.

    File must contain two sheets:
    - First sheet: names of books to deny.
    - Second sheet: names of authors to deny.
    """
    if not file.filename.endswith('.xlsx'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="incorrect file type. Please upload an XLSX file."
        )

    try:
        xls_data = pd.read_excel(file.file, sheet_name=None, dtype=str)
        sheet_names = list(xls_data.keys())

        if len(sheet_names) < 2:
            raise ValueError("file must contain at least two sheets: one for book names and one for author names.")

        # Read data from the first two sheets
        names_df = xls_data[sheet_names[0]]
        authors_df = xls_data[sheet_names[1]]

        if 'name' not in names_df.columns or 'name' not in authors_df.columns:
            raise ValueError("each file must contain a 'name' column in both sheets.")

        names_to_deny = names_df['name'].dropna().tolist()
        authors_to_deny = authors_df['name'].dropna().tolist()

        updated_count = book_service.update_denylist(db, names=names_to_deny, authors=authors_to_deny)

        return {
            "message": "Black list was updated.",
            "books_denied_count": updated_count
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error occurred while processing the file: {str(e)}")
