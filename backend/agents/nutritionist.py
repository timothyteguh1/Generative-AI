import google.generativeai as genai
import json
from config import configure_ai

configure_ai()

# Prioritas: Gemini 2.5 Flash -> Fallback
try:
    model = genai.GenerativeModel('models/gemini-2.5-flash')
except:
    model = genai.GenerativeModel('models/gemini-1.5-flash')

CYAN = "\033[96m"
RESET = "\033[0m"

def analyze_nutrition(recipe):
    print(f"{CYAN}[NUTRITIONIST AGENT] Menghitung angka gizi...{RESET}")
    
    prompt = f"""
    Analisis resep: "{recipe['dish']}".
    Bahan: {recipe['ingredients']}
    
    Perkirakan Kalori dan Protein per porsi.
    
    ATURAN PENTING: Output HANYA ANGKA (Integer/Number), DILARANG menulis satuan (kkal/gram).
    
    JSON Schema:
    {{
        "calories": 500,
        "protein": 20,
        "carbs": 30,
        "fat": 15
    }}
    """
    
    try:
        res = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.1, # Rendah agar angka konsisten/faktual
                response_mime_type="application/json"
            )
        )
        data = json.loads(res.text)
        
        # Python menambahkan satuan agar format UI Cantik
        return {
            "calories": f"{data.get('calories', '0')} kkal",
            "protein": f"{data.get('protein', '0')}g",
            "carbs": f"{data.get('carbs', '0')}g",
            "fat": f"{data.get('fat', '0')}g"
        }
    except:
        return {"calories": "- kkal", "protein": "- g", "carbs": "-", "fat": "-"}