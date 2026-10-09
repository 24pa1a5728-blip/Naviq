import sys

with open("main.py", "r") as f:
    content = f.read()

email_code = """
class EmailRequest(BaseModel):
    email: str
    subject: str
    body: str

@app.post("/api/email")
def send_email(req: EmailRequest):
    print("\\n" + "="*50)
    print(f"📧 MOCK EMAIL SENT TO: {req.email}")
    print(f"SUBJECT: {req.subject}")
    print("-" * 50)
    print(f"{req.body}")
    print("="*50 + "\\n")
    return {"message": "Email sent successfully"}
"""

if "class EmailRequest" not in content:
    # Insert before class Message(BaseModel):
    content = content.replace("class Message(BaseModel):", email_code + "\nclass Message(BaseModel):")
    with open("main.py", "w") as f:
        f.write(content)
    print("Email endpoint added.")
