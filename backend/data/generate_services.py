import json
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")

services = [
    {
        "id": "passport",
        "name": "Passport (Fresh / Re-issue)",
        "category": "identity",
        "variants": ["fresh", "reissue"],
        "official_portal": {"name": "Passport Seva", "url": "https://portal2.passportindia.gov.in"},
        "steps": [
            {"id": "p1", "text": "Register on Passport Seva Portal", "depends_on": [], "source": {"title": "Passport Seva Registration", "url": "https://portal2.passportindia.gov.in"}},
            {"id": "p2", "text": "Fill the online application form and submit", "depends_on": ["p1"], "source": {"title": "Passport Application", "url": "https://portal2.passportindia.gov.in"}},
            {"id": "p3", "text": "Pay fees and schedule appointment", "depends_on": ["p2"], "source": {"title": "Fee Payment", "url": "https://portal2.passportindia.gov.in"}},
            {"id": "p4", "text": "Visit PSK (Passport Seva Kendra) for document verification and biometrics", "depends_on": ["p3"], "source": {"title": "Visit PSK", "url": "https://portal2.passportindia.gov.in"}},
            {"id": "p5", "text": "Police Verification", "depends_on": ["p4"], "source": {"title": "Police Verification", "url": "https://portal2.passportindia.gov.in"}}
        ],
        "documents": [
            {"id": "d_aadhaar", "name": "Aadhaar Card (Address Proof)", "needed_for_steps": ["p4"], "how_to_get": "Download from UIDAI or visit Aadhaar center", "obtained_from_service": "aadhaar_update", "source": {"title": "Document Advisor", "url": "https://portal2.passportindia.gov.in/AppOnlineProject/popuponline/AttachmentAdvisorSub"}},
            {"id": "d_birth", "name": "Birth Certificate (Age Proof)", "needed_for_steps": ["p4"], "how_to_get": "Apply at local municipal corporation", "obtained_from_service": "birth_certificate", "source": {"title": "Document Advisor", "url": "https://portal2.passportindia.gov.in/AppOnlineProject/popuponline/AttachmentAdvisorSub"}},
            {"id": "d_10th", "name": "10th Standard Marksheet (Non-ECR)", "needed_for_steps": ["p4"], "how_to_get": "From educational board", "obtained_from_service": None, "source": {"title": "Document Advisor", "url": "https://portal2.passportindia.gov.in/AppOnlineProject/popuponline/AttachmentAdvisorSub"}}
        ],
        "fees_note": "Rs. 1500 for normal fresh passport (36 pages). Check the official portal for tatkaal or re-issue fees.",
        "state_specific": {},
        "last_verified": today
    },
    {
        "id": "driving_licence",
        "name": "Driving Licence (Learner / Permanent)",
        "category": "transport",
        "variants": ["learner", "permanent"],
        "official_portal": {"name": "Sarathi Parivahan", "url": "https://sarathi.parivahan.gov.in"},
        "steps": [
            {"id": "dl1", "text": "Apply for Learner's Licence online", "depends_on": [], "source": {"title": "Apply LL", "url": "https://sarathi.parivahan.gov.in"}},
            {"id": "dl2", "text": "Pass the online Learner's Licence test", "depends_on": ["dl1"], "source": {"title": "LL Test", "url": "https://sarathi.parivahan.gov.in"}},
            {"id": "dl3", "text": "Wait for 30 days", "depends_on": ["dl2"], "source": {"title": "DL Guidelines", "url": "https://sarathi.parivahan.gov.in"}},
            {"id": "dl4", "text": "Apply for Permanent Driving Licence and book driving test slot", "depends_on": ["dl3"], "source": {"title": "Apply DL", "url": "https://sarathi.parivahan.gov.in"}},
            {"id": "dl5", "text": "Pass the driving skill test at the RTO", "depends_on": ["dl4"], "source": {"title": "DL Test", "url": "https://sarathi.parivahan.gov.in"}}
        ],
        "documents": [
            {"id": "dl_aadhaar", "name": "Aadhaar Card (Address & Age Proof)", "needed_for_steps": ["dl1"], "how_to_get": "Use eKYC on Parivahan", "obtained_from_service": "aadhaar_update", "source": {"title": "Parivahan Docs", "url": "https://sarathi.parivahan.gov.in"}},
            {"id": "dl_med", "name": "Medical Certificate (Form 1A)", "needed_for_steps": ["dl1"], "how_to_get": "From a registered medical practitioner", "obtained_from_service": None, "source": {"title": "Parivahan Docs", "url": "https://sarathi.parivahan.gov.in"}}
        ],
        "fees_note": "Check the official portal for state-specific LL and DL fees.",
        "state_specific": {"AP": "RTO tests may require visiting specific tracks."},
        "last_verified": today
    },
    {
        "id": "birth_certificate",
        "name": "Birth Certificate",
        "category": "civil",
        "variants": ["new", "delayed", "correction"],
        "official_portal": {"name": "Civil Registration System (CRS)", "url": "https://crsorgi.gov.in"},
        "steps": [
            {"id": "bc1", "text": "Obtain discharge summary from the hospital", "depends_on": [], "source": {"title": "CRS Portal", "url": "https://crsorgi.gov.in"}},
            {"id": "bc2", "text": "Register birth on CRS portal or state portal within 21 days", "depends_on": ["bc1"], "source": {"title": "CRS Registration", "url": "https://crsorgi.gov.in"}},
            {"id": "bc3", "text": "If delayed, obtain affidavit and SDM order", "depends_on": [], "source": {"title": "CRS Guidelines", "url": "https://crsorgi.gov.in"}},
            {"id": "bc4", "text": "Download digitally signed certificate after approval", "depends_on": ["bc2"], "source": {"title": "CRS Download", "url": "https://crsorgi.gov.in"}}
        ],
        "documents": [
            {"id": "bc_hosp", "name": "Hospital Discharge Summary", "needed_for_steps": ["bc2"], "how_to_get": "From the hospital of birth", "obtained_from_service": None, "source": {"title": "CRS Manual", "url": "https://crsorgi.gov.in"}},
            {"id": "bc_id", "name": "Parents' ID Proof", "needed_for_steps": ["bc2"], "how_to_get": "Aadhaar or Voter ID", "obtained_from_service": "aadhaar_update", "source": {"title": "CRS Manual", "url": "https://crsorgi.gov.in"}}
        ],
        "fees_note": "Free if registered within 21 days. Check official portal for late fees.",
        "state_specific": {"AP": "Can be applied through AP MeeSeva portal."},
        "last_verified": today
    },
    {
        "id": "income_certificate",
        "name": "Income Certificate",
        "category": "revenue",
        "variants": ["new"],
        "official_portal": {"name": "State e-District Portal", "url": "https://india.gov.in/topics/certificates/income-certificate"},
        "steps": [
            {"id": "ic1", "text": "Register on the state's e-District portal", "depends_on": [], "source": {"title": "India.gov.in", "url": "https://india.gov.in"}},
            {"id": "ic2", "text": "Fill the Income Certificate form and upload documents", "depends_on": ["ic1"], "source": {"title": "State Guidelines", "url": "https://india.gov.in"}},
            {"id": "ic3", "text": "Field verification by Village Revenue Officer", "depends_on": ["ic2"], "source": {"title": "Verification Process", "url": "https://india.gov.in"}},
            {"id": "ic4", "text": "Download certificate once Tahsildar approves", "depends_on": ["ic3"], "source": {"title": "Download", "url": "https://india.gov.in"}}
        ],
        "documents": [
            {"id": "ic_id", "name": "Aadhaar Card", "needed_for_steps": ["ic2"], "how_to_get": "UIDAI", "obtained_from_service": "aadhaar_update", "source": {"title": "Docs", "url": "https://india.gov.in"}},
            {"id": "ic_proof", "name": "Salary Slip / ITR / Affidavit", "needed_for_steps": ["ic2"], "how_to_get": "From employer or IT Dept", "obtained_from_service": None, "source": {"title": "Docs", "url": "https://india.gov.in"}}
        ],
        "fees_note": "Usually Rs. 15-50 processing fee at CSCs. Check state portal.",
        "state_specific": {"AP": "Apply via MeeSeva.", "TS": "Apply via TS MeeSeva."},
        "last_verified": today
    },
    {
        "id": "caste_certificate",
        "name": "Caste Certificate",
        "category": "revenue",
        "variants": ["new"],
        "official_portal": {"name": "State e-District Portal", "url": "https://india.gov.in/topics/certificates/caste-certificate"},
        "steps": [
            {"id": "cc1", "text": "Submit application via e-District or local CSC", "depends_on": [], "source": {"title": "Application", "url": "https://india.gov.in"}},
            {"id": "cc2", "text": "Verification by Revenue Inspector", "depends_on": ["cc1"], "source": {"title": "Verification", "url": "https://india.gov.in"}},
            {"id": "cc3", "text": "Approval by Tahsildar and digital issuance", "depends_on": ["cc2"], "source": {"title": "Issuance", "url": "https://india.gov.in"}}
        ],
        "documents": [
            {"id": "cc_proof", "name": "Father's/Relative's Caste Certificate", "needed_for_steps": ["cc1"], "how_to_get": "From family records", "obtained_from_service": None, "source": {"title": "Docs", "url": "https://india.gov.in"}},
            {"id": "cc_res", "name": "Proof of Address", "needed_for_steps": ["cc1"], "how_to_get": "Ration card or Aadhaar", "obtained_from_service": "residence_certificate", "source": {"title": "Docs", "url": "https://india.gov.in"}}
        ],
        "fees_note": "Check state portal for CSC fees.",
        "state_specific": {"AP": "Processed through AP MeeSeva."},
        "last_verified": today
    },
    {
        "id": "residence_certificate",
        "name": "Residence / Nativity Certificate",
        "category": "revenue",
        "variants": ["new"],
        "official_portal": {"name": "State e-District Portal", "url": "https://india.gov.in"},
        "steps": [
            {"id": "rc1", "text": "Apply online on e-District portal", "depends_on": [], "source": {"title": "Apply", "url": "https://india.gov.in"}},
            {"id": "rc2", "text": "VAO / Revenue Inspector verifies address history", "depends_on": ["rc1"], "source": {"title": "Verification", "url": "https://india.gov.in"}},
            {"id": "rc3", "text": "Certificate issued by Tahsildar", "depends_on": ["rc2"], "source": {"title": "Issuance", "url": "https://india.gov.in"}}
        ],
        "documents": [
            {"id": "rc_bills", "name": "Utility Bills (Electricity/Water) for last 5-7 years", "needed_for_steps": ["rc1"], "how_to_get": "From utility providers", "obtained_from_service": None, "source": {"title": "Docs", "url": "https://india.gov.in"}},
            {"id": "rc_id", "name": "Aadhaar / Voter ID", "needed_for_steps": ["rc1"], "how_to_get": "UIDAI / ECI", "obtained_from_service": "aadhaar_update", "source": {"title": "Docs", "url": "https://india.gov.in"}}
        ],
        "fees_note": "Nominal CSC fees apply. Check portal.",
        "state_specific": {"AP": "Available via MeeSeva."},
        "last_verified": today
    },
    {
        "id": "aadhaar_update",
        "name": "Aadhaar Update",
        "category": "identity",
        "variants": ["address", "name", "mobile", "biometric"],
        "official_portal": {"name": "UIDAI", "url": "https://myaadhaar.uidai.gov.in"},
        "steps": [
            {"id": "au1", "text": "Login to myAadhaar portal (for address/demographics) or book appointment for biometrics/mobile", "depends_on": [], "source": {"title": "myAadhaar", "url": "https://myaadhaar.uidai.gov.in"}},
            {"id": "au2", "text": "Upload valid proof of identity/address (if online)", "depends_on": ["au1"], "source": {"title": "Upload Docs", "url": "https://myaadhaar.uidai.gov.in"}},
            {"id": "au3", "text": "Pay update fee", "depends_on": ["au2"], "source": {"title": "Payment", "url": "https://myaadhaar.uidai.gov.in"}},
            {"id": "au4", "text": "Wait for SRN processing (usually 5-15 days)", "depends_on": ["au3"], "source": {"title": "Processing", "url": "https://myaadhaar.uidai.gov.in"}}
        ],
        "documents": [
            {"id": "au_poa", "name": "Proof of Address (for address update)", "needed_for_steps": ["au2"], "how_to_get": "Voter ID, Passport, or Ration Card", "obtained_from_service": "passport", "source": {"title": "Valid Documents List", "url": "https://uidai.gov.in/images/commdoc/valid_documents_list.pdf"}}
        ],
        "fees_note": "Rs. 50 for online demographic update. Rs. 100 for biometrics. Check UIDAI for latest fees.",
        "state_specific": {},
        "last_verified": today
    },
    {
        "id": "pan_card",
        "name": "PAN Card",
        "category": "identity",
        "variants": ["new", "correction"],
        "official_portal": {"name": "NSDL / Income Tax", "url": "https://www.onlineservices.nsdl.com"},
        "steps": [
            {"id": "pan1", "text": "Fill Form 49A online", "depends_on": [], "source": {"title": "Form 49A", "url": "https://www.onlineservices.nsdl.com"}},
            {"id": "pan2", "text": "Authenticate using Aadhaar e-KYC (paperless) or submit physical docs", "depends_on": ["pan1"], "source": {"title": "Authentication", "url": "https://www.onlineservices.nsdl.com"}},
            {"id": "pan3", "text": "Pay application fee", "depends_on": ["pan2"], "source": {"title": "Payment", "url": "https://www.onlineservices.nsdl.com"}},
            {"id": "pan4", "text": "e-PAN generated and physical card dispatched", "depends_on": ["pan3"], "source": {"title": "Dispatch", "url": "https://www.onlineservices.nsdl.com"}}
        ],
        "documents": [
            {"id": "pan_aadhaar", "name": "Aadhaar Card", "needed_for_steps": ["pan2"], "how_to_get": "UIDAI", "obtained_from_service": "aadhaar_update", "source": {"title": "PAN Docs", "url": "https://www.onlineservices.nsdl.com"}}
        ],
        "fees_note": "Check official portal. Usually around Rs. 107 for Indian dispatch.",
        "state_specific": {},
        "last_verified": today
    },
    {
        "id": "voter_id",
        "name": "Voter ID",
        "category": "identity",
        "variants": ["new", "correction"],
        "official_portal": {"name": "Voters' Service Portal", "url": "https://voters.eci.gov.in"},
        "steps": [
            {"id": "vo1", "text": "Register/Login on Voters' Portal", "depends_on": [], "source": {"title": "Voter Portal", "url": "https://voters.eci.gov.in"}},
            {"id": "vo2", "text": "Fill Form 6 for new registration", "depends_on": ["vo1"], "source": {"title": "Form 6", "url": "https://voters.eci.gov.in"}},
            {"id": "vo3", "text": "Upload Photo, ID, and Address Proof", "depends_on": ["vo2"], "source": {"title": "Upload Docs", "url": "https://voters.eci.gov.in"}},
            {"id": "vo4", "text": "BLO verification", "depends_on": ["vo3"], "source": {"title": "Verification", "url": "https://voters.eci.gov.in"}},
            {"id": "vo5", "text": "EPIC (Voter ID) generated and mailed", "depends_on": ["vo4"], "source": {"title": "EPIC generation", "url": "https://voters.eci.gov.in"}}
        ],
        "documents": [
            {"id": "vo_age", "name": "Age Proof (Birth Certificate / Aadhaar / PAN)", "needed_for_steps": ["vo3"], "how_to_get": "Appropriate authority", "obtained_from_service": "birth_certificate", "source": {"title": "Form 6 Instructions", "url": "https://voters.eci.gov.in"}},
            {"id": "vo_address", "name": "Address Proof (Aadhaar / Utility Bill)", "needed_for_steps": ["vo3"], "how_to_get": "UIDAI or Utility provider", "obtained_from_service": "aadhaar_update", "source": {"title": "Form 6 Instructions", "url": "https://voters.eci.gov.in"}}
        ],
        "fees_note": "Free of cost.",
        "state_specific": {},
        "last_verified": today
    },
    {
        "id": "ration_card",
        "name": "Ration Card",
        "category": "food",
        "variants": ["new", "modification"],
        "official_portal": {"name": "National Food Security Portal / State Portals", "url": "https://nfsa.gov.in"},
        "steps": [
            {"id": "rat1", "text": "Visit state specific food civil supplies portal or MeeSeva", "depends_on": [], "source": {"title": "NFSA", "url": "https://nfsa.gov.in"}},
            {"id": "rat2", "text": "Fill application with family details and Aadhaar numbers", "depends_on": ["rat1"], "source": {"title": "Application", "url": "https://nfsa.gov.in"}},
            {"id": "rat3", "text": "Submit income proof", "depends_on": ["rat2"], "source": {"title": "Income Proof", "url": "https://nfsa.gov.in"}},
            {"id": "rat4", "text": "Field verification by civil supplies officer", "depends_on": ["rat3"], "source": {"title": "Verification", "url": "https://nfsa.gov.in"}}
        ],
        "documents": [
            {"id": "rat_aadhaar", "name": "Aadhaar Cards of all members", "needed_for_steps": ["rat2"], "how_to_get": "UIDAI", "obtained_from_service": "aadhaar_update", "source": {"title": "Docs", "url": "https://nfsa.gov.in"}},
            {"id": "rat_income", "name": "Income Certificate", "needed_for_steps": ["rat3"], "how_to_get": "Apply via state portal", "obtained_from_service": "income_certificate", "source": {"title": "Docs", "url": "https://nfsa.gov.in"}}
        ],
        "fees_note": "Check state portal for exact fees.",
        "state_specific": {"AP": "Apply via AP Civil Supplies or Village Secretariat."},
        "last_verified": today
    }
]

with open('backend/data/services.json', 'w') as f:
    json.dump(services, f, indent=2)

print("Generated services.json")
