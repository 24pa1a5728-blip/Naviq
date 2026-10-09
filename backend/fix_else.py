import re
with open("main.py", "r") as f:
    content = f.read()

# Replace the whole else block
old_else = content.split("    else:")[1].split("class Message(BaseModel):")[0]

new_else = """
        # Fallback to Mock
        print("\\n" + "="*50)
        print(f"📧 MOCK EMAIL SENT TO: {req.email}")
        print(f"SUBJECT: {req.subject}")
        print("-" * 50)
        print(f"{req.body}")
        print("="*50 + "\\n")
        return {"message": "Mock Email sent successfully"}

"""

content = content.replace("    else:" + old_else, "    else:" + new_else + "\n\n")

with open("main.py", "w") as f:
    f.write(content)
