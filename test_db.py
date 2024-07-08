from db_manager import create_db, add_password, get_password

def test_db():
    # Initialize the database
    create_db()
    
    # Test adding a password
    service = "example.com"
    username = "user1"
    password = "password123"
    add_password(service, username, password)
    print("Password added successfully.")
    
    # Test retrieving a password
    result = get_password(service)
    if result:
        print(f"Retrieved username: {result[0]}")
        print(f"Retrieved password: {result[1]}")
    else:
        print("Service not found.")

if __name__ == "__main__":
    test_db()
