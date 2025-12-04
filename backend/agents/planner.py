import google.generativeai as genai
import json
from config import configure_ai

configure_ai()
try: model = genai.GenerativeModel('models/gemini-2.5-flash')
except: model = genai.GenerativeModel('models/gemini-pro')

CYAN = "\033[96m"
RESET = "\033[0m"

def clean_json(text):
    try:
        s = text.find('{'); e = text.rfind('}')
        return text[s:e+1] if s!=-1 else text
    except: return text

# --- FUNGSI 1: MEMBUAT RESEP (TEKS SAJA) ---
def generate_recipe_plan(dish):
    print(f"{CYAN}\n[PLANNER AGENT] 🧠 Membuat struktur teks resep: {dish}...{RESET}")
    
    # HAPUS permintaan 'visual_keyword' dari prompt ini agar Planner ngebut!
    prompt = f"""
    Buat resep JSON untuk: {dish}. Bahasa Indonesia.
    
    JSON WAJIB:
    {{
        "dish": "{dish}",
        "ingredients": ["Bahan 1", "Bahan 2"],
        "steps": [
            {{ "instruction": "Potong bawang tipis-tipis..." }}
        ]
    }}
    """
    try:
        res = model.generate_content(prompt)
        return json.loads(clean_json(res.text))
    except: return None

# --- FUNGSI 2: REVISI RESEP ---
def refine_recipe_plan(old_recipe, critique):
    # Sama seperti di atas, hapus visual_keyword
    print(f"{CYAN}[PLANNER AGENT] 🛠️ Merevisi teks resep...{RESET}")
    prompt = f"""
    Resep '{old_recipe['dish']}' dikritik: "{critique}".
    Perbaiki 'ingredients' dan 'steps' agar lebih sehat.
    
    Output JSON:
    {{
        "dish": "{old_recipe['dish']}",
        "ingredients": ["..."],
        "steps": [ {{ "instruction": "..." }} ]
    }}
    """
    try:
        res = model.generate_content(prompt)
        return json.loads(clean_json(res.text))
    except: return old_recipe