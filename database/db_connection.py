import mysql.connector as seqel

def get_connection():
    
    cnx = seqel.connect(
        host = "localhost",
        database = "library_db",
        user = "root",
        password = "root"
    )

    return cnx

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    sql_promt_books  = """
        CREATE TABLE IF NOT EXISTS books (
        id INT PRIMARY KEY AUTO_INCREMENT,
        title VARCHAR(50) NOT NULL,
        author VARCHAR(50) NOT NULL,
        genre ENUM('Fiction','Non-Fiction','Science','History','Other'),
        is_available BOOLEAN DEFAULT TRUE,
        borrowed_by_member_id INT DEFAULT NULL
        )   
         """
    cursor.execute(sql_promt_books)

    sql_promt_members = """
        CREATE TABLE IF NOT EXISTS members (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(50) NOT NULL,
        email VARCHAR(50) UNIQUE NOT NULL,
        is_active BOOLEAN NOT NULL DEFAULT TRUE,
        total_borrows INT NOT NULL DEFAULT 0
        )
    """
    
    cursor.execute(sql_promt_members)
    conn.commit()
    cursor.close()
    conn.close()

    


