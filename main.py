from fastapi import FastAPI, HTTPException
from src.db.connection import init_db, engine
from src.db.models import Book
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

class BookSchema(BaseModel):
    title: str
    author: str
    year: int
    genre: str | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server is starting")
    await init_db()
    yield
    print("server is stopping")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def main():
    return {"message": "Hello World"}

@app.get("/books")
async def get_books():
    async with AsyncSession(engine) as session:
        result = await session.execute(select(Book))
        return result.scalars().all()

@app.get("/books/{book_id}")
async def get_book(book_id: int):
    async with AsyncSession(engine) as session:
        book = await session.get(Book, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book

@app.post("/books")
async def create_book(data: BookSchema):
    async with AsyncSession(engine) as session:
        book = Book(**data.model_dump())
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

@app.put("/books/{book_id}")
async def update_book(book_id: int, data: BookSchema):
    async with AsyncSession(engine) as session:
        book = await session.get(Book, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        for key, value in data.model_dump().items():
            setattr(book, key, value)
        await session.commit()
        await session.refresh(book)
        return book

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    async with AsyncSession(engine) as session:
        book = await session.get(Book, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        await session.delete(book)
        await session.commit()
        return {"message": "Book deleted"}