import re

with open("main.py", "r") as f:
    content = f.read()

dynamic_form_logic = """
    user_messages = [m.content for m in req.messages if m.role == 'user']
    if not user_messages:
        raise HTTPException(status_code=400, detail="No user messages provided")
        
    latest_query = user_messages[-1].lower()

    # Dynamic Form Injection for Prototype
    if len(user_messages) == 1:
        fields = []
        if "passport" in latest_query:
            fields = [
                {"name": "Applicant Type", "options": ["Adult (18+)", "Minor (Under 18)"]},
                {"name": "Application Type", "options": ["Fresh Passport", "Re-issue of Passport"]},
                {"name": "Employment Type", "options": ["Private", "Government/PSU", "Student", "Other"]}
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
                {"name": "Application Type", "options": ["New Voter Registration", "Correction of Details", "Shifted to new constituency"]}
            ]
        
        # Only return form if we mapped fields
        if fields:
            return {
                "type": "form",
                "text": "Great! To give you the right guidance, I need a few details.",
                "fields": fields
            }

    try:
"""

content = re.sub(
    r"def generate_plan\(req: Query\):\n\s*try:",
    "def generate_plan(req: Query):\n" + dynamic_form_logic,
    content
)

with open("main.py", "w") as f:
    f.write(content)

print("Dynamic form logic added to main.py")
