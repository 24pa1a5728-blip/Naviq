import re

with open("main.py", "r") as f:
    content = f.read()

new_matching_logic = """    # Step A: Intent Matching
    matched_id = None
    
    # 1. Search full history for exact service ID
    history_str_lower = history_str.lower()
    for s in SERVICES_DB:
        if s["id"].replace("_", " ") in history_str_lower or s["id"].replace("_", "") in history_str_lower:
            matched_id = s["id"]
            break
            
    # 2. Search for specific strong keywords
    if not matched_id:
        if "passport" in history_str_lower: matched_id = "passport"
        elif "driving" in history_str_lower or "dl" in history_str_lower: matched_id = "driving_licence"
        elif "pan card" in history_str_lower or "pan" in history_str_lower: matched_id = "pan_card"
        elif "voter" in history_str_lower: matched_id = "voter_id"
        elif "ration" in history_str_lower: matched_id = "ration_card"
        elif "aadhaar" in history_str_lower: matched_id = "aadhaar_update"
        elif "birth" in history_str_lower: matched_id = "birth_certificate"
        elif "caste" in history_str_lower: matched_id = "caste_certificate"
        elif "income" in history_str_lower: matched_id = "income_certificate"
        elif "residence" in history_str_lower or "nativity" in history_str_lower: matched_id = "residence_certificate"

    # 3. Fallback to variants checking ONLY in the first message if still not found
    if not matched_id and query.messages:
        first_msg = query.messages[0].content.lower()
        for s in SERVICES_DB:
            if any(v in first_msg for v in s.get("variants", [])):
                matched_id = s["id"]
                break

    # If absolutely nothing matched, default to passport for demo
    if not matched_id:
        matched_id = "passport\"\"\"
"""

# The chunk to replace is between `user_latest = query.messages[-1]...` and `if not matched_id:`
# Actually let's just replace from `# Step A: Intent Matching` to `if not matched_id: raise HTTPException`
start_marker = "    # Step A: Intent Matching (Simple keyword for now, robust enough for demo)"
end_marker = "    if not matched_id:"
pattern = re.compile(re.escape(start_marker) + r".*?" + re.escape(end_marker), re.DOTALL)

def replace_logic(match):
    return new_matching_logic.strip() + "\n\n    if not matched_id:"

new_content = pattern.sub(replace_logic, content)

with open("main.py", "w") as f:
    f.write(new_content)

print("Intent matching logic updated successfully!")
