from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer

class Base(DeclarativeBase):
    pass

class Book(Base):
    __tablename__ = 'book'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    author: Mapped[str] = mapped_column(String(100))
    year: Mapped[int] = mapped_column(Integer)
    genre: Mapped[str] = mapped_column(String(50), nullable=True)

    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title}, author={self.author}, genre={self.genre})>"