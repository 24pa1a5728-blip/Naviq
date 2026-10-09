import re

with open("main.py", "r") as f:
    content = f.read()

# I will find the start of send_email_helper and the start of class Message(BaseModel):
# and replace everything in between with the correct implementations of both!

start_marker = "def send_email_helper(to_email: str, subject: str, body: str):"
end_marker = "class Message(BaseModel):"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

correct_code = """def send_email_helper(to_email: str, subject: str, body: str):
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

class EmailRequest(BaseModel):
    email: str
    subject: str
    body: str

@app.post("/api/email")
def send_email_api(req: EmailRequest):
    send_email_helper(req.email, req.subject, req.body)
    return {"message": "Email request processed"}

import os
from twilio.rest import Client

class SMSRequest(BaseModel):
    phone: str
    message: str

@app.post("/api/sms")
def send_sms(req: SMSRequest):
    twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
    twilio_auth = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_phone = os.getenv("TWILIO_PHONE_NUMBER")
    
    if twilio_sid and twilio_auth and twilio_phone:
        try:
            client = Client(twilio_sid, twilio_auth)
            message = client.messages.create(
                body=f"SECURITY ALERT: {req.message}",
                from_=twilio_phone,
                to=req.phone
            )
            print(f"✅ REAL SMS SENT VIA TWILIO TO: {req.phone} (SID: {message.sid})")
            return {"message": "Real SMS sent successfully"}
        except Exception as e:
            error_msg = str(e)
            print(f"❌ FAILED TO SEND REAL SMS: {error_msg}")
            if "trial accounts" in error_msg.lower():
                raise HTTPException(status_code=400, detail="Twilio Trial Account Error: You must use your Twilio Virtual Phone Number as the sender (not your personal number), and you can only send to verified phone numbers.")
            else:
                raise HTTPException(status_code=400, detail=f"Twilio Error: {error_msg}")
    else:
        # Fallback to Mock
        print("\\n" + "="*50)
        print(f"📱 MOCK SECURITY SMS ALERT SENT TO: {req.phone}")
        print("-" * 50)
        print(f"{req.message}")
        print("="*50 + "\\n")
        return {"message": "Mock SMS dispatched successfully"}

"""

new_content = content[:start_idx] + correct_code + content[end_idx:]

with open("main.py", "w") as f:
    f.write(new_content)

print("Fixed communication APIs!")
