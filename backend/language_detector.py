"""
language_detector.py
Detects if a query is in Hinglish (Hindi + English mix) or plain English.
No external libraries required.
"""

# Common Hindi/Hinglish words that signal the user is writing in Hinglish
HINGLISH_KEYWORDS = [
    "mahine", "mahina", "saal", "kitna", "hoga", "karega", "karo", "mein",
    "mujhe", "chahiye", "kya", "hain", "hai", "ho", "aap", "main", "yaar",
    "bhai", "paisa", "paise", "rupaye", "invest", "karna", "karte", "karta",
    "milega", "milenge", "lagana", "lagao", "lagaye", "batao", "bata",
    "agar", "toh", "aur", "ya", "lekin", "par", "pe", "se", "ka", "ki",
    "ke", "ne", "ko", "ek", "do", "teen", "char", "paanch", "das", "sau",
    "hazaar", "lakh", "crore", "nahi", "nai", "haan", "thoda", "zyada",
]


def detect_language(query: str) -> str:
    """
    Returns 'hinglish' if the query contains Hinglish keywords,
    otherwise returns 'english'.
    """
    if not query:
        return "english"

    query_lower = query.lower()
    words = query_lower.split()

    for word in words:
        # Strip punctuation from each word
        clean_word = word.strip("?.,!;:'\"")
        if clean_word in HINGLISH_KEYWORDS:
            return "hinglish"

    return "english"
