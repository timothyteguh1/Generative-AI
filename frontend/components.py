import streamlit as st
import os

def render_header():
    st.markdown("""
        <div class="hero-container">
            <div class="hero-title">👨‍🍳 ChefBot Pro</div>
            <small style="color:#888">Smart Cooking Assistant with AI</small>
        </div>
    """, unsafe_allow_html=True)

def render_chat_message(role, content):
    """
    Render chat custom dengan gaya Card/Box modern
    """
    if role == "user":
        # Layout User (Kanan)
        avatar = "👤"
        row_class = "row-user"
        bubble_class = "bubble-user"
        avatar_class = "avatar-user"
        align_style = "text-align: right;" # Text rata kanan
    else:
        # Layout Bot (Kiri)
        avatar = "👨‍🍳"
        row_class = "row-bot"
        bubble_class = "bubble-bot"
        avatar_class = "avatar-bot"
        align_style = "text-align: left;" # Text rata kiri

    # Render HTML Custom
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
    # Kita hapus bagian health_tip, hanya tampilkan Kalori & Protein
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
    """
    Render kartu langkah menggunakan GAMBAR LOKAL.
    """
    
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
    
    # --- LOGIKA GAMBAR LOKAL ---
    if image_path and os.path.exists(image_path):
        # Tampilkan gambar dari file lokal
        st.image(image_path, use_container_width=True)
    else:
        # Placeholder jika gambar gagal download
        st.warning(f"⚠️ Gambar tidak ditemukan: {image_path}")
        st.markdown(f"<div style='height:200px; background:#eee; display:flex; align-items:center; justify-content:center; color:#888;'>No Image Available</div>", unsafe_allow_html=True)
    
    # Render Teks
    st.markdown(f"""
        <div style="padding: 20px;">
            <p style="font-size: 1.1rem; line-height: 1.6; color: #2C3E50; margin: 0;">
                {instruction}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
def render_shopping_card(shopping_list):
    if not shopping_list: return

    # CSS Khusus Tombol Belanja & Layout Rapi
    st.markdown("""
    <style>
        .shop-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid #F0F0F0;
            gap: 15px; /* Jarak antar teks dan tombol */
        }
        
        /* Container Teks (Kiri) */
        .shop-info-col {
            flex-grow: 1; /* Mengisi ruang kosong */
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .shop-name {
            font-weight: 600;
            color: #2C3E50;
            font-size: 0.95rem;
            display: block;
            margin-bottom: 4px;
        }
        
        .shop-cat {
            font-size: 0.7rem;
            color: #7f8c8d;
            background: #F4F6F7;
            padding: 2px 8px;
            border-radius: 4px;
            display: inline-block;
            width: fit-content;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* Container Tombol (Kanan) - Fixed Width agar Rata */
        .shop-actions-col {
            flex-shrink: 0; /* Jangan mengecil */
            display: flex;
            gap: 5px;
        }

        .shop-btn {
            text-decoration: none;
            padding: 6px 14px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 600;
            transition: 0.2s;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            white-space: nowrap; /* Mencegah teks tombol turun baris */
        }
        
        .btn-toped {
            background-color: #E5F9F1;
            color: #03AC0E !important; 
            border: 1px solid #03AC0E;
        }
        .btn-toped:hover { background-color: #03AC0E; color: white !important; }
        
        .btn-shopee {
            background-color: #FFF0F0;
            color: #EE4D2D !important;
            border: 1px solid #EE4D2D;
        }
        .btn-shopee:hover { background-color: #EE4D2D; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

    # Header Card
    st.markdown("""
    <div class="info-card" style="border: 1px solid #F0F0F0;">
        <div class="card-header">🛒 Belanja Bahan</div>
        <p style="font-size:0.9rem; color:#7f8c8d !important; margin-bottom:15px;">
            Daftar belanja otomatis (Klik untuk beli):
        </p>
    """, unsafe_allow_html=True)

    # Render List Bahan
    for item in shopping_list:
        st.markdown(f"""
        <div class="shop-row">
            <div class="shop-info-col">
                <span class="shop-name">{item['name']}</span>
                <span class="shop-cat">{item['category']}</span>
            </div>
            <div class="shop-actions-col">
                <a href="{item['link_toped']}" target="_blank" class="shop-btn btn-toped">Tokopedia</a>
                <a href="{item['link_shopee']}" target="_blank" class="shop-btn btn-shopee">Shopee</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)