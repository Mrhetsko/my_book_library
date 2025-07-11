from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services import book_service


view_router = APIRouter(
    tags=["Book Viewer"],
    include_in_schema=False
)

@view_router.get("/view/{book_id}", response_class=HTMLResponse)
def view_book(book_id: int, db: Session = Depends(get_db)):
    """
    Online book viewer. Including books in denied list.
    """
    db_book = book_service.get_book_by_id(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    try:
        with open(db_book.file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Book file not found on server")

    html_content = f"""
    <html>
        <head><title>{db_book.name}</title></head>
        <body>
            <h1>{db_book.name}</h1>
            <h2>{db_book.author}</h2>
            <hr>
            <pre>{content}</pre>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)