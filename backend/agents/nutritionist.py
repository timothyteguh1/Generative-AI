import ollama
import json
import re # Import Regex untuk pembersihan

# Gunakan model yang kamu punya (gemma2:2b atau llama3)
MODEL_NAME = "gemma2:2b"

CYAN = "\033[96m"
RESET = "\033[0m"

def analyze_nutrition(recipe):
    print(f"{CYAN}[NUTRITIONIST AGENT] Menghitung angka gizi dengan Ollama...{RESET}")
    
    # Ambil bahan sebagai string bersih
    ingredients_text = str(recipe['ingredients'])
    
    prompt = f"""
    You are a Nutritionist. Analyze this recipe: "{recipe['dish']}".
    Ingredients: {ingredients_text}
    
    Task: Estimate Calories (kkal), Protein (g), Carbs (g), and Fat (g) per serving.
    
    RULES:
    1. Output ONLY a valid JSON object.
    2. Do NOT add any conversational text like "Here is the JSON".
    3. Use numbers only (Integer).
    
    JSON Format:
    {{
        "calories": 500,
        "protein": 20,
        "carbs": 50,
        "fat": 15
    }}
    """
    
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            format='json', # Paksa mode JSON
            messages=[{'role': 'user', 'content': prompt}]
        )
        
        raw_text = response['message']['content']
        print(f"[DEBUG NUTRITION]: {raw_text}") # Cek output di terminal
        
        # --- TEKNIK PEMBERSIHAN JSON ---
        # Kadang AI menambahkan teks di luar kurung kurawal. Kita potong paksa.
        start = raw_text.find('{')
        end = raw_text.rfind('}') + 1
        
        if start != -1 and end != -1:
            clean_json = raw_text[start:end]
            data = json.loads(clean_json)
        else:
            # Fallback jika tidak ketemu kurung kurawal
            data = {}

        # Return dengan format yang aman (Default '0' jika gagal baca angka)
        return {
            "calories": f"{data.get('calories', '0')} kkal",
            "protein": f"{data.get('protein', '0')}g",
            "carbs": f"{data.get('carbs', '0')}g",
            "fat": f"{data.get('fat', '0')}g"
        }
        
    except Exception as e:
        print(f"\033[91mError Nutritionist: {e}\033[0m")
        # Return strip jika error total
        return {"calories": "- kkal", "protein": "- g", "carbs": "-", "fat": "-"}