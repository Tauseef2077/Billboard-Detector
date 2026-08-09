import re
import easyocr
from rapidfuzz import fuzz

reader = easyocr.Reader(['en'])

TOBACCO_KEYWORDS = [

    # ============================
    # Global Cigarette Brands
    # ============================
    "marlboro", "camel", "winston", "parliament", "kent", "dunhill",
    "lucky strike", "luckystrike", "pall mall", "newport", "kool",
    "chesterfield", "davidoff", "rothmans", "gauloises", "bond",
    "lambert butler", "lambert & butler", "l&M", "lm", "ld cigarettes",
    "more cigarettes", "gitanes", "benson hedges", "benson & hedges",
    "benson", "hedges",

    # ============================
    # Indian Cigarette Brands
    # ============================
    "gold flake", "goldflake", "four square", "foursquare", "charms",
    "charm", "insignia", "classic", "red and white", "red&white",
    "navy cut", "kings", "kings cigarettes", "bidi", "beedi", "biri",
    "flake", "flake premium", "cool lip", "capstan", "scissors",
    "tipper", "tajpuri", "tajpuri bidi", "no 10 bidi",

    # ============================
    # Chewing Tobacco / Gutkha (India)
    # ============================
    "gutkha", "guthka", "gutka", "pan masala", "paan masala", "zarda",
    "tobacco", "chewing tobacco", "scented tobacco", "chaini khaini",
    "chaini khaini", "khaini", "surti", "jarda", "quiwam", "kimam",
    "mishri", "naswar", "snuff", "snus",

    # Popular Indian Gutkha Brands
    "vimal", "rmd", "rajshree", "parag", "manikchand", "madras", 
    "goa gutkha", "goa 1000", "pan parag", "pan bahar", 
    "tansen", "dilbagh", "vikram gutkha", "hanuman gutkha",
    "betel nut", "areca nut", "supari", "supary", "betelnut",

    # ============================
    # Hookah / Shisha / Rolling Papers
    # ============================
    "hookah", "shisha", "hubble bubble", "hooka", "sheesha",
    "rolling paper", "rolling papers", "raw papers", "raw rolling",
    "zig zag papers", "ocb", "clipper lighter", "pipe tobacco",
    "hookah tobacco", "shisha tobacco",

    # ============================
    # Vapes / E-Cigs / Nicotine Devices
    # ============================
    "vape", "vaping", "juul", "juulpods", "pod vape", "nicotine salt",
    "e cigarette", "ecigarette", "e cig", "ecig", "vape pen",
    "vaporizer", "mods", "vape juice", "nicotine", "nic salt",
    "e-liquid", "eliquid", "cloud vape", "disposable vape",

    # Common Vape Brands
    "iqos", "myle", "vuse", "relx", "elfbar", "hyde", "puffbar",

    # ============================
    # Generic Tobacco & Smoking Words
    # ============================
    "cigarette", "cigarettes", "smoking", "smoke", "tobacco",
    "nicotine", "tar", "filter cigarettes", "light cigarettes",
    "menthol cigarettes", "brown cigarettes", "bidi tobacco",
    "rolling tobacco", "tobacco shop", "cigar", "cigars", "cigarillo",

    # ============================
    # Legal / Illegal Tobacco Disclaimers
    # (If these appear → HIGH chance tobacco ad)
    # ============================
    "smoking kills", "smoking is injurious", 
    "tobacco kills", "tobacco is injurious", 
    "injurious to health", "statutory warning",

    # ============================
    # OCR Short Variations (optional)
    # ============================
    "marlbro", "winstn", "parliment", "goldflake", "gudkha",
    "guktha", "panmasala", "gutakah", "sisha", "shisa",

]

def Tobacco_predict(img_path):
    def extract_text(img_path):
        results = reader.readtext(img_path, detail=0)
        return " ".join(results)

    def clean_text(text):
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", "", text)
        return text


    def detect_tobacco(text, threshold=80):
        text = text.lower()
        matched_keywords = []

        for keyword in TOBACCO_KEYWORDS:
            score = fuzz.partial_ratio(keyword, text)
            if score >= threshold:
                matched_keywords.append((keyword, score))

        return matched_keywords

    def analyze_tobacco(img_path):
        raw = extract_text(img_path)
        cleaned = clean_text(raw)
        
        matchings = detect_tobacco(cleaned)
        yesno = True if matchings else False
        return {
            "tobacco_found": yesno,
            "keyword": matchings
        }
    return analyze_tobacco(img_path)
