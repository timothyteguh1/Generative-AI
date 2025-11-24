import google.generativeai as genai
import json
from config import configure_ai

# Setup
configure_ai()
# Gunakan model yang tersedia
try:
    model = genai.GenerativeModel('models/gemini-2.5-flash')
except:
    model = genai.GenerativeModel('models/gemini-pro')

def clean_json_text(text):
    try:
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            return text[start : end + 1]
        return text
    except:
        return text

def analyze_nutrition(recipe_data):
    print("\n🍎 [NUTRITIONIST] Menganalisis kandungan gizi...")
    
    prompt = f"""
    Kamu adalah Ahli Gizi (Nutritionist).
    
    Analisis resep berikut:
    Nama: {recipe_data['dish']}
    Bahan: {recipe_data['ingredients']}
    
    Tugas: Estimasi kandungan gizi PER PORSI.
    
    OUTPUT WAJIB JSON:
    {{
        "calories": "angka (misal: 450 kkal)",
        "protein": "angka (misal: 20g)",
        "carbs": "angka (misal: 50g)",
        "fats": "angka (misal: 15g)",
        "health_tip": "Satu kalimat saran kesehatan singkat (Bahasa Indonesia) terkait resep ini."
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        clean_text = clean_json_text(response.text)
        return json.loads(clean_text)
    except Exception as e:
        print(f"❌ [NUTRITION ERROR] {e}")
        return None