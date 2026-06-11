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

        sql_promt = "SELECT * FROM books WHERE id = %s"

        cursor.execute(sql_promt,(id,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return row
           
    def update_book(self,id:int,data):
        conn = get_connection()
        cursor = conn.cursor()

        set_parts = [f"`{key}`" for key in data.keys()]
        set_clause = ", ".join(set_parts)

        values = list(data.values()) + [id]

        sql_promt = f"UPDATE books SET {set_clause} WHERE id = %s"
        
        cursor.execute(sql_promt,values)
        
        cursor.close()
        conn.close()


    def set_available(self,id:int,val:str,member_id:str):
        conn = get_connection()
        cursor = conn.cursor()

        values = (val,member_id,id)
        sql_promt = "UPDATE books SET is_available = %s , borrowed_by_member_id = %s WHERE id = %s"

        cursor.execute(sql_promt,values)

        conn.commit()
        cursor.close()
        conn.close()


    def count_total_books(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql_promt = "SELECT * FROM books ORDER BY name ASC"

        cursor.execute(sql_promt)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows

    def count_available_books(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql_promt = "SELECT * FROM books WHERE is_available = TRUE"

        cursor.execute(sql_promt)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows
    
    def count_borrowed_books(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql_promt = "SELECT * FROM books WHERE is_available = FALSE"

        cursor.execute(sql_promt)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows

    def count_by_genre(self,genre):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql_promt = "SELECT * FROM books WHERE genre = %s"
        cursor.execute(sql_promt,(genre,))

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows

    def count_active_borrows_by_member(member_id:int):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql_promt = "SELECT COUNT(*) FROM books WHERE member_id = %s"
        cursor.execute(sql_promt,(member_id,))

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return row
    