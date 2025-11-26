import google.generativeai as genai
import json
from config import configure_ai

configure_ai()
model = genai.GenerativeModel('models/gemini-2.5-flash')

def analyze_nutrition(recipe):
    # Prompt disederhanakan: HAPUS permintaan 'health_tip'
    prompt = f"Analisis gizi '{recipe['dish']}'. JSON: {{'calories':'Angka saja (misal 500 kkal)','protein':'Angka saja (misal 20g)'}}"
    try:
        res = model.generate_content(prompt)
        text = res.text.replace("```json","").replace("```","").strip()
        s = text.find('{'); e = text.rfind('}')
        return json.loads(text[s:e+1])
    except: return None