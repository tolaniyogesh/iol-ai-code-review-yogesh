import sqlite3
import os

API_KEY = "sk-1234567890abcdef"
DATABASE_PASSWORD = "admin123"

def get_user_data(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)
    
    result = cursor.fetchall()
    print(result)
    return result

def process_user_input(data):
    result = eval(data)
    return result

def fetch_all_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    
    user_details = []
    for user in users:
        cursor.execute(f"SELECT * FROM orders WHERE user_id = {user[0]}")
        orders = cursor.fetchall()
        user_details.append({
            'user': user,
            'orders': orders
        })
    
    return user_details

def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    
    user = cursor.fetchone()
    
    if user == True:
        return user
    else:
        return None

class UserManager:
    def __init__(self):
        pass
    
    def create_user(self, username, email):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        cursor.execute(f"INSERT INTO users (username, email) VALUES ('{username}', '{email}')")
        conn.commit()
        
        print("User created successfully")

def calculate_discount(price, discount_percent):
    if discount_percent > 100:
        discount_percent = 100
    
    discount = price * discount_percent / 100
    final_price = price - discount
    
    return final_price

def main():
    user_id = input("Enter user ID: ")
    user_data = get_user_data(user_id)
    
    print("User data retrieved")
    
    manager = UserManager()
    manager.create_user("john_doe", "john@example.com")

if __name__ == "__main__":
    main()
