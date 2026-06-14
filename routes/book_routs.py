from fastapi import APIRouter , HTTPException
from pydantic import BaseModel
from database import book_db
from database import member_db
from typing import Literal


bk_db = book_db.BookDB()
mm_db = member_db.MemberDB()
router = APIRouter()

class CreateBook(BaseModel):
        title: str
        author: str
        genre: Literal['Fiction','Non-Fiction','Science','History','Other']

class UpdateBook(BaseModel):
     is_available: bool = True
     borrowed_by_member_id: int | None  = None

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

@router.get("/books/{id}")
def get_book_by_id(id:int):
    try:
         the_book = bk_db.get_book_by_id(id=id)
         if the_book is None:
              raise HTTPException(status_code=404, detail="The book not found")
         
         return the_book
    except HTTPException:
         raise

@router.patch("/books/{id}/borrow/{member_id}")
def borrow_book_to_member(id:int,member_id:int):
    try:
        the_book = bk_db.get_book_by_id(id=id)
        if the_book is None:
              raise HTTPException(status_code=404, detail="The book not found")
        
        the_member = mm_db.get_member_by_id(id=member_id)
        if the_member is None:
             raise HTTPException(status_code=404, detail="The member not found")
        
        if the_book["is_available"] == False:
             raise HTTPException(status_code=400, detail="The book is not available")
        
        count_borrow = bk_db.count_active_borrows_by_member(member_id=member_id)
        if count_borrow > 3:
              raise HTTPException(status_code=400, detail="The member cant borrow more than three books")
        
        borrow_book = UpdateBook(is_available=False, borrowed_by_member_id=member_id)

        bk_db.update_book(id=id,payload=borrow_book.model_dump())
        mm_db.increment_borrows(id=member_id)
    
    except HTTPException:
         raise

@router.patch("/books/{id}/return/{member_id}")
def return_book_from_member(id:int,member_id:int):
    try:
        the_book = bk_db.get_book_by_id(id=id) 
        if the_book is None:
             raise HTTPException(status_code=404, detail="The book dont found")

        the_member = mm_db.get_member_by_id(id=member_id)
        if the_member is None:
             raise HTTPException(status_code=404, detail="The member not found")
        
        valid_member_active = the_member["is_active"]
        if valid_member_active == False:
             raise HTTPException(status_code=400 , detail="The member not active")
        
        valid_member_id = the_book["borrowed_by_member_id"]
        if int(valid_member_id) != member_id:
             raise HTTPException(400, detail="The book not borrowed to this member")

        return_book = UpdateBook(is_available=True ,borrowed_by_member_id=None)
        bk_db.update_book(id=id,payload=return_book.model_dump())

    except HTTPException:
         raise
