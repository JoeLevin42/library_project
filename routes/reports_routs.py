from fastapi import APIRouter
from database import member_db

router = APIRouter()

@router.get("/reports/summary")
def get_reports_summary():
    pass

@router.get("/reports/books-by-genre")
def get_reports_by_genre():
    pass

@router.get("/reports/top-member")
def get_report_top_member():
    pass