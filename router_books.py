from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

import dal_books

router = APIRouter(prefix="/books", tags=["Books"])

class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    language: Optional[str] = Field(default=None, max_length=100)
    price: float = Field(..., ge=0)
    published_year: Optional[int] = Field(default=None, ge=0, le=9999)


class BookUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    language: Optional[str] = Field(default=None, max_length=100)
    price: float = Field(..., ge=0)
    published_year: Optional[int] = Field(default=None, ge=0, le=9999)


@router.get("")
def get_books():
    return dal_books.get_all_books()


@router.get("/{book_id}")
def get_book(book_id: int):
    book = dal_books.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("", status_code=201)
def create_book(book: BookCreate):
    new_book = dal_books.insert_book(
        title=book.title,
        author=book.author,
        language=book.language,
        price=book.price,
        published_year=book.published_year
    )
    return new_book


@router.put("/{book_id}")
def update_book(book_id: int, book: BookUpdate):
    updated_book = dal_books.update_book(
        book_id=book_id,
        title=book.title,
        author=book.author,
        language=book.language,
        price=book.price,
        published_year=book.published_year
    )

    if updated_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return updated_book


@router.delete("/{book_id}")
def delete_book(book_id: int):
    deleted_book = dal_books.delete_book(book_id)

    if deleted_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return {
        "message": "Book deleted successfully",
        "book": deleted_book
    }


@router.delete("/table/refresh")
def recreate_books_table():
    dal_books.recreate_table_books()
    return {"message": "Books table dropped and recreated successfully"}