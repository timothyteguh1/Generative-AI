import ollama
import json

# Pastikan model ini sudah di-pull di Ollama Anda (misal: llama3)
MODEL_NAME = "llama3"

CYAN = "\033[96m"
RESET = "\033[0m"

# --- FUNGSI 1: MEMBUAT RESEP (PROFESSIONAL CHEF STANDARD) ---
def generate_recipe_plan(dish):
    print(f"{CYAN}\n[PLANNER AGENT] 👨‍🍳 Executive Chef meracik resep Premium: {dish}...{RESET}")
    
    # --- PROMPT: EXECUTIVE CHEF STANDARD ---
    prompt = f"""
    Bertindaklah sebagai **EXECUTIVE CHEF HOTEL BINTANG 5**.
    Tugas: Buatkan resep "Signature Dish" untuk menu: "{dish}" (1 Porsi).
    
    STANDAR KUALITAS (WAJIB):
    1. **RASA HARUS MEWAH (DELICIOUS)**:
       - Jangan buat resep hambar/sederhana ala anak kos.
       - GUNAKAN BUMBU AROMATIK: Bawang merah, bawang putih, bombay, daun bawang, atau rempah yang relevan.
       - MAIN FLAVOR: Pastikan ada keseimbangan rasa (Gurih, Manis, Asin).
    
    2. **AUDIT BAHAN (SANGAT KETAT)**:
       - Cek setiap langkah. Jika ada kata "Tumis/Goreng", WAJIB ada "Minyak Goreng" atau "Butter" di list ingredients.
       - Jika ada kata "Rebus", WAJIB ada "Air" di list ingredients.
       - Jangan lupa bumbu dasar: Garam, Gula, Merica/Lada, Kaldu Jamur/Ayam. Tulis di ingredients!
    
    3. **LANGKAH MEMASAK (DETAILED & PRO)**:
       - DILARANG langkah yang terlalu sedikit/pendek. Minimal 6-10 langkah.
       - Bagi menjadi fase: [PERSIAPAN BAHAN] -> [PROSES MASAK] -> [PENYAJIAN].
       - Satu langkah = Satu aksi spesifik (Micro-Steps).
       - Contoh Pro: "Panaskan wajan hingga berasap sedikit (wok hei) sebelum memasukkan minyak." (Ini instruksi chef asli).
    
    4. **DURASI**:
       - Berikan estimasi waktu (integer menit) yang realistis untuk setiap langkah.
    
    Output WAJIB JSON valid:
    {{
        "dish": "{dish} Spesial Chef",
        "portion": "1 Orang",
        "description": "Deskripsi masakan yang menggugah selera dengan kata-kata premium...",
        "ingredients": [
            "Minyak Goreng (2 sdm)", 
            "Bawang Putih (2 siung, cincang)",
            "Dada Ayam (100g, potong dadu)",
            "Nasi Putih (200g)",
            "Kecap Manis (1 sdm)",
            "Garam (1/2 sdt)",
            "Lada Bubuk (1/4 sdt)",
            "Telur (1 butir)",
            "Daun Bawang (iris tipis)"
        ],
        "steps": [
            {{ "instruction": "Siapkan semua bahan (Mise en place). Cincang halus bawang putih dan potong ayam.", "duration_minutes": 5 }},
            {{ "instruction": "Panaskan wajan dengan api besar, tuang minyak goreng.", "duration_minutes": 2 }},
            {{ "instruction": "Tumis bawang putih hingga harum keemasan.", "duration_minutes": 2 }},
            {{ "instruction": "Masukkan ayam, masak hingga berubah warna.", "duration_minutes": 3 }},
            {{ "instruction": "Masukkan nasi, aduk cepat dengan api besar.", "duration_minutes": 3 }},
            {{ "instruction": "Tambahkan kecap, garam, dan lada. Aduk rata (Koreksi Rasa).", "duration_minutes": 2 }}
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
    print(f"{CYAN}[PLANNER AGENT] 🛠️ Executive Chef merevisi menu...{RESET}")
    
    prompt = f"""
    Konteks: Resep awal "{old_recipe['dish']}".
    Kritik User: "{critique}".
    
    Tugas: Revisi resep agar lebih sempurna.
    
    ATURAN:
    1. Pastikan bahan SANGAT LENGKAP (Cek Minyak, Air, Bumbu).
    2. Langkah harus detail (Step-by-step professional).
    3. Output JSON sama seperti struktur sebelumnya.
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