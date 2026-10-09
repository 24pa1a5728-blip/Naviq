import json

with open('data/services.json', 'r') as f:
    services = json.load(f)

for s in services:
    if s['id'] == 'passport':
        s['official_portal']['url'] = "https://www.passportindia.gov.in"
        for step in s['steps']:
            step['source']['url'] = "https://www.passportindia.gov.in"
        for doc in s['documents']:
            if doc.get('source'):
                doc['source']['url'] = "https://www.passportindia.gov.in"
    
    if s['id'] == 'birth_certificate':
        # Revert state_specific for birth certificate back to CRS or specific municipal ones
        s['state_specific'] = {
            "Andhra Pradesh": {"portal_name": "AP MeeSeva", "portal_url": "https://ap.meeseva.gov.in"},
            "Telangana": {"portal_name": "TS MeeSeva", "portal_url": "https://ts.meeseva.telangana.gov.in"},
            "Maharashtra": {"portal_name": "Civil Registration System", "portal_url": "https://crsorgi.gov.in"},
            "Delhi": {"portal_name": "MCD Online / CRS", "portal_url": "https://mcdonline.nic.in"}
        }

with open('data/services.json', 'w') as f:
    json.dump(services, f, indent=2)

print("Updated services.json")
