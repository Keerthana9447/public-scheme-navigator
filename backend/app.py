from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import re

from .rag_pipeline import RAGPipeline

# --- Initialize FastAPI ---
app = FastAPI(title="Public Scheme Navigator")

# --- Initialize RAG pipeline ---
rag = RAGPipeline()

# --- Serve frontend files at /frontend ---
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")

# --- Allow frontend requests (CORS) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Root endpoint ---
@app.get("/")
def root():
    return {"message": "Backend is running!"}

# --- Eligibility Checker ---
@app.get("/eligibility")
def check_eligibility(
    age: int = Query(...),
    income: int = Query(...),
    gender: str = Query(None),
    occupation: str = Query(None),
    disability: bool = Query(False)
):
    schemes = rag.load_schemes()
    eligible = []
    for scheme in schemes:
        if age >= scheme.get("min_age", 0) and age <= scheme.get("max_age", 200):
            if income <= scheme.get("income_limit", 999999):
                eligible.append(scheme["name"])

    if eligible:
        return {
            "message": "✅ You are eligible for the following services:",
            "eligible_schemes": eligible
        }
    return {
        "message": "❌ You are not eligible for any services.",
        "eligible_schemes": []
    }

# --- Document Guidance ---
@app.get("/guidance")
def get_guidance(scheme: str = Query(...)):
    guidance_map = {
        "Scholarship for Students": [
            "Birth certificate",
            "School ID card",
            "Income certificate",
            "Previous year marksheet"
        ],
        "Senior Citizen Pension": [
            "Age proof (Aadhaar/PAN)",
            "Income certificate",
            "Bank account details",
            "Residential proof"
        ],
        "Healthcare Subsidy": [
            "Income certificate",
            "Medical records",
            "Aadhaar card",
            "Bank account details"
        ],
        "Disability Support Scheme": [
            "Disability certificate",
            "Income certificate",
            "Aadhaar card",
            "Bank account details"
        ]
    }
    return {"scheme": scheme, "documents": guidance_map.get(scheme, ["No guidance available"])}

# --- Chatbot ---
@app.get("/chat")
def chat(query: str):
    response = rag.generate_answer(query)

    # Try to extract age and income from query text
    age_match = re.search(r"\b(\d{1,2})\b", query.lower())
    income_match = re.search(r"\b(\d{4,6})\b", query)

    age = int(age_match.group(1)) if age_match else None
    income = int(income_match.group(1)) if income_match else None

    if age is not None and income is not None:
        schemes = rag.load_schemes()
        eligible = []
        for scheme in schemes:
            if age >= scheme.get("min_age", 0) and age <= scheme.get("max_age", 200):
                if income <= scheme.get("income_limit", 999999):
                    eligible.append(scheme["name"])

        if eligible:
            eligible_str = ", ".join(eligible)
            return {
                "response": f"🎉 Great news! Based on age {age} and income {income}, you qualify for: {eligible_str}"
            }
        else:
            return {
                "response": f"😔 Sorry, based on age {age} and income {income}, you don’t qualify for any schemes."
            }
    else:
        return {
            "response": f"💡 I found schemes related to '{query}'. Please mention your age and income clearly (e.g., 'I am 21 years old with income 20000')."
        }
