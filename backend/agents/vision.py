import google.generativeai as genai
import json
from config import configure_ai

configure_ai()
model = genai.GenerativeModel('models/gemini-2.5-flash')

CYAN = "\033[96m"
MAGENTA = "\033[95m"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def evaluate_cooking_step(image, instruction):
    print(f"{MAGENTA}[VISION AGENT] 👁️ Menganalisis foto masakan...{RESET}")
    
    prompt = f"""
    Compare the cooking image with this instruction: '{instruction}'.
    Analyze strictly based on visual appearance (doneness, texture, color).
    
    Return JSON with this schema:
    {{
        "status": "PASS" or "FAIL",
        "feedback": "Reason in Indonesian (max 15 words)"
    }}
    """
    
    try:
        # --- FITUR KUNCI: JSON MODE ---
        # Memaksa output hanya JSON valid. Anti-Error Parsing.
        res = model.generate_content(
            [prompt, image],
            generation_config=genai.types.GenerationConfig(
                temperature=0.4,
                response_mime_type="application/json" 
            )
        )
        
        data = json.loads(res.text)
        
        if data.get('status') == 'PASS':
            print(f"{GREEN}[VISION AGENT] ✅ PASS{RESET}")
        else:
            print(f"{RED}[VISION AGENT] ❌ FAIL: {data.get('feedback')}{RESET}")
            
        return data
        
    except Exception as e:
        print(f"{RED}[VISION ERROR] {e}{RESET}")
        return {"status": "FAIL", "feedback": "Gagal koneksi ke AI, coba lagi."}