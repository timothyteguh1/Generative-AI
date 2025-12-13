import ollama
import json

# Pastikan model ini sudah di-pull
MODEL_NAME = "llama3"

CYAN = "\033[96m"
RESET = "\033[0m"

# --- FUNGSI 1: MEMBUAT RESEP (TEKS + WAKTU) ---
def generate_recipe_plan(dish):
    print(f"{CYAN}\n[PLANNER AGENT] 🧠 Meracik resep & estimasi waktu: {dish} (1 Porsi)...{RESET}")
    
    # --- PROMPT DIPERBARUI UNTUK MEMINTA DURASI WAKTU ---
    prompt = f"""
    Kamu adalah Chef Profesional. Buatkan resep masakan untuk: "{dish}".
    Gunakan Bahasa Indonesia.
    
    ATURAN SANGAT PENTING (STRICT RULES):
    1. PORSI: WAJIB UNTUK 1 ORANG (Single Serving).
    2. BAHAN: Harus ada takaran spesifik (misal: "100g", "2 sdm").
    3. LANGKAH & WAKTU (SANGAT PENTING):
       - SATU LANGKAH = HANYA SATU AKSI FISIK.
       - Berikan estimasi waktu pengerjaan (duration_minutes) dalam Integer untuk setiap langkah.
       - Jika langkah sangat cepat (misal: sajikan), tulis 1 menit.
    
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
            {{ "instruction": "Cuci bersih kentang...", "duration_minutes": 5 }},
            {{ "instruction": "Goreng hingga matang...", "duration_minutes": 10 }}
        ]
    }}
    """
    
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            format='json',
            messages=[{'role': 'user', 'content': prompt}]
        )
        return json.loads(response['message']['content'])
    except Exception as e:
        print(f"Error Planner: {e}")
        return None

# --- FUNGSI 2: REVISI RESEP ---
def refine_recipe_plan(old_recipe, critique):
    print(f"{CYAN}[PLANNER AGENT] 🛠️ Merevisi resep sesuai request...{RESET}")
    
    prompt = f"""
    Konteks: Resep awal "{old_recipe['dish']}".
    Kritik User: "{critique}".
    
    Tugas: Perbaiki resep.
    
    ATURAN LANGKAH:
    - Pecah setiap langkah menjadi SATU AKSI per langkah.
    - Sertakan "duration_minutes" (integer) di setiap langkah revisi.
    
    Output JSON (Struktur sama seperti sebelumnya).
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