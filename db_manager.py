import sqlite3
import hashlib
from datetime import datetime
import shutil

def create_db():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS passwords
                 (service_hash TEXT, username_hash TEXT, password TEXT, creation_date TEXT)''')
    conn.commit()
    conn.close()

def hash_string(string):
    return hashlib.sha256(string.encode()).hexdigest()

def add_password(service, username, password):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    service_hash = hash_string(service)
    username_hash = hash_string(username)
    creation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO passwords (service_hash, username_hash, password, creation_date) VALUES (?, ?, ?, ?)", 
              (service_hash, username_hash, password, creation_date))
    conn.commit()
    conn.close()

def get_password(service):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    service_hash = hash_string(service)
    c.execute("SELECT username_hash, password, creation_date FROM passwords WHERE service_hash=?", (service_hash,))
    result = c.fetchone()
    conn.close()
    return result

def get_all_passwords():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("SELECT service_hash, username_hash, creation_date FROM passwords")
    results = c.fetchall()
    conn.close()
    return results

def search_passwords(query):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("SELECT service_hash, username_hash FROM passwords WHERE service_hash LIKE ?", ('%' + query + '%',))
    results = c.fetchall()
    conn.close()
    return results

def backup_database(backup_path):
    shutil.copy('passwords.db', backup_path)
    shutil.copy('secret.key', backup_path)
    print("Backup completed.")

def restore_database(backup_path):
    shutil.copy(f'{backup_path}/passwords.db', '.')
    shutil.copy(f'{backup_path}/secret.key', '.')
    print("Restore completed.")
