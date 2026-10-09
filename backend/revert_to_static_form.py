import re

with open("main.py", "r") as f:
    content = f.read()

# Replace the dynamic form logic with the static form logic
static_form_logic = """
    user_messages = [m.content for m in req.messages if m.role == 'user']
    if not user_messages:
        raise HTTPException(status_code=400, detail="No user messages provided")
        
    latest_query = user_messages[-1].lower()

    # Exact match with user's Figma prototype image
    if len(user_messages) == 1:
        fields = [
            {"name": "Applicant type", "options": ["Indian Citizen", "NRI", "Foreign National"]},
            {"name": "State / Location", "options": ["Andhra Pradesh", "Telangana", "Maharashtra", "Delhi"]}
        ]
        return {
            "type": "form",
            "text": "Great! To give you the right guidance, I need a few details.",
            "fields": fields
        }

    try:
"""

content = re.sub(
    r"    user_messages = \[m\.content.*?try:",
    static_form_logic.strip() + "\n\n    try:",
    content,
    flags=re.DOTALL
)

with open("main.py", "w") as f:
    f.write(content)

print("Reverted to static prototype form.")
