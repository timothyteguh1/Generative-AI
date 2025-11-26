import google.generativeai as genai
import json
from config import configure_ai

configure_ai()
try: model = genai.GenerativeModel('models/gemini-2.5-flash')
except: model = genai.GenerativeModel('models/gemini-pro')

def clean_json(text):
    try:
        s = text.find('{'); e = text.rfind('}')
        return text[s:e+1] if s!=-1 else text
    except: return text

def generate_recipe_plan(dish):
    prompt = f"""
    Buat resep JSON untuk: {dish}. Bahasa Indonesia.
    JSON WAJIB:
    {{
        "dish": "Nama Masakan",
        "ingredients": ["Bahan 1", "Bahan 2"],
        "steps": [
            {{ "instruction": "Potong...", "visual_keyword": "chopping onion photorealistic" }}
        ]
    }}
    """
    try:
        res = model.generate_content(prompt)
        return json.loads(clean_json(res.text))
    except: return None