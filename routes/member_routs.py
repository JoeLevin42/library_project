from fastapi import APIRouter , HTTPException
from pydantic import BaseModel
from database import member_db

class CreateMember(BaseModel):
        name: str 
        email: str

class UpdateMember(BaseModel):
        name: str | None = None
        email: str | None = None
        genre: str | None = None
        is_available: bool | None = None
        borrowed_by_member_id: str | None = None

mm_db = member_db.MemberDB()
router = APIRouter()

@router.post("/members")
def create_new_member(member_data : CreateMember):

    try:
        mm_db.create_member(member_data.model_dump())

    except HTTPException:
         raise
    except Exception as e:
         raise HTTPException(status_code=503 , detail=f"The creation failed unknown error {str(e)}")
    
    return  {"message":"Member created"}

@router.get("/members")
def get_all_members():
    try:
        all_members = mm_db.get_all_members()
        return all_members
    
    except HTTPException:
         raise

@router.get("/members/{id}")
def get_member_by_id(id:int):
    try:
        the_member = mm_db.get_member_by_id(id=id)
        if the_member is None:
            raise HTTPException(status_code=404 , detail="The member not found")

        return the_member
    except HTTPException:
         raise
    
@router.patch("/members/{id}")
def update_member(id:int,data: UpdateMember):
    try:
        the_member =  mm_db.get_member_by_id(id=id)

        if the_member is None:
             raise HTTPException(status_code=404, detail="The member not found")
        
        mm_db.update_member(id=id,data=data.model_dump())
    
    except HTTPException:
         raise

@router.put("/members/{id}/deactivate")
def deactivate_member(id:int):
    try:
        the_member = mm_db.get_member_by_id(id=id)
        if the_member is None:
            raise HTTPException(status_code=404, detail="The member not found")
        
        mm_db.deactivate_member(id=id)
    
    except HTTPException:
         raise

@router.put("/members/{id}/activate")
def activate_member(id:int):
    try:
         the_member = mm_db.active_member(id=id)
         if the_member is None:
              raise HTTPException(status_code=404, detail="The member not found")
        
         mm_db.active_member(id=id)

    except HTTPException:
         raise
