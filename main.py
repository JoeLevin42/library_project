from fastapi import FastAPI
import uvicorn
from routes.book_routs import router as book_router
from routes.member_routs import router as member_router
from database.db_connection import create_tables

app = FastAPI()
create_tables()

app.include_router(book_router)
app.include_router(member_router)

if __name__ == "__main__":
    uvicorn.run(host="localhost",port=8000)