import google.generativeai as genai
import json
import urllib.parse
from config import configure_ai

configure_ai()

# Prioritas: Gemini 2.5 Flash -> Fallback: 2.0 Flash / 1.5 Flash
try:
    model = genai.GenerativeModel('models/gemini-2.5-flash')
except:
    try:
        model = genai.GenerativeModel('models/gemini-2.0-flash-exp')
    except:
        model = genai.GenerativeModel('models/gemini-1.5-flash')

CYAN = "\033[96m"
RESET = "\033[0m"

def generate_shopping_list(ingredients):
    print(f"{CYAN}[SHOPPER AGENT] 🛒 Merapikan daftar belanja dengan AI...{RESET}")

    # Prompt Cerdas: Minta search_term khusus untuk E-commerce
    prompt = f"""
    Saya punya daftar bahan masakan: {ingredients}.
    
    Tugas:
    1. Identifikasi bahan UTAMA yang perlu dibeli.
    2. Bersihkan kata sifat (potongan, iris, secukupnya, untuk taburan).
    3. Tentukan kategori (Sayuran, Daging, Bumbu, dll).
    
    Output JSON WAJIB (Array of Objects):
    {{
        "items": [
            {{
                "display_name": "Nama Lengkap (misal: Ayam Kampung Potong 1kg)", 
                "search_term": "Ayam Kampung",  <-- KATA KUNCI BERSIH UNTUK PENCARIAN
                "category": "Daging"
            }}
        ]
    }}
    """
    
    try:
        # Gunakan JSON Mode agar output stabil
        res = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(response_mime_type="application/json")
        )
        data = json.loads(res.text)
        
        final_list = []
        for item in data.get('items', []):
            # Nama untuk ditampilkan di UI (Lengkap)
            display_name = item.get('display_name', item.get('name', 'Bahan'))
            
            # Kata kunci untuk Link (Bersih)
            keyword = item.get('search_term', display_name)
            
            # Encode URL
            query = urllib.parse.quote(keyword)
            
            final_item = {
                'name': display_name,
                'category': item.get('category', 'Bahan'),
                'link_toped': f"https://www.tokopedia.com/search?st=product&q={query}",
                'link_shopee': f"https://shopee.co.id/search?keyword={query}"
            }
            final_list.append(final_item)
            
        print(f"{CYAN}[SHOPPER AGENT] ✅ Link belanja siap!{RESET}")
        return final_list
        
    except Exception as e:
        print(f"\033[91m[SHOPPER AGENT] ❌ Error: {e}{RESET}")
        return []