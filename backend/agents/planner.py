import google.generativeai as genai
import json
from config import configure_ai

configure_ai()

# Prioritas Model: 2.5 Flash -> Fallback ke 2.0 / 1.5 Flash
try:
    model = genai.GenerativeModel('models/gemini-2.5-flash')
except:
    try:
        model = genai.GenerativeModel('models/gemini-2.0-flash-exp')
    except:
        model = genai.GenerativeModel('models/gemini-1.5-flash')

CYAN = "\033[96m"
RESET = "\033[0m"

# --- FUNGSI 1: MEMBUAT RESEP (TEKS SAJA) ---
def generate_recipe_plan(dish):
    print(f"{CYAN}\n[PLANNER AGENT] 🧠 Meracik resep personal: {dish} (1 Porsi)...{RESET}")
    
    prompt = f"""
    Kamu adalah Chef Profesional. Buatkan resep masakan untuk: "{dish}".
    Gunakan Bahasa Indonesia.
    
    ATURAN SANGAT PENTING (STRICT RULES):
    1. PORSI: WAJIB UNTUK 1 ORANG (Single Serving). Jangan buat porsi keluarga.
    2. BAHAN: Harus ada takaran spesifik yang masuk akal untuk 1 orang (Contoh: "100g Dada Ayam", "2 butir Telur", "1 sdt Garam").
    3. LANGKAH: Jelas, runtut, dan mudah diikuti pemula.
    
    Output WAJIB JSON dengan struktur ini:
    {{
        "dish": "{dish}",
        "portion": "1 Orang",
        "description": "Deskripsi singkat masakan yang menggugah selera (maks 1 kalimat)",
        "ingredients": [
            "Bahan 1 (dengan takaran)",
            "Bahan 2 (dengan takaran)"
        ],
        "steps": [
            {{ "instruction": "Cuci bersih bahan, lalu potong dadu..." }},
            {{ "instruction": "Panaskan minyak..." }}
        ]
    }}
    """
    
    try:
        # Gunakan JSON Mode agar tidak perlu parsing manual yang rawan error
        res = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(response_mime_type="application/json")
        )
        return json.loads(res.text)
    except Exception as e:
        print(f"Error Planner: {e}")
        return None

# --- FUNGSI 2: REVISI RESEP ---
def refine_recipe_plan(old_recipe, critique):
    print(f"{CYAN}[PLANNER AGENT] 🛠️ Merevisi resep sesuai request...{RESET}")
    
    prompt = f"""
    Konteks: Resep awal "{old_recipe['dish']}" (Porsi 1 Orang).
    Kritik User: "{critique}".
    
    Tugas: Perbaiki resep agar sesuai kritik, TETAPI TETAP UNTUK 1 ORANG.
    
    Output JSON:
    {{
        "dish": "{old_recipe['dish']}",
        "portion": "1 Orang",
        "ingredients": ["..."],
        "steps": [ {{ "instruction": "..." }} ]
    }}
    """
    
    try:
        res = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(response_mime_type="application/json")
        )
        return json.loads(res.text)
    except:
        return old_recipe