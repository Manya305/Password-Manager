import sqlite3
import hashlib

def create_db():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS passwords
                 (service_hash TEXT, username_hash TEXT, password TEXT)''')
    conn.commit()
    conn.close()

def hash_string(string):
    return hashlib.sha256(string.encode()).hexdigest()

def add_password(service, username, password):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    service_hash = hash_string(service)
    username_hash = hash_string(username)
    c.execute("INSERT INTO passwords (service_hash, username_hash, password) VALUES (?, ?, ?)", (service_hash, username_hash, password))
    conn.commit()
    conn.close()

def get_password(service):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    service_hash = hash_string(service)
    c.execute("SELECT username_hash, password FROM passwords WHERE service_hash=?", (service_hash,))
    result = c.fetchone()
    conn.close()
    return result
