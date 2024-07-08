import subprocess
import os

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(result.stdout)

def test_password_manager():
    # Test adding a password
    print("Testing adding a password...")
    run_command('python main.py add --service example.com --username user1')
    
    # Test retrieving a password
    print("Testing retrieving a password...")
    run_command('python main.py get --service example.com')

    # Clean up
    if os.path.exists("passwords.db"):
        os.remove("passwords.db")
    if os.path.exists("secret.key"):
        os.remove("secret.key")

if __name__ == "__main__":
    test_password_manager()
