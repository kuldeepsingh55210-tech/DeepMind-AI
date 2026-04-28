def get_study_prompt(exam: str, subject: str, question: str, language: str) -> str:
    exam_instructions = {
        "JEE": """You are an expert JEE coach.
Focus on:
- Deep concept clarity
- Step-by-step numerical solutions
- Shortcut tricks for JEE
- Common mistakes students make
- Difficulty level of this topic in JEE""",

        "NEET": """You are an expert NEET coach.
Focus on:
- NCERT-based explanations
- Biological diagrams description (text form)
- Memory tricks for NEET
- NCERT line importance
- Assertion-Reason style tips""",

        "Board 10": """You are an expert CBSE Class 10 teacher.
Focus on:
- Simple NCERT-based explanation
- Board exam marking scheme
- Important definitions
- Common board exam questions on this topic
- Easy memory techniques""",

        "Board 12": """You are an expert CBSE Class 12 teacher.
Focus on:
- Detailed NCERT explanation
- Derivations if needed
- Board exam tips
- Important formulas
- Previous year board question pattern"""
    }

    language_instructions = {
        "hindi": """IMPORTANT: Respond ONLY in Hindi (Devanagari script).
Use simple Hindi words.
Avoid complex Sanskrit terms.
Example style: "न्यूटन का दूसरा नियम कहता है कि..."
""",

        "hinglish": """IMPORTANT: Respond in Hinglish (Hindi + English mix).
Use natural conversational Hinglish.
Keep English for technical terms and formulas.
Example style: "Newton ka 2nd law basically kehta hai ki..."
Avoid jargon. Be friendly like a study buddy.
""",

        "english": """IMPORTANT: Respond in simple clear English.
Avoid complex vocabulary.
Be friendly and encouraging.
Example style: "Newton's 2nd law simply means..."
"""
    }

    exam_text = exam_instructions.get(exam, exam_instructions["Board 10"])
    lang_text = language_instructions.get(language, language_instructions["english"])

    prompt = f"""
{exam_text}

{lang_text}

Student's Question: {question}
Subject: {subject}
Exam Target: {exam}

Respond ONLY in this exact JSON format, no extra text:
{{
    "explanation": "Clear explanation of the concept",
    "example": "One relevant example or numerical solution with steps",
    "exam_tip": "One specific tip for {exam} exam",
    "difficulty": "Easy or Medium or Hard",
    "related_topics": ["topic1", "topic2", "topic3"],
    "quick_summary": "One line summary of the answer"
}}

RULES:
- explanation must be detailed but simple
- If question has a numerical, solve it step by step in example field
- exam_tip must be specific to {exam}
- related_topics must have exactly 3 topics
- quick_summary must be under 15 words
- Use the specified language throughout
- Never use these words: corpus, volatile, rebalancing
- Always be encouraging to the student
"""

    return prompt

if __name__ == "__main__":
    prompt = get_study_prompt("JEE", "Physics", "Newton ka 2nd law explain karo", "hinglish")
    print(prompt)
    print("---")
    prompt2 = get_study_prompt("NEET", "Biology", "Mitosis and meiosis difference", "english")
    print(prompt2)
