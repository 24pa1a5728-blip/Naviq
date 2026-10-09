import re

with open("main.py", "r") as f:
    content = f.read()

dynamic_form_logic = """
    user_messages = [m.content for m in req.messages if m.role == 'user']
    if not user_messages:
        raise HTTPException(status_code=400, detail="No user messages provided")
        
    latest_query = user_messages[-1].lower()

    if len(user_messages) == 1:
        fields = []
        if "passport" in latest_query:
            fields = [
                {"name": "Applicant type", "options": ["Indian Citizen", "NRI", "Foreign National"]},
                {"name": "State / Location", "options": ["Andhra Pradesh", "Telangana", "Maharashtra", "Delhi"]}
            ]
        elif "pan" in latest_query:
            fields = [
                {"name": "Applicant Category", "options": ["Individual (Indian Citizen)", "Foreign Citizen", "Company/Trust"]},
                {"name": "Application Type", "options": ["New PAN", "Correction/Update in PAN"]}
            ]
        elif "driving" in latest_query or "licence" in latest_query or "license" in latest_query:
            fields = [
                {"name": "License Type", "options": ["Learner's License", "Permanent License", "Renewal"]},
                {"name": "Vehicle Class", "options": ["Motorcycle (2-wheeler)", "Light Motor Vehicle (Car)", "Transport Vehicle"]}
            ]
        elif "voter" in latest_query:
            fields = [
                {"name": "Application Type", "options": ["New Voter Registration", "Correction of Details", "Shifted to new constituency"]},
                {"name": "State / Location", "options": ["Andhra Pradesh", "Telangana", "Maharashtra", "Delhi"]}
            ]
        else:
            fields = [
                {"name": "Applicant type", "options": ["Individual", "Business/Organization"]},
                {"name": "State / Location", "options": ["Andhra Pradesh", "Telangana", "Maharashtra", "Delhi", "Other"]}
            ]
            
        if fields:
            return {
                "type": "form",
                "text": "Great! To give you the right guidance, I need a few details.",
                "fields": fields
            }

    try:
"""

# Replace from `user_messages = [m.content` up to `try:`
content = re.sub(
    r"    user_messages = \[m\.content.*?try:",
    dynamic_form_logic.strip() + "\n\n    try:",
    content,
    flags=re.DOTALL
)

with open("main.py", "w") as f:
    f.write(content)

print("Dynamic form restored with Passport matching prototype!")
