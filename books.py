from email.policy import default

from fastapi import FastAPI, Path, Query, HTTPException
from typing import Optional
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="id is not required on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1799, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example":{
                "title": "A new book",
                "author": "A new author",
                "description": "A new description",
                "rating": 5,
                "published_date": 2012
            }
        }
    }

BOOKS = [
    Book(1, "Pride and Prejudice", "Jane Austen", "Some description", 5, 1813),
    Book(2, "Crime and Punishment", "Fyodor Dostoevsky", "Some description", 4, 1866),
    Book(3, "Anna Karenina", "Lev Tolstoy", "Some description", 5, 1878),
    Book(4, "Emma", "Jane Austen", "Some description", 3, 1815),
    Book(5, "White Nights", "Fyodor Dostoevsky", "Some description", 4, 1848),
    Book(6, "Far from the madding crowd", "Thomas Hardy", "Some description", 5, 1874),
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def get_all_books():
    return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/published-date/", status_code=status.HTTP_200_OK)
async def get_books_by_published_date(published_date: int = Query(gt=1799, lt=2031)):
    books_by_published_date = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_by_published_date.append(book)
    return books_by_published_date

@app.get("/books/", status_code=status.HTTP_200_OK)
async def get_books_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_by_rating = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_by_rating.append(book)
    return books_by_rating

@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

@app.put("/update-book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")
    

@app.delete("/delete-book/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break

def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book