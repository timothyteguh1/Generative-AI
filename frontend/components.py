import streamlit as st
import os
import re

# --- FILE: frontend/components.py ---

def render_header():
    st.markdown("""
        <div class="hero-container">
            <div class="hero-title">👨‍🍳 ChefBot Pro</div>
            <small style="color:#888">Smart Cooking Assistant with AI</small>
        </div>
    """, unsafe_allow_html=True)

def render_chat_message(role, content):
    if role == "user":
        avatar = "👤"
        row_class = "row-user"
        bubble_class = "bubble-user"
        avatar_class = "avatar-user"
        align_style = "text-align: right;" 
    else:
        avatar = "👨‍🍳"
        row_class = "row-bot"
        bubble_class = "bubble-bot"
        avatar_class = "avatar-bot"
        align_style = "text-align: left;"

    st.markdown(f"""
    <div class="chat-row {row_class}">
        <div class="chat-avatar {avatar_class}">{avatar}</div>
        <div class="chat-bubble {bubble_class}">
            <div style="{align_style}">{content}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_ingredient_card(ingredients):
    items = "".join([f"<li style='margin-bottom:5px;'>{i}</li>" for i in ingredients])
    st.markdown(f"""
    <div class="info-card" style="border-top: 4px solid #F39C12;">
        <div class="card-header">🛒 Bahan-Bahan</div>
        <ul style="padding-left:20px;">{items}</ul>
    </div>
    """, unsafe_allow_html=True)

def render_nutrition_card(nutri):
    if not nutri: return
    st.markdown(f"""
    <div class="info-card" style="background: #F1F8E9; border: 1px dashed #66BB6A;">
        <div class="card-header" style="color:#2E7D32 !important; margin-bottom: 10px;">🍎 Info Gizi (Per Porsi)</div>
        <div style="display:flex; justify-content:space-around; align-items:center;">
            <div style="text-align:center;">
                <span style="font-size: 1.5rem;">🔥</span><br>
                <b style="font-size: 1.2rem; color: #2C3E50;">{nutri.get('calories', '-')}</b><br>
                <small style="color:#666; text-transform:uppercase;">Kalori</small>
            </div>
            <div style="border-left: 1px solid #CCC; height: 40px;"></div>
            <div style="text-align:center;">
                <span style="font-size: 1.5rem;">💪</span><br>
                <b style="font-size: 1.2rem; color: #2C3E50;">{nutri.get('protein', '-')}</b><br>
                <small style="color:#666; text-transform:uppercase;">Protein</small>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_step_card(idx, total, instruction, image_path):
    st.markdown(f"""
    <div style="
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
        overflow: hidden;
        border: 1px solid #E0E0E0;
        margin-bottom: 20px;
    ">
        <div style="
            background: #D35400; 
            color: white; 
            padding: 8px 16px; 
            font-weight: bold;
            display: flex; justify-content: space-between;
        ">
            <span>🔥 Langkah {idx + 1}</span>
            <span>{idx + 1}/{total}</span>
        </div>
    """, unsafe_allow_html=True)
    
    # --- LOGIKA TAMPILAN GAMBAR (UPDATE) ---
    # Cek apakah image_path berisi URL (dimulai dengan http)
    if image_path and image_path.startswith("http"):
        # Tampilkan langsung dari internet
        st.image(image_path, use_container_width=True)
        
    # Cek apakah image_path adalah file lokal
    elif image_path and os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
        
    else:
        # Placeholder jika kosong
        st.markdown(f"""
        <div style='height:200px; background:#F9FAFB; display:flex; flex-direction:column; align-items:center; justify-content:center; color:#9CA3AF; border-bottom: 1px solid #eee;'>
            <span style='font-size:2rem;'>🍳</span>
            <span style='font-size:0.8rem; margin-top:5px;'>Menyiapkan ilustrasi...</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style="padding: 20px;">
            <p style="font-size: 1.1rem; line-height: 1.6; color: #2C3E50; margin: 0;">
                {instruction}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_shopping_card(shopping_list):
    """
    Versi UPDATE: Layout Rapi (Flexbox Center) & Pembersih Teks
    """
    if not shopping_list: return

    # CSS Khusus agar tombol sejajar (Align Items: Center)
    st.markdown("""
    <style>
        .shop-row {
            display: flex;
            align-items: center; /* KUNCI: Membuat vertikal tengah */
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid #F0F0F0;
            gap: 15px;
        }
        
        .shop-info-col {
            flex: 1; /* Mengambil sisa ruang */
            padding-right: 10px;
        }

        .shop-name {
            font-weight: 600;
            color: #2C3E50;
            font-size: 0.95rem;
            display: block;
            margin-bottom: 4px;
            line-height: 1.3;
        }
        
        .shop-cat {
            font-size: 0.7rem;
            color: #7f8c8d;
            background: #F4F6F7;
            padding: 2px 8px;
            border-radius: 4px;
            display: inline-block;
            text-transform: uppercase;
        }

        .shop-actions-col {
            display: flex;
            gap: 6px;
            flex-shrink: 0; /* Tombol tidak boleh mengecil */
            align-items: center;
        }

        .shop-btn {
            text-decoration: none !important;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 80px; /* Lebar minimum agar seragam */
            height: 30px;
        }
        
        .btn-toped { background-color: #E5F9F1; color: #03AC0E !important; border: 1px solid #03AC0E; }
        .btn-toped:hover { background-color: #03AC0E; color: white !important; }
        
        .btn-shopee { background-color: #FFF0F0; color: #EE4D2D !important; border: 1px solid #EE4D2D; }
        .btn-shopee:hover { background-color: #EE4D2D; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card" style="border: 1px solid #F0F0F0;">
        <div class="card-header">🛒 Belanja Bahan</div>
        <p style="font-size:0.9rem; color:#7f8c8d !important; margin-bottom:15px;">
            Klik tombol untuk beli langsung:
        </p>
    """, unsafe_allow_html=True)

    for item in shopping_list:
        raw_name = item['name']
        
        # --- LOGIKA PEMBERSIH ---
        # Hapus (potongan), (untuk sop), dll
        clean_name = re.sub(r'\s*\(.*?\)', '', raw_name).strip()
        
        st.markdown(f"""
        <div class="shop-row">
            <div class="shop-info-col">
                <span class="shop-name">{clean_name}</span>
                <span class="shop-cat">{item['category']}</span>
            </div>
            <div class="shop-actions-col">
                <a href="{item['link_toped']}" target="_blank" class="shop-btn btn-toped">Tokopedia</a>
                <a href="{item['link_shopee']}" target="_blank" class="shop-btn btn-shopee">Shopee</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)