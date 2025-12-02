import google.generativeai as genai
from config import configure_ai

configure_ai()
model = genai.GenerativeModel('models/gemini-2.5-flash')
CYAN = "\033[96m"
RESET = "\033[0m"

def ask_chef_consultant(q, dish, step):
    print(f"{CYAN}[Consultant Agent] Menyiapkan jawaban...{RESET}")
    prompt = f"User masak '{dish}', langkah '{step}'. Tanya: '{q}'. Jawab santai."
    try: return model.generate_content(prompt).text
    except: return "Chef sibuk."