import re

with open("main.py", "r") as f:
    content = f.read()

# We need to replace the passport fields logic
old_passport_logic = """        if "passport" in latest_query:
            fields = [
                {"name": "Applicant type", "options": ["Indian Citizen", "NRI", "Foreign National"]},
                {"name": "State / Location", "options": ["Andhra Pradesh", "Telangana", "Maharashtra", "Delhi"]}
            ]"""

new_passport_logic = """        if "passport" in latest_query:
            fields = [
                {"name": "State", "options": ["Andhra Pradesh", "Telangana", "Other Location"]},
                {"name": "Application type", "options": ["New Application", "Existing Application"]}
            ]"""

content = content.replace(old_passport_logic, new_passport_logic)

with open("main.py", "w") as f:
    f.write(content)

print("Passport logic updated!")
