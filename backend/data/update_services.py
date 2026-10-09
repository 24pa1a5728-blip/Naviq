import json

def update_services():
    with open('data/services.json', 'r') as f:
        services = json.load(f)

    state_portals = {
        "Andhra Pradesh": {"portal_name": "AP MeeSeva", "portal_url": "https://ap.meeseva.gov.in/DeptWebPortal/UserInterface/LoginForm.aspx"},
        "Telangana": {"portal_name": "TS MeeSeva", "portal_url": "https://ts.meeseva.telangana.gov.in/meeseva/home.htm"},
        "Maharashtra": {"portal_name": "Aaple Sarkar", "portal_url": "https://aaplesarkar.mahaonline.gov.in"},
        "Delhi": {"portal_name": "e-District Delhi", "portal_url": "https://edistrict.delhigovt.nic.in"}
    }
    
    ration_portals = {
        "Andhra Pradesh": {"portal_name": "AP Civil Supplies", "portal_url": "https://epdsap.ap.gov.in"},
        "Telangana": {"portal_name": "TS Civil Supplies", "portal_url": "https://epds.telangana.gov.in"},
        "Maharashtra": {"portal_name": "MahaFood", "portal_url": "https://mahafood.gov.in"},
        "Delhi": {"portal_name": "Delhi Food & Supply", "portal_url": "https://nfs.delhi.gov.in"}
    }

    for s in services:
        if s['id'] in ['income_certificate', 'caste_certificate', 'residence_certificate', 'birth_certificate']:
            # Overwrite state specific with accurate portals
            s['state_specific'] = state_portals
        elif s['id'] == 'ration_card':
            s['state_specific'] = ration_portals
            
    with open('data/services.json', 'w') as f:
        json.dump(services, f, indent=2)
        
update_services()
print("Updated services.json with accurate regional portals")
