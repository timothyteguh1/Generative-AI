import streamlit as st

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

def render_step_card(idx, total, instruction, visual_key):
    # Gambar AI Otomatis
    img_url = f"https://image.pollinations.ai/prompt/{visual_key.replace(' ', '%20')}%20food%20photography?width=800&height=400&nologo=true"
    
    # Render Gambar
    st.image(img_url, use_container_width=True)
    
    # Render Teks Langkah
    st.markdown(f"""
    <div class="info-card" style="border-top: 4px solid #D35400; margin-top:15px;">
        <div class="card-header">🔥 Langkah {idx + 1} dari {total}</div>
        <p style="font-size:1.2rem; line-height:1.5;">{instruction}</p>
    </div>
    """, unsafe_allow_html=True)
    
    
def render_shopping_card(shopping_list):
    if not shopping_list: return

    # CSS Khusus Tombol Belanja
    st.markdown("""
    <style>
        .shop-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #F0F0F0;
        }
        .shop-name {
            font-weight: 600;
            color: #2C3E50;
            font-size: 0.95rem;
        }
        .shop-cat {
            font-size: 0.75rem;
            color: #95A5A6;
            background: #F4F6F7;
            padding: 2px 8px;
            border-radius: 4px;
            margin-left: 8px;
        }
        .shop-btn {
            text-decoration: none;
            padding: 5px 12px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 600;
            transition: 0.2s;
            display: inline-block;
            margin-left: 5px;
        }
        .btn-toped {
            background-color: #E5F9F1; /* Hijau Pudar Toped */
            color: #03AC0E !important; 
            border: 1px solid #03AC0E;
        }
        .btn-toped:hover { background-color: #03AC0E; color: white !important; }
        
        .btn-shopee {
            background-color: #FFF0F0; /* Oranye Pudar Shopee */
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
            Klik tombol untuk cari harga termurah di marketplace:
        </p>
    """, unsafe_allow_html=True)

    # Render List Bahan
    for item in shopping_list:
        st.markdown(f"""
        <div class="shop-row">
            <div>
                <span class="shop-name">{item['name']}</span>
                <span class="shop-cat">{item['category']}</span>
            </div>
            <div>
                <a href="{item['link_toped']}" target="_blank" class="shop-btn btn-toped">Tokopedia</a>
                <a href="{item['link_shopee']}" target="_blank" class="shop-btn btn-shopee">Shopee</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)