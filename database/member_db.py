from db_connection import get_connection

class MemberDB:
    def __init__(self):
        pass

    def create_member(self,data:dict):
        conn = get_connection()
        cursor = conn.cursor()

        columns_parts = [f"`{key}`" for key in data.keys()]
        columns_str = ", ".join(columns_parts)
        place_holders = ", ".join(["%s"]*len(columns_parts))
        values = tuple(data.values())
        sql_promt = f"INSERT INTO members ({columns_str}) VALUES ({place_holders})"

        cursor.execute(sql_promt,values)
        conn.commit()

        cursor.close()
        conn.close()

        #mybe its will be a good idea to retunr the lastrowid 
        
    def get_all_members(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT * FROM members"
        cursor.execute(sql)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()
        
        return rows


    def get_member_by_id(self,id:int):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT * FROM members WHERE id = %s"
        cursor.execute(sql,(id,))

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return row
    
    def update_member(self,id:int,data:dict):
        conn = get_connection()
        cursor = conn.cursor()

        columns_parts = [f"`{key}`=%s" for key in data.keys()]
        columns_str = ", ".join(columns_parts)
        values = tuple(data.values()) + (id,) # the id is the last

        sql_promt = f"UPDATE members SET {columns_str} WHERE id = %s" # id have to be last

        cursor.execute(sql_promt,values)
        conn.commit()

        cursor.close()
        conn.close()


    def deactivate_member(self,id:int):
        conn = get_connection()
        cursor = conn.cursor()

        sql_promt = "UPDATE members SET is_active = TRUE WHERE id = %s"
        cursor.execute(sql_promt,(id,))
        conn.commit()

        cursor.close()
        conn.close()


    def active_member(self,id:int):
        conn = get_connection()
        cursor = conn.cursor()

        sql_promt = "UPDATE members SET is_active = FALSE WHERE id = %s"
        cursor.execute(sql_promt,(id,))
        conn.commit()

        cursor.close()
        conn.close()


    def increment_borrows(self,id:int):
        conn = get_connection()
        cursor = conn.cursor()

        sql_promt = "UPDATE members SET total_borrows = total_borrows+1 WHERE id = %s"
        cursor.execute(sql_promt,(id,))
        conn.commit()

        cursor.close()
        conn.close()
        

    def count_active_members(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql_promt = "SELECT COUNT(*) FROM members WHERE is_active = TRUE"
        cursor.execute(sql_promt)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows
    
    def get_top_member(self):
        conn = get_connection()
        cursor = conn.cursor()

        sql_promt_max = "SELECT MAX(total_borrows) FROM members"
        cursor.execute(sql_promt_max)
        max_number = cursor.fetchone()[0]

        sql_promt_main = "SELECT * FROM members WHERE total_borrows =%s"
        cursor.execute(sql_promt_main,(max_number,))

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows