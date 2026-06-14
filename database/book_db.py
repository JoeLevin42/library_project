from database.db_connection import get_connection

class BookDB:
    def __init__(self):
        pass

    def create_book(self,payload:dict):
        
        conn = get_connection()
        cursor = conn.cursor()

        columns_parts = [f"`{key}`" for key in payload.keys()]
        columns_str = ", ".join(columns_parts)
        place_holders = ", ".join(["%s"]*len(columns_parts))
        values = tuple(payload.values())

        sql = f"INSERT INTO books ({columns_str}) VALUES ({place_holders})"

        try:
            cursor.execute(sql,values)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()
        
    def get_all_books(self):
       
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT * FROM books"

        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows
        finally:
            cursor.close()
            conn.close()
        
    
    def get_book_by_id(self,id:int):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT * FROM `books` WHERE id = %s"
        try:
            cursor.execute(sql,(id,))
            row = cursor.fetchone()
            return row
        
        finally:
            cursor.close()
            conn.close()
           
    def update_book(self,id:int,payload:dict):
        conn = get_connection()
        cursor = conn.cursor()

        update_parts = [f"`{key}`=%s" for key in payload.keys()]
        update_str = ", ".join(update_parts)
        values = tuple(payload.values()) + (id,)
        sql = f"UPDATE books SET {update_str} WHERE id = %s"

        try:
            cursor.execute(sql,values)
            conn.commit()

        except Exception as e:
            conn.rollback()
            raise

        finally:
            cursor.close()
            conn.close()

    def set_available(self,id:int,val:bool,member_id:str):
        conn = get_connection()
        cursor = conn.cursor()

        values = (val,member_id,id)
        sql = "UPDATE books SET is_available = %s ,borrowed_by_member_id = %s WHERE id = %s"

        try:
            cursor.execute(sql,values)
            conn.commit()

        except Exception as e:
            conn.rollback()
            raise

        finally:
            cursor.close()
            conn.close()        

    def count_total_books(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True) 

        sql = "SELECT COUNT(*) AS total_books FROM books"

        try:
            cursor.execute(sql)
            row = cursor.fetchone()
            return row # optional return row["total_books"] to return only the number as int
        
        finally:
            cursor.close()
            conn.close()

    def count_available_books(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT COUNT(*) as total_available FROM books WHERE is_available = TRUE"

        try:
            cursor.execute(sql)
            row = cursor.fetchone() # the same idea as the previous method
            return row
        
        finally:
            cursor.close()
            conn.close()


    def count_borrowed_books(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT COUNT(*) AS count_borrowed FROM BOOKS WHERE is_available = FALSE"
        
        try:
            cursor.execute(sql)
            row = cursor.fetchone()
            return row
        
        finally:
            cursor.close()
            conn.close()


    def count_by_genre(self,genre):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT COUNT(*) AS count_genre FROM books WHERE genre = %s"

        try:
            cursor.execute(sql,(genre,))
            row = cursor.fetchone()
            return row
        
        finally:
            cursor.close()
            conn.close()


    def count_active_borrows_by_member(self,member_id:int):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
        SELECT COUNT(*) AS total_active
        FROM books 
        WHERE borrowed_by_member_id = %s
        """
        try:
            cursor.execute(sql,(member_id,))
            row = cursor.fetchone()
            return row["total_active"]
        
        finally:
            cursor.close()
            conn.close()