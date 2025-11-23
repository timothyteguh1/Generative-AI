import google.generativeai as genai
from config import configure_ai

# Setup
configure_ai()
# Gunakan model chat yang luwes
model = genai.GenerativeModel('models/gemini-2.5-flash')

def ask_chef_consultant(user_question, dish_name, current_step_text):
    """
    Menjawab pertanyaan user sesuai konteks resep yang sedang dimasak.
    """
    print(f"💬 [CONSULTANT] User bertanya: {user_question}")
    
    prompt = f"""
    Kamu adalah Chef Asisten yang ramah.
    Saat ini User sedang memasak: "{dish_name}".
    User sedang berada di langkah: "{current_step_text}".
    
    User bertanya: "{user_question}"
    
    Tugasmu:
    1. Jawab pertanyaan dengan singkat, padat, dan membantu.
    2. Fokus pada konteks masakan tersebut.
    3. Jangan berikan resep baru, tapi bantu dia menyelesaikan langkah ini.
    4. Gunakan bahasa Indonesia yang santai dan menyemangati.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "Maaf, Chef sedang sibuk di dapur sebelah. Bisa ulangi pertanyaannya?"