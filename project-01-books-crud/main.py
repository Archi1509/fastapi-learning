from fastapi import FastAPI, Body, HTTPException

app = FastAPI()

books = [
    {
        "id": 1,
        "title": "Atomic Habits",
        "author": "James Clear",
        "category": "Self Help"
    },
    {
        "id": 2,
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt",
        "category": "Programming"
    },
    {
        "id": 3,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "category": "Programming"
    },
    {
        "id": 4,
        "title": "Deep Work",
        "author": "Cal Newport",
        "category": "Productivity"
    },
    {
        "id": 5,
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "category": "Fiction"
    }
]


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/books")
def read_all_books():
    return books

@app.get("/books/title/{book_title}")
def read_book_by_title(book_title: str):
    books_to_return = []
    for book in books:
        if book_title.casefold() in book.get("title").casefold():
            books_to_return.append(book)
    if not books_to_return:
        raise HTTPException(status_code=404, detail="Book not found")
    return books_to_return

@app.get("/books/")
def read_books_filter_category(category: str):
    books_to_return = []
    for book in books:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    if not books_to_return:
        raise HTTPException(status_code=404, detail="Book not found")
    return books_to_return

@app.get("/books/author/{author}")
def read_books_by_author(author: str):
    books_to_return = []
    for book in books:
        if author.casefold() in book.get("author").casefold():
            books_to_return.append(book)
    if not books_to_return:
        raise HTTPException(status_code=404, detail="Book not found")
    return books_to_return

@app.get("/books/author/{author}/category/{category}")
def read_books_by_author_and_category(author: str, category: str):
    books_to_return = []
    for book in books:
        if (author.casefold() in book.get("author").casefold() and
                book.get("category").casefold() == category.casefold()):
            books_to_return.append(book)
    if not books_to_return:
        raise HTTPException(status_code=404, detail="Book not found")
    return books_to_return

@app.post("/books")
def add_book(book = Body()):
    books.append(book)
    return book

@app.put("/books/id/{book_id}")
def update_book_data(book_id: int, updated_book= Body()):
    for book in books:
        if book.get("id") == book_id:
            book.update(updated_book)
    return updated_book

@app.delete("/books/id/{book_id}")
def delete_book_data(book_id: int):
    for i in range(len(books)):
        if books[i].get('id') == book_id:
            books.pop(i)
            break
        

@app.get("/books/count")
def count_books():
    return {
        "total_books": len(books)
    }

@app.get("/books/all/categories")
def read_all_book_categories():
    categories = []
    for book in books:
        if book.get("category") and book.get("category") not in categories:
            categories.append(book.get("category"))
    return categories




