# Run: pip install fastapi uvicorn anthropic

from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from groq import Groq
from language_detector import detect_language
from sip import calculate_sip
from tax_advisor import calculate_tax_savings
from investment_advisor import get_investment_advice
from study_engine import get_study_prompt

# Anthropic API client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Step 3 — Create the FastAPI app
app = FastAPI()

static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Step 4 — Add CORS middleware (required for frontend later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Step 5 — Request model
class SIPRequest(BaseModel):
    monthly_amount: float
    years: int
    annual_return: float = 12.0
    query: str = ""

class TaxRequest(BaseModel):
    annual_salary: float
    query: str = ""

class InvestRequest(BaseModel):
    amount: float
    query: str = ""

class StudyRequest(BaseModel):
    exam: str
    subject: str
    question: str
    query: str = ""

def generate_explanation(monthly_amount, years, annual_return, final_amount, total_invested, wealth_created, language):
    if language == "hinglish":
        tone = "Write in natural Hinglish (mix of Hindi and English). Example style: Aapne har mahine sirf X lagate hue Y total banaya."
    else:
        tone = "Write in simple friendly English."

    prompt = f"""
    You are a simple finance helper. Explain this SIP result in exactly 2-3 short sentences.

    Data:
    - Monthly investment: Rs {monthly_amount}
    - Number of years: {years}
    - Expected annual return: {annual_return}%
    - Final amount: Rs {final_amount}
    - Total invested: Rs {total_invested}
    - Extra earned: Rs {wealth_created}

    Structure your explanation like this:
    Sentence 1: What they will have at the end
    Sentence 2: How much extra they earned on top of what they invested
    Sentence 3: One simple action step

    Rules:
    - Never use these words: CAGR, portfolio, corpus, rebalancing, volatility, asset allocation
    - Keep it under 60 words
    - Be encouraging and friendly
    - Use Rs symbol for money
    - {tone}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    return response.choices[0].message.content


def generate_tax_explanation(annual_salary, tax_without_saving, tax_with_saving, tax_saved, language):
    if language == "hinglish":
        tone = "Write in natural Hinglish. Example: Aapki salary pe pehle itna tax tha, ab kam dena hoga."
    else:
        tone = "Write in simple friendly English."

    prompt = f"""
    You are a simple tax helper for Indian salaried employees.
    Explain this tax saving result in exactly 2-3 short sentences.

    Data:
    - Annual salary: Rs {annual_salary}
    - Tax without saving: Rs {tax_without_saving}
    - Tax after 80C saving: Rs {tax_with_saving}
    - Total tax saved: Rs {tax_saved}
    - Section 80C limit: Rs 1,50,000

    Structure:
    Sentence 1: How much tax they pay without any saving
    Sentence 2: How much tax they save using 80C
    Sentence 3: Best option — PPF or ELSS

    Rules:
    - No jargon
    - Under 60 words
    - Use Rs symbol
    - {tone}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    return response.choices[0].message.content


@app.get("/")
def serve_frontend():
    frontend_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {"status": "running"}


# POST endpoint
@app.post("/sip")
def sip_projection(request: SIPRequest):
    if request.monthly_amount <= 0 or request.years <= 0:
        return {"error": "monthly_amount and years must be greater than 0"}

    result = calculate_sip(request.monthly_amount, request.years, request.annual_return)

    language = detect_language(request.query)

    try:
        explanation = generate_explanation(
            monthly_amount=request.monthly_amount,
            years=request.years,
            annual_return=request.annual_return,
            final_amount=result["final_amount"],
            total_invested=result["total_invested"],
            wealth_created=result["wealth_created"],
            language=language
        )
    except:
        explanation = f"If you invest Rs {request.monthly_amount} every month for {request.years} years at {request.annual_return}% return, you will have Rs {result['final_amount']}. You invested Rs {result['total_invested']} and earned Rs {result['wealth_created']} extra."

    return {
        "explanation": explanation,
        "final_amount": result["final_amount"],
        "yearly_growth": result["yearly_growth"]
    }

# Step 7 — Health check route
@app.get("/")
def health_check():
    return {"status": "running"}


@app.post("/tax")
def tax_saving(request: TaxRequest):
    if request.annual_salary <= 0:
        return {"error": "annual_salary must be greater than 0"}

    result = calculate_tax_savings(request.annual_salary)

    language = detect_language(request.query)

    try:
        explanation = generate_tax_explanation(
            annual_salary=result["annual_salary"],
            tax_without_saving=result["tax_without_saving"],
            tax_with_saving=result["tax_with_saving"],
            tax_saved=result["tax_saved"],
            language=language
        )
    except:
        explanation = f"On salary of Rs {result['annual_salary']}, you pay Rs {result['tax_without_saving']} in tax. By investing Rs 1,50,000 in PPF or ELSS under 80C, you can save Rs {result['tax_saved']} and pay only Rs {result['tax_with_saving']}."

    return {
        "explanation": explanation,
        "annual_salary": result["annual_salary"],
        "tax_without_saving": result["tax_without_saving"],
        "tax_with_saving": result["tax_with_saving"],
        "tax_saved": result["tax_saved"],
        "section_80c_limit": result["section_80c_limit"],
        "options": result["options"]
    }


@app.post("/invest")
def invest_advice(request: InvestRequest):
    language = detect_language(request.query)
    result = get_investment_advice(
        amount=request.amount,
        language=language
    )
    return result

@app.post("/study")
def study_help(request: StudyRequest):
    if not request.question or not request.exam or not request.subject:
        return {"error": "Please provide exam, subject and question"}

    language = detect_language(request.query or request.question)

    prompt = get_study_prompt(
        exam=request.exam,
        subject=request.subject,
        question=request.question,
        language=language
    )

    try:
        message = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        raw = message.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.replace("```json", "").replace("```", "").strip()
        import json
        result = json.loads(raw)
    except Exception as e:
        result = {
            "explanation": "System is processing your question. Please try again.",
            "example": "",
            "exam_tip": "Keep practicing regularly.",
            "difficulty": "Medium",
            "related_topics": [],
            "quick_summary": "Please try again."
        }

    return {
        "exam": request.exam,
        "subject": request.subject,
        "question": request.question,
        "language": language,
        "explanation": result.get("explanation", ""),
        "example": result.get("example", ""),
        "exam_tip": result.get("exam_tip", ""),
        "difficulty": result.get("difficulty", "Medium"),
        "related_topics": result.get("related_topics", []),
        "quick_summary": result.get("quick_summary", "")
    }
