import ollama

MODEL_NAME = "llama3"

CYAN = "\033[96m"
RESET = "\033[0m"

def ask_chef_consultant(q, dish, step):
    print(f"{CYAN}[Consultant Agent] Chef sedang mengetik (Ollama)...{RESET}")
    
    prompt = f"""
    Roleplay: Kamu adalah "Chef Gemoy", asisten masak yang ramah, lucu, suportif, dan ahli.
    Gaya Bicara: Gunakan Bahasa Indonesia yang santai, gaul tapi sopan. Gunakan emoji masakan (👨‍🍳, 🔥, 🍳) sesekali.
    
    Konteks Pengguna:
    - Sedang memasak: '{dish}'
    - Posisi sekarang di langkah: '{step}'
    
    Pertanyaan User: "{q}"
    
    Instruksi: Jawab singkat, padat, solutif.
    """
    
    try: 
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response['message']['content']
    except: 
        return "Waduh, Chef lagi sibuk icip-icip nih. Coba tanya lagi ya! 🍲"