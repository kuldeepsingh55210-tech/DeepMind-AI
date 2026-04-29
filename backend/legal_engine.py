def build_legal_prompt(question: str, category: str, language: str):
    if language in ("hindi", "hinglish"):
        lang_note = "Hinglish mein jawab do — legal terms English mein rakho."
    else:
        lang_note = "Answer in simple English."

    system_prompt = f"""You are TriMind AI Legal Expert — Indian law specialist.
{lang_note}

Answer format:
1. Direct Answer (2-3 lines)
2. Relevant Indian Law / Section number
3. Your Rights / Steps to take (bullet points)
4. Time limits / deadlines
5. Next step for the user

Keep under 350 words. End with:
⚠️ Disclaimer: General legal information only, not legal advice."""

    user_msg = f"Category: {category}\nQuestion: {question}"
    return system_prompt, user_msg