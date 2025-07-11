from fastapi import FastAPI
from app.api.v1 import books
from app.routers.web_viever import view_router

app = FastAPI(
    title="Book Service API",
    description="API to manage books, including uploading, downloading, and searching.",
    version="1.0.0"
)

app.include_router(books.router, prefix="/api/v1/books", tags=["books"])
app.include_router(view_router, prefix="/book", tags=["books"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Book Service API. Visit /docs for documentation."}
