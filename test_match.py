import json
with open("backend/data/services.json", "r") as f:
    SERVICES_DB = json.load(f)

user_latest = "here are my details. state: andhra pradesh, application type: new application"
history_str = "i need a passport\nhere are my details. state: andhra pradesh, application type: new application"

matched_id = None
for s in SERVICES_DB:
    if s["id"].replace("_", " ") in user_latest or any(v in user_latest for v in s.get("variants", [])):
        matched_id = s["id"]
        break
        
print("1st match:", matched_id)

if not matched_id:
    for m in [history_str]:
        msg = m.lower()
        for s in SERVICES_DB:
            if s["id"].replace("_", " ") in msg or any(v in msg for v in s.get("variants", [])):
                matched_id = s["id"]
                break
        if matched_id: break

print("2nd match:", matched_id)

if not matched_id:
    # Hardcode fallback keywords for robust matching
    if "driving" in history_str.lower() or "dl" in history_str.lower(): matched_id = "driving_licence"
    elif "birth" in history_str.lower(): matched_id = "birth_certificate"
    elif "caste" in history_str.lower(): matched_id = "caste_certificate"
    elif "income" in history_str.lower(): matched_id = "income_certificate"
    elif "residence" in history_str.lower() or "nativity" in history_str.lower(): matched_id = "residence_certificate"
    elif "passport" in history_str.lower(): matched_id = "passport"
    elif "aadhaar" in history_str.lower(): matched_id = "aadhaar_update"
    elif "pan" in history_str.lower(): matched_id = "pan_card"
    elif "voter" in history_str.lower(): matched_id = "voter_id"
    elif "ration" in history_str.lower(): matched_id = "ration_card"
    
print("3rd match:", matched_id)
