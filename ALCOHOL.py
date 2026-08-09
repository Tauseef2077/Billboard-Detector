ALCOHOL_KEYWORDS = [
    # --- Core alcohol types ---
    "beer", "whisky", "vodka", "rum", "gin", "scotch",
    "tequila", "brandy", "wine",

    # --- Global beer brands ---
    "kingfisher", "budweiser", "corona", "heineken",
    "tuborg", "carlsberg", "miller", "hoegaarden",

    # --- Indian liquor brands ---
    "royal stag", "blenders pride", "officers choice",
    "mc dowell", "imperial blue", "signature",
    "old monk", "magic moments", "bira",
    "haywards", "black dog", "100 pipers",
    "antiquity", "royal challenge", "bagpiper",
    "rockford", "oaksmith",

    # --- Common alcohol-related terms ---
    "lager", "brewery", "distillery", "single malt","premium blend"
]

import re
import easyocr
from rapidfuzz import fuzz

reader = easyocr.Reader(['en'])

def Alcohol_predict(img_path):
    def extract_text(img_path):
        results = reader.readtext(img_path, detail=0)
        return " ".join(results)

    def clean_text(text):
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", "", text)
        return text


    def detect_alcohol_fuzzy(text, threshold=82):
        text = text.lower()
        matched_keywords = []

        for keyword in ALCOHOL_KEYWORDS:
            score = fuzz.partial_ratio(keyword, text)
            if score >= threshold:
                matched_keywords.append((keyword, score))

        return matched_keywords

    def analyze_alcohol(img_path):
        raw = extract_text(img_path)
        cleaned = clean_text(raw)
        
        matchings = detect_alcohol_fuzzy(cleaned)
        yesno = True if matchings else False
        return {
            "alcohol_found": yesno,
            "keyword": matchings
        }
    return analyze_alcohol(img_path)


