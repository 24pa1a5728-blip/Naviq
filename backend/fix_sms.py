import re

with open("main.py", "r") as f:
    content = f.read()

# First remove the old broken send_sms block
content = re.sub(r"@app\.post\(\"/api/sms\"\).*?return \{\"message\": \"SMS dispatched successfully\"\}", "", content, flags=re.DOTALL)

# Now add the proper Twilio block before `class Message(BaseModel):`
new_sms_code = """
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
            print(f"❌ FAILED TO SEND REAL SMS: {e}")
            raise HTTPException(status_code=500, detail="Failed to send real SMS via Twilio.")
    else:
        # Fallback to Mock
        print("\\n" + "="*50)
        print(f"📱 MOCK SECURITY SMS ALERT SENT TO: {req.phone}")
        print("-" * 50)
        print(f"{req.message}")
        print("="*50 + "\\n")
        return {"message": "Mock SMS dispatched successfully"}

"""

content = content.replace("class Message(BaseModel):", new_sms_code + "class Message(BaseModel):")

with open("main.py", "w") as f:
    f.write(content)

