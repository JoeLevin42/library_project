from fastapi import APIRouter

router = APIRouter()

@router.get("/books")
def get_all_books():
    pass


@router.post("/books")
def create_new_member():
    pass

@router.get("books/{id}")
def get_book_by_id(id:int):
    pass

@router.patch("/books/{id}/borrow/{member_id}")
def borrow_book_to_member(id:int,member_id:int):
    pass

@router.patch("/books/{id}/return/{member_id}")
def return_book_from_member(id:int,member_id:int):
    pass

