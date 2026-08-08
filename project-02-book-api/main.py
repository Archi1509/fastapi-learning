from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from starlette import status
from typing import Optional

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
    id: Optional[int] = Field(default=None, description='Book id not needed to be created.')
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    model_config = {
        'json_schema_extra': {
            'example': {
                'title': 'A New Book',
                'author': 'Author Name',
                'description': 'Description of New Book',
                'rating': 5,
                'published_date': 2025,
            }
        }
    }

BOOKS = [
    Book(1, 'Python Basics', 'John Smith', 'Introduction to Python programming', 5, 2022),
    Book(2, 'FastAPI Guide', 'Alex Brown', 'Building APIs with FastAPI', 4, 2023),
    Book(3, 'Learning PostgreSQL', 'Sarah Wilson', 'A guide to PostgreSQL databases', 5, 2021),
    Book(4, 'Clean Code', 'Robert Martin', 'Principles of writing clean code', 5, 2008),
    Book(5, 'Django Fundamentals', 'David Lee', 'Learn Django web development', 3, 2024),
    Book(6, 'Backend Development', 'Emily Clark', 'Fundamentals of backend development', 4, 2025)
]

@app.get("/books")
def get_all_books():
    return BOOKS

@app.get("/book/id/{id}")
def get_book_by_id(id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.get("/book/")
def get_books_by_rating(rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == rating:
            books_to_return.append(book)
    return books_to_return

@app.get("/book/published/")
def get_book_publish_date(published_date: int = Query(lt=2031, gt=1999)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return

def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

@app.post("/book/", status_code=status.HTTP_201_CREATED)
def create_book(book: BookRequest):
    new_book = Book(**book.model_dump())
    BOOKS.append(find_book_id(new_book))
    return new_book

@app.put("/book/update_book", status_code=status.HTTP_200_OK)
def update_book(book: BookRequest):
    updated = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = Book(
                book.id,
                book.title,
                book.author,
                book.description,
                book.rating,
                book.published_date
            )
            updated = True
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.delete("/book/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(id: int = Path(gt=0)):
    deleted = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == id:
            BOOKS.pop(i)
            deleted = True
            break
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")



