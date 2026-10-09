import re

with open("main.py", "r") as f:
    content = f.read()

sms_code = """
class SMSRequest(BaseModel):
    phone: str
    message: str

@app.post("/api/sms")
def send_sms(req: SMSRequest):
    print("\\n" + "="*50)
    print(f"📱 MOCK SMS SENT TO: {req.phone}")
    print("-" * 50)
    print(f"{req.message}")
    print("="*50 + "\\n")
    return {"message": "SMS dispatched successfully"}
"""

if "class SMSRequest" not in content:
    content = content.replace("class Message(BaseModel):", sms_code + "\nclass Message(BaseModel):")
    with open("main.py", "w") as f:
        f.write(content)
    print("SMS endpoint added.")
