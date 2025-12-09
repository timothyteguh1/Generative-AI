import google.generativeai as genai
from config import configure_ai

configure_ai()

# Prioritas: Gemini 2.5 Flash
try:
    model = genai.GenerativeModel('models/gemini-2.5-flash')
except:
    model = genai.GenerativeModel('models/gemini-1.5-flash')

CYAN = "\033[96m"
RESET = "\033[0m"

def ask_chef_consultant(q, dish, step):
    print(f"{CYAN}[Consultant Agent] Chef sedang mengetik...{RESET}")
    
    # --- PERSONA OPTIMIZATION ---
    prompt = f"""
    Roleplay: Kamu adalah "Chef Gemoy", asisten masak yang ramah, lucu, suportif, dan ahli.
    Gaya Bicara: Gunakan Bahasa Indonesia yang santai, gaul tapi sopan. Gunakan emoji masakan (👨‍🍳, 🔥, 🍳) sesekali.
    
    Konteks Pengguna:
    - Sedang memasak: '{dish}'
    - Posisi sekarang di langkah: '{step}'
    
    Pertanyaan User: "{q}"
    
    Instruksi:
    1. Jawab pertanyaan dengan singkat, padat, dan solutif.
    2. Berikan tips tambahan jika relevan.
    3. Jika pertanyaan di luar topik masak, arahkan kembali ke dapur dengan candaan halus.
    """
    
    try: 
        res = model.generate_content(prompt)
        return res.text
    except: 
        return "Waduh, Chef lagi sibuk icip-icip nih. Coba tanya lagi ya! 🍲"