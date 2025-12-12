import ollama
import json

# Pastikan model ini sudah di-pull
MODEL_NAME = "llama3"

CYAN = "\033[96m"
RESET = "\033[0m"

# --- FUNGSI 1: MEMBUAT RESEP (TEKS SAJA) ---
def generate_recipe_plan(dish):
    print(f"{CYAN}\n[PLANNER AGENT] 🧠 Meracik resep personal: {dish} (1 Porsi) dengan Ollama...{RESET}")
    
    # --- PERUBAHAN UTAMA DI SINI (PROMPT LEBIH GALAK) ---
    prompt = f"""
    Kamu adalah Chef Profesional. Buatkan resep masakan untuk: "{dish}".
    Gunakan Bahasa Indonesia.
    
    ATURAN SANGAT PENTING (STRICT RULES):
    1. PORSI: WAJIB UNTUK 1 ORANG (Single Serving).
    2. BAHAN: Harus ada takaran spesifik (misal: "100g", "2 sdm").
    3. LANGKAH (SANGAT PENTING):
       - SATU LANGKAH = HANYA SATU AKSI FISIK.
       - DILARANG menggabungkan dua kegiatan dalam satu nomor.
       - Contoh SALAH: "Cuci kentang, kupas kulitnya, lalu potong dadu." (Ini 3 aksi).
       - Contoh BENAR:
         1. "Cuci bersih kentang dengan air mengalir."
         2. "Kupas kulit kentang hingga bersih."
         3. "Potong kentang menjadi bentuk dadu kecil."
       - Pecah langkah menjadi detail agar mudah difoto per langkahnya.
    
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
            {{ "instruction": "Langkah 1 (Satu Aksi)" }},
            {{ "instruction": "Langkah 2 (Satu Aksi)" }}
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
    - Pecah setiap langkah menjadi SATU AKSI per langkah (Single Action per Step).
    - Jangan gabungkan "Cuci dan Potong" dalam satu langkah. Pisahkan jadi dua langkah.
    
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