history_str_lower = "i need a passport\nhere are my details. state: andhra pradesh, application type: new application"

matched_id = None

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

print("Matched:", matched_id)
