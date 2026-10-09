import sys

with open("main.py", "r") as f:
    lines = f.readlines()

auth_code = """
import sqlite3
import hashlib

class AuthRequest(BaseModel):
    email: str
    password: str

def init_db():
    conn = sqlite3.connect("data/users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

init_db()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@app.post("/api/signup")
def signup(req: AuthRequest):
    conn = sqlite3.connect("data/users.db")
    c = conn.cursor()
    c.execute("SELECT email FROM users WHERE email=?", (req.email,))
    if c.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Email already registered")
    c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (req.email, hash_password(req.password)))
    conn.commit()
    conn.close()
    return {"message": "User created successfully", "token": "token_" + req.email, "email": req.email}

@app.post("/api/login")
def login(req: AuthRequest):
    conn = sqlite3.connect("data/users.db")
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE email=?", (req.email,))
    row = c.fetchone()
    conn.close()
    if not row or row[0] != hash_password(req.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"message": "Login successful", "token": "token_" + req.email, "email": req.email}
"""

# Insert auth_code before class Message(BaseModel):
for i, line in enumerate(lines):
    if line.startswith("class Message(BaseModel):"):
        lines.insert(i, auth_code + "\n")
        break

with open("main.py", "w") as f:
    f.writelines(lines)
