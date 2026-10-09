import os
import json
from typing import List, Optional, Literal, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

app = FastAPI()

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load services
with open("data/services.json", "r") as f:
    SERVICES_DB = json.load(f)

SERVICES_MAP = {s["id"]: s for s in SERVICES_DB}
AVAILABLE_SERVICE_NAMES = [s["name"] for s in SERVICES_DB]


import sqlite3
import hashlib

class AuthRequest(BaseModel):
    email: str
    password: str

def init_db():
    conn = sqlite3.connect("data/users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

init_db()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@app.post("/api/signup")
def signup(req: AuthRequest):
    conn = sqlite3.connect("data/users.db")
    c = conn.cursor()
    c.execute("SELECT email FROM users WHERE email=?", (req.email,))
    if c.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Email already registered")
    c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (req.email, hash_password(req.password)))
    conn.commit()
    conn.close()
    return {"message": "User created successfully", "token": "token_" + req.email, "email": req.email}

@app.post("/api/login")
def login(req: AuthRequest):
    conn = sqlite3.connect("data/users.db")
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE email=?", (req.email,))
    row = c.fetchone()
    conn.close()
    if not row or row[0] != hash_password(req.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Send Security Alert
    import threading
    alert_subject = "🚨 Security Alert: New Login to Naviq"
    alert_body = f"Hello,\n\nA new login was just detected on your Naviq account ({req.email}).\nIf this was you, no action is needed.\nIf this was not you, please secure your account immediately.\n\n- Naviq Security Team"
    threading.Thread(target=send_email_helper, args=(req.email, alert_subject, alert_body)).start()

    return {"message": "Login successful", "token": "token_" + req.email, "email": req.email}


import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email_helper(to_email: str, subject: str, body: str):
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")
    if smtp_email and smtp_password:
        try:
            msg = MIMEMultipart()
            msg['From'] = smtp_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.send_message(msg)
            server.quit()
            print(f"✅ REAL EMAIL SENT TO: {to_email}")
        except Exception as e:
            print(f"❌ FAILED TO SEND REAL EMAIL: {e}")
    else:
        print("\n" + "="*50)
        print(f"📧 MOCK EMAIL SENT TO: {to_email}")
        print(f"SUBJECT: {subject}")
        print("-" * 50)
        print(f"{body}")
        print("="*50 + "\n")

class EmailRequest(BaseModel):
    email: str
    subject: str
    body: str

@app.post("/api/email")
def send_email_api(req: EmailRequest):
    send_email_helper(req.email, req.subject, req.body)
    return {"message": "Email request processed"}

import os
from twilio.rest import Client

class SMSRequest(BaseModel):
    phone: str
    message: str

@app.post("/api/sms")
def send_sms(req: SMSRequest):
    twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
    twilio_auth = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_phone = os.getenv("TWILIO_PHONE_NUMBER")
    
    if twilio_sid and twilio_auth and twilio_phone:
        try:
            client = Client(twilio_sid, twilio_auth)
            message = client.messages.create(
                body=f"SECURITY ALERT: {req.message}",
                from_=twilio_phone,
                to=req.phone
            )
            print(f"✅ REAL SMS SENT VIA TWILIO TO: {req.phone} (SID: {message.sid})")
            return {"message": "Real SMS sent successfully"}
        except Exception as e:
            error_msg = str(e)
            print(f"❌ FAILED TO SEND REAL SMS: {error_msg}")
            if "trial accounts" in error_msg.lower():
                raise HTTPException(status_code=400, detail="Twilio Trial Account Error: You must use your Twilio Virtual Phone Number as the sender (not your personal number), and you can only send to verified phone numbers.")
            else:
                raise HTTPException(status_code=400, detail=f"Twilio Error: {error_msg}")
    else:
        # Fallback to Mock
        print("\n" + "="*50)
        print(f"📱 MOCK SECURITY SMS ALERT SENT TO: {req.phone}")
        print("-" * 50)
        print(f"{req.message}")
        print("="*50 + "\n")
        return {"message": "Mock SMS dispatched successfully"}

class Message(BaseModel):
    role: str
    content: str

class Query(BaseModel):
    messages: List[Message]
    state: Optional[str] = "Andhra Pradesh"

# -----------------
# Response Models
# -----------------
class SourceModel(BaseModel):
    title: str
    url: str

class StepModel(BaseModel):
    id: str
    text: str
    depends_on: List[str] = []
    source: SourceModel
    status: str = "pending"

class DocumentModel(BaseModel):
    name: str
    have: bool = False
    how_to_get: str
    source: SourceModel
    blocked_by_service: Optional[str] = None

class PrerequisiteModel(BaseModel):
    name: str
    reason: str
    link_to_service_id: str

class TodoModel(BaseModel):
    id: str
    text: str
    done: bool = False

class ReminderModel(BaseModel):
    time: str
    text: str

class ServiceInfo(BaseModel):
    id: str
    name: str
    official_url: str

class PlanResponse(BaseModel):
    type: Literal["plan"] = "plan"
    service: ServiceInfo
    steps: List[StepModel]
    documents: List[DocumentModel]
    prerequisite_services: List[PrerequisiteModel]
    todo: List[TodoModel]
    reminders: List[ReminderModel]
    last_verified: str
    disclaimer: str = "Rules can change. Confirm on the official portal."

class QuestionResponse(BaseModel):
    type: Literal["question"] = "question"
    text: str

class FinalOutput(BaseModel):
    response_type: Literal["question", "plan"]
    question_text: Optional[str] = None
    plan: Optional[PlanResponse] = None


def topological_sort(steps: List[Dict]) -> List[Dict]:
    """Sort steps based on depends_on. Simple Kahn's algorithm."""
    in_degree = {s['id']: 0 for s in steps}
    graph = {s['id']: [] for s in steps}
    
    for s in steps:
        for dep in s.get('depends_on', []):
            if dep in graph:
                graph[dep].append(s['id'])
                in_degree[s['id']] += 1
                
    queue = [s_id for s_id in in_degree if in_degree[s_id] == 0]
    sorted_ids = []
    
    while queue:
        curr = queue.pop(0)
        sorted_ids.append(curr)
        for neighbor in graph[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    if len(sorted_ids) != len(steps):
        raise ValueError("Cycle detected or missing dependencies in steps")
        
    step_map = {s['id']: s for s in steps}
    return [step_map[s_id] for s_id in sorted_ids]


def build_demo_plan(service_id: str, state_name: str) -> dict:
    svc = SERVICES_MAP[service_id]
    steps = topological_sort(svc["steps"])
    
    # Extract regional portal if available
    portal_name = svc["official_portal"]["name"]
    portal_url = svc["official_portal"]["url"]
    if state_name in svc.get("state_specific", {}):
        state_data = svc["state_specific"][state_name]
        if isinstance(state_data, dict) and "portal_name" in state_data:
            portal_name = state_data["portal_name"]
            portal_url = state_data["portal_url"]
            
    for s in steps:
        s["status"] = "pending"
        # Make the mock sources point to the right state portal if they point to generic portals
        if s["source"]["url"].startswith("https://india.gov.in"):
            s["source"]["url"] = portal_url
            s["source"]["title"] = f"{portal_name} Portal"
            
    docs = []
    for d in svc.get("documents", []):
        d_source_url = d.get("source", {}).get("url", portal_url)
        d_source_title = d.get("source", {}).get("title", "Official Portal")
        if d_source_url.startswith("https://india.gov.in"):
            d_source_url = portal_url
            d_source_title = f"{portal_name} Portal"
            
        docs.append({
            "name": d["name"],
            "have": False,
            "how_to_get": d.get("how_to_get", ""),
            "source": {"title": d_source_title, "url": d_source_url},
            "blocked_by_service": d.get("obtained_from_service")
        })
    prereqs = []
    for d in docs:
        if d["blocked_by_service"]:
            psvc = SERVICES_MAP.get(d["blocked_by_service"])
            if psvc:
                prereqs.append({
                    "name": psvc["name"],
                    "reason": f"Required for {d['name']}",
                    "link_to_service_id": psvc["id"]
                })
    return {
        "type": "plan",
        "service": {
            "id": svc["id"],
            "name": f"{svc['name']} ({state_name})" if state_name in svc.get("state_specific", {}) else svc["name"],
            "official_url": portal_url
        },
        "steps": steps,
        "documents": docs,
        "prerequisite_services": prereqs,
        "todo": [{"id": f"t_{i}", "text": f"Gather {d['name']}", "done": False} for i, d in enumerate(docs)],
        "reminders": [{"time": "Immediately", "text": "Review documents needed"}],
        "last_verified": svc["last_verified"],
        "disclaimer": "Rules can change. Confirm on the official portal."
    }


@app.post("/api/plan")
async def generate_plan(query: Query):
    import logging
    logging.info(f"Received request: {query.messages[-1].content}")

    api_key = os.getenv("GOOGLE_API_KEY")
    demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"
    
    if not api_key and not demo_mode:
        raise HTTPException(status_code=503, detail="AI Service is currently unavailable and demo mode is off.")

    # INTERCEPT FOR DEMO FORM
    user_messages = [m.content for m in query.messages if m.role == 'user']
    latest_query = user_messages[-1].lower() if user_messages else ""
    
    if len(user_messages) == 1:
        fields = []
        if "passport" in latest_query:
            fields = [
                {"name": "State", "options": ["Andhra Pradesh", "Telangana", "Other Location"]},
                {"name": "Application type", "options": ["New Application", "Existing Application"]}
            ]
        elif "pan" in latest_query:
            fields = [
                {"name": "Applicant Category", "options": ["Individual", "Foreign Citizen", "Company/Trust"]},
                {"name": "Application Type", "options": ["New PAN", "Correction/Update in PAN"]}
            ]
        
        if fields:
            return {
                "type": "form",
                "text": "Great! To give you the right guidance, I need a few details.",
                "fields": fields
            }

    history_str = "\n".join([f"{m.role}: {m.content}" for m in query.messages])
    user_latest = query.messages[-1].content.lower()

# Step A: Intent Matching
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
        matched_id = "passport"""

    if not matched_id:
        for m in query.messages:
            msg = m.content.lower()
            for s in SERVICES_DB:
                if s["id"].replace("_", " ") in msg or any(v in msg for v in s.get("variants", [])):
                    matched_id = s["id"]
                    break
            if matched_id: break

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

    if not matched_id:
        logging.info("Unsupported service requested")
        return {
            "type": "unsupported",
            "text": "I don't have verified information for this service yet.",
            "available_services": AVAILABLE_SERVICE_NAMES
        }

    # Step B & C: RAG via Gemini
    if demo_mode and not api_key:
        # pure rule based fallback if no key
        if len(query.messages) == 1:
            return {"type": "question", "text": "Are there any specific details or missing documents I should know about?"}
        plan_data = build_demo_plan(matched_id, query.state)
        plan_data["demo_mode"] = True
        return plan_data

    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    llm = ChatGoogleGenerativeAI(model=model_name, api_key=api_key)
    structured_llm = llm.with_structured_output(FinalOutput)

    context_json = json.dumps(SERVICES_MAP[matched_id])
    
    prompt = f"""
You are an expert government filing agent. 
Use ONLY the verified context below. Do not add any step, portal, fee, or form that is not in the context.
If information is missing, say so. Do NOT invent anything.

VERIFIED CONTEXT:
{context_json}

USER STATE: {query.state}

CONVERSATION HISTORY:
{history_str}

Decide:
1. If you need to ask a clarifying question (e.g. variants, which docs they have), return response_type="question" and question_text.
2. If you have enough info, return response_type="plan" and the filled plan. 
   - Extract prerequisite services for any documents they are missing.
   - Use exact step IDs from context. 
"""

    try:
        response = await structured_llm.ainvoke(prompt)
        
        if response.response_type == "question":
            return {"type": "question", "text": response.question_text}
            
        # Step D: VALIDATE
        plan = response.plan
        if not plan:
            raise ValueError("Plan object missing")
            
        # Validate steps exist in knowledge base
        valid_step_ids = [s["id"] for s in SERVICES_MAP[matched_id]["steps"]]
        for step in plan.steps:
            if step.id not in valid_step_ids:
                # LLM hallucinated a step, let's just log and fallback to rule-based or raise
                logging.error(f"Validation failed: hallucinated step {step.id}")
                plan_data = build_demo_plan(matched_id, query.state)
                return plan_data

        plan_dict = plan.dict()
        try:
            plan_dict["steps"] = topological_sort(plan_dict["steps"])
        except Exception as e:
            logging.error(f"Cycle detected: {e}")
            plan_data = build_demo_plan(matched_id, query.state)
            return plan_data

        return {"type": "plan", "plan": plan_dict}
        
    except Exception as e:
        logging.error(f"Error calling LLM: {e}")
        # fallback to demo
        plan_data = build_demo_plan(matched_id, query.state)
        plan_data["demo_mode"] = True
        return plan_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
