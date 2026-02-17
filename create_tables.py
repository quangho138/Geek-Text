"""
POSTGRES DATABASE DRAFT

Within your virtual environment, run:

pip install psycopg2-binary
pip install python-dotenv

 - make sure you have a .env file that contains the connection info (db_name, db_user, etc.) below
 - make sure you created the database already (CREATE DATABASE <dbname>;) within postgres
"""


import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()  # reads the .env file and sets the variables

db_name= os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_port = os.getenv("DB_PORT")


def create_tables():
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host="localhost",
        port=db_port
    )
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("""
                
        CREATE TABLE IF NOT EXISTS Publisher (
            id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            name VARCHAR(150)
        );
        -- Can be removed and placed with either the Book or Author instead


                
        CREATE TABLE IF NOT EXISTS Book ( 
            id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            isbn VARCHAR(13) UNIQUE,
            name VARCHAR(32) NOT NULL,
            description VARCHAR(255),
            price NUMERIC(10, 2) NOT NULL,
            genre VARCHAR(24),
            year_published INT,
            publisher_id INTEGER NOT NULL,
            FOREIGN KEY (publisher_id) REFERENCES Publisher(id)
        );

        -- number of copies a book sold is a calculated attribute from the AuthorBook table

                
        CREATE TABLE IF NOT EXISTS Author (
            id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(150) NOT NULL,
            biography VARCHAR(255)
                
            -- Relationship between authors and publishers is indirect through the Book table
        );
                

                


                
        CREATE TABLE IF NOT EXISTS AuthorBook (
            author_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            
            FOREIGN KEY (author_id) REFERENCES Author(id) ON DELETE CASCADE,
            FOREIGN KEY (book_id) REFERENCES Book(id) ON DELETE CASCADE,
            PRIMARY KEY (author_id, book_id)
        );  
         -- If we completely removed this table and added author_id as a foreign key in the Book table, then that would mean that ONLY 1 author can create 1 book. 
         -- That means 2 or more authors can't work on the same book. So, we can remove this table if we're planning on making only 1 author own a book.



        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            username VARCHAR(150) NOT NULL UNIQUE,
            password TEXT NOT NULL,
            first_name VARCHAR(150),
            last_name VARCHAR(150),
            email TEXT UNIQUE,
            home_address TEXT
        );



        -- Orders are needed for the Book Reviews portion since it states a user can only review a book they purchased. 
        -- So this keeps track of order ids. And OrderItem keeps track of the books a user actually purchased.
                
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            total_price NUMERIC(10, 2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            status TEXT,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(id)
        );


        CREATE TABLE IF NOT EXISTS OrderItem (
            order_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            quantity INT,
            price_at_purchase NUMERIC(10, 2) NOT NULL,

            CONSTRAINT check_QuantityGreaterThanZero CHECK (quantity > 0),
            FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
            FOREIGN KEY (book_id) REFERENCES Book(id) ON DELETE CASCADE,
            PRIMARY KEY (order_id, book_id)
        );

        
        
        CREATE TABLE IF NOT EXISTS CartItem (
            id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            user_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            quantity INT,

            CONSTRAINT check_QuantityGreaterThanZero CHECK (quantity > 0),
            CONSTRAINT unique_user_book UNIQUE (user_id, book_id),
            
            FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
            FOREIGN KEY (book_id) REFERENCES Book(id) ON DELETE CASCADE
        );
        -- get unit price, book title, and author by doing a JOIN query with Book and Author



        CREATE TABLE IF NOT EXISTS CreditCard (
            id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            user_id INTEGER NOT NULL,
            card_number VARCHAR(32) NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
        );


        CREATE TABLE IF NOT EXISTS Wishlist (
            id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            user_id INTEGER NOT NULL,
            name VARCHAR(50) NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
            UNIQUE (user_id, name) -- a single user can't create 2 wishlists with the same name

            -- A user cannot have more than 3 wishlists. This must be enforced through application logic
        );
                


        CREATE TABLE IF NOT EXISTS WishlistItem (
            wishlist_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            FOREIGN KEY (wishlist_id) REFERENCES Wishlist(id) ON DELETE CASCADE,
            FOREIGN KEY (book_id) REFERENCES Book(id) ON DELETE CASCADE,
            PRIMARY KEY (wishlist_id, book_id)
        );



        -- users can only create 1 review per book

        CREATE TABLE IF NOT EXISTS Review (
            id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            user_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            rating INTEGER CHECK (rating BETWEEN 1 AND 5),
            comment VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                
            CONSTRAINT unique_review_user_book UNIQUE (user_id, book_id),
            FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
            FOREIGN KEY (book_id) REFERENCES Book(id) ON DELETE CASCADE
        );
    """)

    print("All tables created successfully.")
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_tables()
