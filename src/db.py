import os
import sqlite3

# From: https://goo.gl/YzypOI
def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


class DatabaseDriver(object):
    """
    Database driver for the Task app.
    Handles with reading and writing data with the database.
    
    """

    def __init__(self):
        """
        Secures a connection with the database and stores it into the instance variable 'conn'
        """
        self.conn = sqlite3.connect(
            "users.db", check_same_thread= False
        )

    def create_users_table(self):
        """
        Using SQL, create users table with NULL balance.
        """
        self.conn.execute("""
                          CREATE TABLE IF NOT EXISTS users(
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT NOT NULL,
                          username TEXT NOT NULL,
                          balance INTEGER DEFAULT 0
                          );
                          """)
        
    def delete_users_table(self):
        """
        Using SQL, delete the users table
        """
        self.conn.execute("DROP TABLE IF EXISTS users;")
    
    def get_all_users(self):
        """
        Using SQL, get all users in the table users.
        """
        cursor = self.conn.execute("SELECT * FROM users;")
        users = []
        for row in cursor:
            users.append({"id": row[0],"name": row[1], "username": row[2], "balance": row[3]})

        return users
    
    def get_specific_user(self,id):
        """
        Using SQL, get a user by its id.
        """
        cursor = self.conn.execute("SELECT * FROM users WHERE id = ?;",(id,))
        for row in cursor:
            return {"id": row[0],"name": row[1], "username": row[2], "balance" : row[3]}
        return None

    def create_new_user(self,name,username,balance=0):
        """
        Using SQL, add a new user to the table users.
        """
        cursor = self.conn.execute("INSERT INTO users (name,username,balance) VALUES (?,?,?);" , (name,username,balance))
        self.conn.commit()
        return cursor.lastrowid
    
    def update_users_balance(self,sender_id,sender_afterb,receiver_id,receiver_afterb):
        """
        Using SQL, update the table users after a transaction has been made.
        Substract from the sender's balance and add to the reciever's.
        """
        self.conn.execute("""
            UPDATE users
            SET balance = ?
            WHERE id = ?
            """, (sender_afterb, sender_id))

        self.conn.execute("""
            UPDATE users
            SET balance = ?
            WHERE id = ?
            """, (receiver_afterb, receiver_id))

        self.conn.commit()

    def delete_user(self,id):
        """
        Using SQL, delete a user from users.
        """
        self.conn.execute("""
            DELETE FROM users
            WHERE id = ?;
        """, (id,))

# Only <=1 instance of the database driver
# exists within the app at all times
DatabaseDriver = singleton(DatabaseDriver)
