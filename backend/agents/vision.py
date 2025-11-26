import google.generativeai as genai
import json
from config import configure_ai

configure_ai()
model = genai.GenerativeModel('models/gemini-2.5-flash')

def evaluate_cooking_step(image, instruction):
    prompt = f"Juri Masak. Instruksi: '{instruction}'. Cek foto. JSON: {{'status':'PASS'/'FAIL', 'feedback':'...'}}"
    try:
        res = model.generate_content([prompt, image])
        text = res.text.replace("```json","").replace("```","").strip()
        return json.loads(text)
    except: return {"status":"FAIL", "feedback":"Error Vision"}