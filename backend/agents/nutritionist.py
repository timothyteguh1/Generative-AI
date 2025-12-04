import google.generativeai as genai
import json
from config import configure_ai

configure_ai()
model = genai.GenerativeModel('models/gemini-2.5-flash')

CYAN = "\033[96m"
RESET = "\033[0m"

def analyze_nutrition(recipe):
    print(f"{CYAN}[NUTRITIONIST AGENT] Menghitung kalori presisi...{RESET}")
    
    prompt = f"""
    Analyze nutrition for: {recipe['dish']}.
    Ingredients: {recipe['ingredients']}
    
    Return JSON with exactly these keys. VALUES MUST BE STRINGS WITH UNITS:
    {{
        "calories": "e.g. 450 kkal",
        "protein": "e.g. 20g",
        "carbs": "e.g. 30g",
        "fat": "e.g. 15g"
    }}
    """
    
    try:
        res = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2, # Rendah agar angka konsisten/faktual
                response_mime_type="application/json"
            )
        )
        return json.loads(res.text)
    except:
        return {"calories": "-", "protein": "-", "carbs": "-", "fat": "-"}