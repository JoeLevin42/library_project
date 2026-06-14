from fastapi import APIRouter , HTTPException
from pydantic import BaseModel
from database import book_db

bk_db = book_db.BookDB()
router = APIRouter()

class CreateBook(BaseModel):
        title: str
        author: str
        genre: str


@router.get("/books")
def get_all_books():
    all_books = bk_db.get_all_books()
    return all_books


@router.post("/books")
def create_new_book(payload: CreateBook):
    try:
        bk_db.create_book(payload=payload.model_dump())
    
    except HTTPException:
         raise

@router.get("books/{id}")
def get_book_by_id(id:int):
    pass

@router.patch("/books/{id}/borrow/{member_id}")
def borrow_book_to_member(id:int,member_id:int):
    pass

@router.patch("/books/{id}/return/{member_id}")
def return_book_from_member(id:int,member_id:int):
    pass

