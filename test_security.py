import sqlite3
API_KEY = "sk-1234567890abcdef"
PASSWORD = "admin123"
def get_user(user_id):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    
    # SQL injection vulnerability - should be flagged
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)
    
    return cursor.fetchone()

# Using eval - should be flagged
def process_input(data):
    return eval(data)

if __name__ == "__main__":
    print("Test file")
