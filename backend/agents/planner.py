import ollama
import json
# from config import configure_ai # Tidak diperlukan lagi

# configure_ai() # Hapus ini

CYAN = "\033[96m"
RESET = "\033[0m"

# Pastikan model ini sudah di-pull: 'ollama pull llama3'
MODEL_NAME = "llama3"

# --- FUNGSI 1: MEMBUAT RESEP (TEKS SAJA) ---
def generate_recipe_plan(dish):
    print(f"{CYAN}\n[PLANNER AGENT] 🧠 Meracik resep personal: {dish} (1 Porsi) dengan Ollama...{RESET}")
    
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
        "description": "Deskripsi singkat masakan",
        "ingredients": [
            "Bahan 1 (dengan takaran)",
            "Bahan 2 (dengan takaran)"
        ],
        "steps": [
            {{ "instruction": "Cuci bersih bahan..." }},
            {{ "instruction": "Panaskan minyak..." }}
        ]
    }}
    """
    
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            format='json', # Fitur JSON Mode Ollama
            messages=[{'role': 'user', 'content': prompt}]
        )
        # Parse string JSON dari response
        return json.loads(response['message']['content'])
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
    Output JSON (struktur sama seperti sebelumnya).
    """
    
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            format='json',
            messages=[{'role': 'user', 'content': prompt}]
        )
        return json.loads(response['message']['content'])
    except:
        return old_recipe