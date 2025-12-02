import google.generativeai as genai
import json
from config import configure_ai

configure_ai()
model = genai.GenerativeModel('models/gemini-2.5-flash')


CYAN = "\033[96m"
RESET = "\033[0m"

def analyze_nutrition(recipe):
    print(f"{CYAN}[NUTRITIONIST AGENT] Menghitung kalori dari resep...{RESET}")
    # Prompt disederhanakan: HAPUS permintaan 'health_tip'
    prompt = f"Analisis gizi '{recipe['dish']}'. JSON: {{'calories':'Angka saja (misal 500 kkal)','protein':'Angka saja (misal 20g)'}}"
    try:
        res = model.generate_content(prompt)
        text = res.text.replace("```json","").replace("```","").strip()
        s = text.find('{'); e = text.rfind('}')
        return json.loads(text[s:e+1])
    except: return None