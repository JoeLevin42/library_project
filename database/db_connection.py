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
        borrowed_by_member_id VARCAHR(50) DEFAULT NULL
        )   
         """
    cursor.execute(sql_promt_books)

    sql_promt_members = """
         USE library_db; CREATE TABLE IF NOT EXISTS members (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(50) NOT NULL,
        email UNIQ NOT NULL,
        is_active BOOLEAN NOT NULL,
        total_borrows INT NOT NULL
        )
    """
    
    cursor.execute(sql_promt_members)
    
    cursor.close()
    conn.close()

    return {}


