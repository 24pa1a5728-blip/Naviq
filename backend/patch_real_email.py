import sys

with open("main.py", "r") as f:
    content = f.read()

real_email_code = """
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailRequest(BaseModel):
    email: str
    subject: str
    body: str

@app.post("/api/email")
def send_email(req: EmailRequest):
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")
    
    if smtp_email and smtp_password:
        try:
            msg = MIMEMultipart()
            msg['From'] = smtp_email
            msg['To'] = req.email
            msg['Subject'] = req.subject
            msg.attach(MIMEText(req.body, 'plain'))
            
            # Using Gmail SMTP as default
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.send_message(msg)
            server.quit()
            print(f"✅ REAL EMAIL SENT TO: {req.email}")
            return {"message": "Email sent successfully"}
        except Exception as e:
            print(f"❌ FAILED TO SEND REAL EMAIL: {e}")
            raise HTTPException(status_code=500, detail="Failed to send email.")
    else:
        # Fallback to Mock
        print("\\n" + "="*50)
        print(f"📧 MOCK EMAIL SENT TO: {req.email}")
        print(f"SUBJECT: {req.subject}")
        print("-" * 50)
        print(f"{req.body}")
        print("="*50 + "\\n")
        return {"message": "Mock Email sent successfully"}
"""

# We need to replace the old send_email function with the new one.
# Since it's easier, we will just use regex to replace the old block.
import re
new_content = re.sub(
    r"class EmailRequest\(BaseModel\):.*?return \{\"message\": \"Email sent successfully\"\}",
    real_email_code.strip(),
    content,
    flags=re.DOTALL
)

with open("main.py", "w") as f:
    f.write(new_content)
print("Real email fallback patched.")
