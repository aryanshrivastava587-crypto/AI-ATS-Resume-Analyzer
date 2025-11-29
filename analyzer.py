import re
from collections import Counter
from typing import Dict, List


STOPWORDS = {
    "the", "and", "or", "to", "of", "in", "for", "on", "a", "an", "with",
    "is", "are", "this", "that", "by", "as", "at", "be", "from", "it",
    "you", "your", "we", "our"
}


def _tokenize(text: str) -> List[str]:
    text = text.lower()
    text = re.sub(r"[^a-z0-9+]", " ", text)
    tokens = [t for t in text.split() if t and t not in STOPWORDS]
    return tokens


def analyze_match(resume_text: str, jd_text: str) -> Dict:
    """
    Very simple ATS-style keyword analysis.
    You can improve this later, but this is enough for V1.
    """
    resume_tokens = _tokenize(resume_text)
    jd_tokens = _tokenize(jd_text)

    resume_set = set(resume_tokens)
    jd_set = set(jd_tokens)

    matched = sorted(jd_set & resume_set)
    missing = sorted(jd_set - resume_set)

    # crude scoring
    if not jd_set:
        score = 0
    else:
        score = round(len(matched) / len(jd_set) * 100)

    resume_freq = Counter(resume_tokens)

    return {
        "score": score,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "resume_keyword_frequency": resume_freq.most_common(15)
    }
