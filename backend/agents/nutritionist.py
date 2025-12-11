import ollama
import json

# Pastikan model ini sudah di-pull
MODEL_NAME = "gemma2:2b" 

CYAN = "\033[96m"
RESET = "\033[0m"

def analyze_nutrition(recipe):
    print(f"{CYAN}[NUTRITIONIST AGENT] Menghitung angka gizi dengan Ollama...{RESET}")
    
    prompt = f"""
    Analisis resep: "{recipe['dish']}".
    Bahan: {recipe['ingredients']}
    
    Perkirakan Kalori dan Protein per porsi.
    
    ATURAN PENTING: Output HANYA ANGKA (Integer/Number), DILARANG menulis satuan (kkal/gram).
    
    JSON Schema Output:
    {{
        "calories": 500,
        "protein": 20,
        "carbs": 30,
        "fat": 15
    }}
    """
    
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            format='json',
            messages=[{'role': 'user', 'content': prompt}]
        )
        data = json.loads(response['message']['content'])
        
        return {
            "calories": f"{data.get('calories', '0')} kkal",
            "protein": f"{data.get('protein', '0')}g",
            "carbs": f"{data.get('carbs', '0')}g",
            "fat": f"{data.get('fat', '0')}g"
        }
    except Exception as e:
        print(f"Error Nutritionist: {e}")
        return {"calories": "- kkal", "protein": "- g", "carbs": "-", "fat": "-"}