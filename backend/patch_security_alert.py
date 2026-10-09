import re

with open("main.py", "r") as f:
    content = f.read()

# We want to extract the email sending logic into a helper function so it can be called internally
helper_func = """
def send_email_helper(to_email: str, subject: str, body: str):
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")
    if smtp_email and smtp_password:
        try:
            msg = MIMEMultipart()
            msg['From'] = smtp_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.send_message(msg)
            server.quit()
            print(f"✅ REAL EMAIL SENT TO: {to_email}")
        except Exception as e:
            print(f"❌ FAILED TO SEND REAL EMAIL: {e}")
    else:
        print("\\n" + "="*50)
        print(f"📧 MOCK EMAIL SENT TO: {to_email}")
        print(f"SUBJECT: {subject}")
        print("-" * 50)
        print(f"{body}")
        print("="*50 + "\\n")
"""

# Add the helper function
content = content.replace("class EmailRequest(BaseModel):", helper_func + "\nclass EmailRequest(BaseModel):")

# Update /api/email to use the helper
old_email_endpoint_pattern = r"@app\.post\(\"/api/email\"\)\ndef send_email\(req: EmailRequest\):.*?(?=@app\.post\(\"/api/sms\"\))"
new_email_endpoint = """@app.post("/api/email")
def send_email_api(req: EmailRequest):
    send_email_helper(req.email, req.subject, req.body)
    return {"message": "Email request processed"}
"""
content = re.sub(old_email_endpoint_pattern, new_email_endpoint, content, flags=re.DOTALL)

# Add security alert to login
old_login = """@app.post("/api/login")
def login(req: AuthRequest):
    conn = sqlite3.connect("data/users.db")
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE email=?", (req.email,))
    row = c.fetchone()
    conn.close()
    if not row or row[0] != hash_password(req.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"message": "Login successful", "token": "token_" + req.email, "email": req.email}"""

new_login = """@app.post("/api/login")
def login(req: AuthRequest):
    conn = sqlite3.connect("data/users.db")
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE email=?", (req.email,))
    row = c.fetchone()
    conn.close()
    if not row or row[0] != hash_password(req.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Send Security Alert
    import threading
    alert_subject = "🚨 Security Alert: New Login to Naviq"
    alert_body = f"Hello,\\n\\nA new login was just detected on your Naviq account ({req.email}).\\nIf this was you, no action is needed.\\nIf this was not you, please secure your account immediately.\\n\\n- Naviq Security Team"
    threading.Thread(target=send_email_helper, args=(req.email, alert_subject, alert_body)).start()

    return {"message": "Login successful", "token": "token_" + req.email, "email": req.email}"""

content = content.replace(old_login, new_login)

with open("main.py", "w") as f:
    f.write(content)

print("Security alert patched.")
