import ollama
import json
import urllib.parse

MODEL_NAME = "llama3"

CYAN = "\033[96m"
RESET = "\033[0m"

def generate_shopping_list(ingredients):
    print(f"{CYAN}[SHOPPER AGENT] 🛒 Merapikan daftar belanja dengan Ollama...{RESET}")

    prompt = f"""
    Saya punya daftar bahan masakan: {ingredients}.
    
    Tugas:
    1. Identifikasi bahan UTAMA yang perlu dibeli.
    2. Bersihkan kata sifat (potongan, iris, secukupnya).
    3. Tentukan kategori.
    
    Output JSON WAJIB:
    {{
        "items": [
            {{
                "display_name": "Nama Lengkap", 
                "search_term": "KATA KUNCI BERSIH",
                "category": "Daging/Sayur/Bumbu"
            }}
        ]
    }}
    """
    
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            format='json',
            messages=[{'role': 'user', 'content': prompt}]
        )
        data = json.loads(response['message']['content'])
        
        final_list = []
        for item in data.get('items', []):
            display_name = item.get('display_name', item.get('name', 'Bahan'))
            keyword = item.get('search_term', display_name)
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