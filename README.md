# library_project

## DESCRIPTION:

### The code for run conatiner in the docker:

## create_new_container:

docker run --name mysql-library -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -d mysql:8

## create database:

CREATE DATABASE library_db;

## create table books:

USE library_db;\
CREATE TABLE IF NOT EXISTS books ( \
    id INT PRIMARY KEY AUTO_INCREMENT, \
    title VARCHAR(50) NOT NULL, \
    author VARCHAR(50) NOT NULL, \
    genre ENUM('Fiction','Non-Fiction','Science','History','Other'), \
    is_availible BOOLEAN DEFAULT TRUE, \
    borrowed_by_member_id VARCAHR(50) DEFAULT NULL \
);


## create table members

USE library_db;
CREATE TABLE IF NOT EXISTS members ( \
    id INT PRIMARY KEY AUTO_INCREMENT, \
    name VARCHAR(50) NOT NULL, \
    email UNIQ NOT NULL, \
    is_active BOOLEAN NOT NULL, \
    total_borrows INT NOT NULL \
    );

## Fodlers structure:

```
library-api/
│
├── app/
│ ├── main.py
│ ├── database/
│ │ ├── db_connection.py
│ │ ├── book_db.py
│ │ └── member_db.py
│ ├── routes/
│ │ ├── book_routes.py
│ │ ├── member_routes.py
│ │ └── report_routes.py
│ └── logs/
│ └── app.log
│
├── README.md
├── requirements.txt
└── .gitignore  
```

## Books table (sql) description:

- **id** : int  this is primary key
- **title** : this is varcahr with max 50 chars
- **author** : the author name varchar max 50 chars
- **genre** : ENUM type (Other,Histroy,Science,Non-Fiction,Fiction)
- **is_borrowed** : bool if the book is availible
- **borrowed_by** : the member that hold this book , null if availible

## Memebrs table (sql) description:

- **id** : int primary key
- **name** : varchar max 50 , name of the member
- **email** : uniq not null , the member email
- **is_active** : bool , if the member active , if false he cant borrow
- **total_borrows** : total 

## database python model:

- **get_connection** : connects to mysql
- **create_tables** : creating the book and the members tables in start of the main func


## class BookDB:

- **create_book(data)** : its create new book and insert to the table , DEFAULT , is_availible = True, borrowed_by=NULL.
- **get_all_books()** : returns list of all the books
- **get_book_by_id(id)** : returns one book by id , if not or none if not exists
- **update_book(id,data)** : updates in the table the field that sends by id
- **set_availible(id,val,member_id)** : updates the is_availible and borrowed_by_member_id
- **count_total_books()** : counts and returns all the book in the database
- **count_availible_books()** : count all the books where is_availible = True
- **count_borrowed_books()** : count all the books where is_availible = False
- **count_by_genre(genre)** : counts all the books with this specific genre
- **count_active_borrows_by_member(member_id)** : counts how much books the memebers holds right now (force unitl 7) , count wiht borroed_by_member_id and compare to meber_id


## class MemeberDB:

-**create_member(data)** : insert to members , DEFAULT :  is_active=True,total_borroes=0
-**get_all_members()** : returns list of all the members without any filter
-**get_member_by_id(id)** : returns one member by the id , or none if not exists
-**update_member(id,data)** : updates the member by the fields that sends
-**deactive_member(id)** : updates that is_active = False to this member
-**active_member(id)** : updates the member is_active =True
-**increment_borrows(id)** : icrements the borrows by one
-**count_active_members()** : counts all the active members where is_active = True
-**get_top_member()** : its returns the member with the highest total_borrows


## System rules:

-**create new book** : The user sends the title/author/genre , and the system adds is_availible=True , borrowed_by = NULL (by default)
-**genre** : have to be one of the legitime options (ENUM) (Fiction / Non-Fiction / Science / History / Other)
every another values raises an error , need to validate in create(POST) and in update(PATCH/PUT)

