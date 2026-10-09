import re

with open("main.py", "r") as f:
    content = f.read()

dynamic_logic = """    # INTERCEPT FOR DEMO FORM
    user_messages = [m.content for m in query.messages if m.role == 'user']
    latest_query = user_messages[-1].lower() if user_messages else ""
    
    if len(user_messages) == 1:
        fields = []
        if "passport" in latest_query:
            fields = [
                {"name": "State", "options": ["Andhra Pradesh", "Telangana", "Other Location"]},
                {"name": "Application type", "options": ["New Application", "Existing Application"]}
            ]
        elif "pan" in latest_query:
            fields = [
                {"name": "Applicant Category", "options": ["Individual", "Foreign Citizen", "Company/Trust"]},
                {"name": "Application Type", "options": ["New PAN", "Correction/Update in PAN"]}
            ]
        
        if fields:
            return {
                "type": "form",
                "text": "Great! To give you the right guidance, I need a few details.",
                "fields": fields
            }

    history_str = "\\n".join([f"{m.role}: {m.content}" for m in query.messages])"""

content = re.sub(
    r"    history_str = \"\\n\"\.join\(\[f\"\{m\.role\}: \{m\.content\}\" for m in query\.messages\]\)",
    dynamic_logic,
    content
)

with open("main.py", "w") as f:
    f.write(content)

print("Backend patched successfully")
