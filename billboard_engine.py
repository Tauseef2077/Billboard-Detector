import os

# --- IMPORT MODULES ---
try:
    from ALCOHOL import Alcohol_predict
    from TOBACCO import Tobacco_predict
    from PROFANITY import Profanity_predict
    from NSFW import nsfw_predict
    from DESCRIPTION import description
    print("--- All AI Modules Imported Successfully ---")
except ImportError as e:
    print(f"CRITICAL ERROR: Missing a file or function. {e}")

# --- RULES & THRESHOLDS ---
NSFW_THRESHOLD = 50.0 

# 1. POSITIVE PHRASES (If these exist, we assume it's SAFE)
SAFE_PHRASES = [
    "good condition", 
    "no visible defects", 
    "structurally sound", 
    "excellent condition", 
    "no apparent defects",
    "safe condition"
]

# 2. NEGATIVE KEYWORDS (We only look for these if Positive Phrases are missing)
DAMAGE_KEYWORDS = [
    "rust", "crack", "bent", "loose", "damage", 
    "poor condition", "falling", "broken", "vegetation", 
    "disrepair", "hazard", "collapse"
]

def run_analysis_engine(image_path):
    print(f"--- Analyzing: {image_path} ---")
    
    # 1. RUN ALL MODELS
    try:
        alc_data = Alcohol_predict(image_path)
        tob_data = Tobacco_predict(image_path)
        prof_data = Profanity_predict(image_path)
        nsfw_score = nsfw_predict(image_path) 
        desc_text = description(image_path)   
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": f"Model Execution Failed: {str(e)}"}

    # 2. ANALYZE RESULTS
    
    # A. Content Flags
    is_alcohol = alc_data.get("alcohol_found", False)
    is_tobacco = tob_data.get("tobacco_found", False)
    is_profanity = prof_data.get("profanity_found", False)
    is_nsfw = nsfw_score > NSFW_THRESHOLD

    # ======================================================
    # B. SMART STRUCTURAL SAFETY CHECK (The Fix)
    # ======================================================
    desc_lower = desc_text.lower()
    structural_issues = []
    is_structure_unsafe = False

    # Step 1: Check if the AI explicitly said it is SAFE
    is_declared_safe = any(phrase in desc_lower for phrase in SAFE_PHRASES)

    if is_declared_safe:
        # If it says "good condition", we FORCE it to be safe, 
        # ignoring words like "rust" that might appear in "no rust".
        is_structure_unsafe = False
    else:
        # Step 2: Only check for damage keywords if it was NOT declared safe
        structural_issues = [word for word in DAMAGE_KEYWORDS if word in desc_lower]
        is_structure_unsafe = len(structural_issues) > 0

    # ======================================================

    # 3. DETERMINE FINAL VERDICT
    final_status = "SAFE / LEGAL"
    status_color = "green"
    reasons = []

    # Priority 1: Illegal/Restricted Content
    if is_nsfw:
        final_status = "ILLEGAL / UNSAFE"
        status_color = "red"
        reasons.append(f"NSFW Content Detected ({nsfw_score:.2f}%)")
    
    if is_alcohol:
        final_status = "RESTRICTED" if final_status != "ILLEGAL / UNSAFE" else final_status
        status_color = "orange" if status_color != "red" else "red"
        kws = [k[0] for k in alc_data.get("keyword", [])]
        reasons.append(f"Alcohol Ad ({', '.join(kws)})")

    if is_tobacco:
        final_status = "RESTRICTED" if final_status != "ILLEGAL / UNSAFE" else final_status
        status_color = "orange" if status_color != "red" else "red"
        kws = [k[0] for k in tob_data.get("keyword", [])]
        reasons.append(f"Tobacco Ad ({', '.join(kws)})")
        
    if is_profanity:
        final_status = "RESTRICTED" if final_status != "ILLEGAL / UNSAFE" else final_status
        status_color = "orange" if status_color != "red" else "red"
        kws = prof_data.get("keywords", [])
        reasons.append(f"Profanity Detected ({', '.join(kws)})")

    # Priority 2: Physical Safety
    if is_structure_unsafe:
        final_status = "PHYSICALLY UNSAFE"
        status_color = "red"
        reasons.append(f"Structural Damage Detected: {', '.join(structural_issues)}")

    # 4. CONSTRUCT FINAL JSON RESPONSE
    response = {
        "flags": {
            "alcohol": is_alcohol,
            "tobacco": is_tobacco,
            "profanity": is_profanity,
            "nsfw": is_nsfw,
            "structure_damage": is_structure_unsafe
        },
        "scores": {
            "nsfw_score": round(nsfw_score, 2)
        },
        "description": desc_text,
        "verdict": {
            "status": final_status,
            "color": status_color,
            "reasons": reasons
        }
    }
    
    return response