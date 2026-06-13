from fastapi import APIRouter
from pydantic import BaseModel
from database import member_db

class CreateMember(BaseModel):
        name: str 
        email: str


mm_db = member_db.MemberDB()
router = APIRouter()

@router.post("/members")
def create_new_member(member_data : CreateMember):
    mm_db.create_member(member_data.model_dump)
   
    return  {"message":"Member created"}

@router.get("/members")
def get_all_members():
    
    all_members = mm_db.get_all_members()
    return all_members

@router.get("/members/{id}")
def get_member_by_id(id:int):
    pass

@router.patch("/members/{id}")
def update_member(id:int,data:dict):
    pass

@router.patch("/members/{id}/deactivate")
def deactivate_member(id:int):
    pass

@router.patch("/members/{id}/activate")
def activate_member(id:int):
    pass