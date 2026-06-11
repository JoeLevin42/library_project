from database.db_connection import get_connection


class BookDB:
    def __init__(self):
        pass

    def create_book(self,data:dict):
        conn = get_connection()
        cursor = conn.cursor()

        name = data.get("name")
        title = data.get("title")
        author = data.get("author")
        genre = data.get("genre")

        values = (name,title,author,genre)

        sql_promt = """
        INSERT INTO books (name,title,author,genre) VALUES (%s,%s,%s,%s)
        """ 
        
        cursor.execute(sql_promt,values)

        conn.commit()
        cursor.close()
        conn.close()

    def get_all_books():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql_promt = "SELECT * FROM books"

        cursor.execute(sql_promt)

        rows = cursor.fetchall()

        cursor.close()
        conn.cursor()

        return rows 

    
    def get_book_by_id(self,id:int):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor 
        
    def update_book(self,id:int,data):
        pass

    def set_available(self,id:int,val:str,member_id):
        pass

    def count_total_books(self):
        pass

    def count_available_books(self):
        pass

    def count_borrowed_books(self):
        pass

    def count_by_genre(self,genre):
        pass

    def count_active_borrows_by_member(member_id:int):
        pass