- **create member** : The user sends name/email  , The system adds is_active=True, total_borrows = 0 (by default)

- **email** : Have to be uniq , if already exists raise an error

- **unactive member** : if is_active = False he cant to borrow book

- **unavailible book** : impossible to borrow book that already borrowed (is_availible=False)

- **maximun books** : member cant to hold more than tree books in one time

- **return book** : it possible to return book only to the member that holds it right now

## Logging format: 
```
time | level | message

2026-06-07 10:30:12 | INFO | POST /books called
2026-06-07 10:30:13 | ERROR | Book not found: 42
2026-06-07 10:30:14 | INFO | Book 42 borrowed by member 7
```

time | level | message
דוגמאות:
2026-06-07 10:30:12 | INFO | POST /books called
2026-06-07 10:30:13 | ERROR | Book not found: 42
2026-06-07 10:30:14 | INFO | Book 42 borrowed by member 7

### Most to right log:
- Log in every start if **REST**
- Log before update to **SQL**
- Log when **ERROR**
- Log in the end of **REST**


## Endpoints:

### BOOKS

- **POST** /books : create book
- **GET** /books : give all the books
- **GET** /book/{id} : return book by id
- **PATCH** /book/{id} : updates book
- **PATCH** /book/{id}/borrow/{member_id} : borrow book to member
- **PATCH** /book/{id}/return/{member_id} : return book to the library from member

### Members

- **POST** /members : create member
- **GET** /members : returns all the members
- **GET** /members/{id} : returns one member by id
- **PATCH** /members/{id} : update member
 - **PATCH** /members/{id}/deactivate : deactivate member
 - **PATCH** /members/{id}/activate : active member

### Reports:

- **GET** /reports/summary : retuns summary report 
- **GET** /reports/books-by-genre : returns books by genre
- **GET** /reports/top-member : retunrs the most active member (most borrows)


## Reports Foramt Example:

### /reports/summary

- total books
- total availible books
- total borrowed books now
- total active members

#### example:
```
}
"total_books": 0,
"available_books": 0,
"currently_borrowed": 0,
"active_members": 0
}
```

### reports/books/by-genre

#### example:

```
[
{"Genre": "Science", "COUNT": 3},
{"Genre": "History", "COUNT": 2}
]
```

### reports/top-member

```
{
"member_id": 1,
"borrowed": 5
}
```

## Validations and tests:

### LEVEL 1 - CREATE MEMBER:

```
POST /members
{
"name": "Sara Cohen",
"email": "sara@example.com"
}
```

### LEVEL 2 CREATE BOOK:

```
POST /books
{
"title": "The Hitchhiker's Guide to the Galaxy",
"author": "Douglas Adams",
"genre": "Fiction"
}
```


### LEVEL 3 BORROW BOOK:

```
PUT /books/{id}/borrow/{member_id}
```
- then valid that:

```
is_available = False
borrowed_by_member_id = member_id
total_borrows + 1
```

### Faliures:

- **CHECK** : book exists | ***IF FALIS**
: 404 Book not found
- **CHECK** : member exists| ***IF FALIS** : 404 Member not found
- **CHECK** : is book availible| ***IF FALIS** : 400 Book is not availible
- **CHECK** : is member active| ***IF FALIS** : 400 Member is not active
- **CHECK** : members holds less than tree| ***IF FALIS** : 400 Member has reached maximum borrows

### LEVEL 4 - RETURN BOOK:

```
PUT /books/{id}/return/{member_id}
```

- after successfull return check:
```
is_available = True
borrowed_by_member_id = NULL
total_borrows , not changed
```

### Faliures:

- **CHECK**: The book exists | **IF FAILS**: 404 Book not found
- **CHECK**: The member exists| **IF FAILS**: 404 Member not found
- **CHECK**: The book is borrowed right now| **IF FAILS** : 400 Book is not borrowed 
- **CHECK**: Book is borrowed to the same friend that returns it (rule 8)| **IF FAILS**: 400 Book is not borrowed by this member
