import ollama
import json
import urllib.parse

# Gunakan model yang terinstall (llama3 atau gemma2:2b)
MODEL_NAME = "llama3"

CYAN = "\033[96m"
RESET = "\033[0m"

def generate_shopping_list(ingredients):
    print(f"{CYAN}[SHOPPER AGENT] 🛒 Merapikan daftar belanja dengan Ollama...{RESET}")

    # --- LANGKAH 1: BERSIHKAN INPUT ---
    # Ubah format rumit [{'name': 'Nasi', 'amount': '200g'}] 
    # Menjadi teks simpel ["200g Nasi", ...] agar AI tidak bingung.
    
    cleaned_ingredients = []
    for item in ingredients:
        if isinstance(item, dict):
            # Gabungkan amount + name
            text = f"{item.get('amount', '')} {item.get('name', '')}".strip()
            cleaned_ingredients.append(text)
        else:
            # Jika sudah string, langsung pakai
            cleaned_ingredients.append(str(item))
            
    # Ubah list menjadi string koma (item1, item2, item3)
    ingredients_text = ", ".join(cleaned_ingredients)

    # --- LANGKAH 2: PROMPT BARU ---
    # Hapus instruksi "Bahan Utama" agar semua bahan masuk list.
    
    prompt = f"""
    Task: Convert this list of cooking ingredients into a structured Shopping List.
    Ingredients: "{ingredients_text}"
    
    Rules:
    1. Include ALL ingredients from the list (do not skip spices/condiments).
    2. Simplify the names for search (e.g., "200g Cold White Rice" -> "Beras Putih").
    3. Categorize them (Vegetable, Meat, Spice, Pantry).
    4. Output strictly JSON.
    
    Output JSON Schema:
    {{
        "items": [
            {{
                "display_name": "Full Name (e.g. 200g Nasi Putih)", 
                "search_term": "Short Search Keyword (e.g. Beras)",
                "category": "Category Name"
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
        
        # Parse JSON
        content = response['message']['content']
        # Pembersihan ekstra jika ada teks sampah
        start = content.find('{')
        end = content.rfind('}') + 1
        if start != -1 and end != -1:
            data = json.loads(content[start:end])
        else:
            data = json.loads(content)
        
        final_list = []
        for item in data.get('items', []):
            display_name = item.get('display_name', 'Bahan')
            keyword = item.get('search_term', display_name)
            
            # Encode URL untuk link belanja
            query = urllib.parse.quote(keyword)
            
            final_item = {
                'name': display_name,
                'category': item.get('category', 'Bahan'),
                'link_toped': f"https://www.tokopedia.com/search?st=product&q={query}",
                'link_shopee': f"https://shopee.co.id/search?keyword={query}"
            }
            final_list.append(final_item)
            
        print(f"{CYAN}[SHOPPER AGENT] ✅ Link belanja siap! ({len(final_list)} items){RESET}")
        return final_list
        
    except Exception as e:
        print(f"\033[91m[SHOPPER AGENT] ❌ Error: {e}{RESET}")
        # Fallback manual jika AI error: Bikin link dari list mentah
        fallback_list = []
        for ing in cleaned_ingredients:
            query = urllib.parse.quote(ing)
            fallback_list.append({
                'name': ing,
                'category': 'Umum',
                'link_toped': f"https://www.tokopedia.com/search?st=product&q={query}",
                'link_shopee': f"https://shopee.co.id/search?keyword={query}"
            })
        return fallback_list