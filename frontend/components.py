import streamlit as st
import os

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
    # CSS Inline color black agar teks bahan terlihat jelas
    items = "".join([f"<li style='margin-bottom:5px; color:#2C3E50;'>{i}</li>" for i in ingredients])
    
    st.markdown(f"""
    <div class="info-card" style="border-top: 4px solid #F39C12;">
        <div class="card-header">🛒 Bahan-Bahan</div>
        <ul style="padding-left:20px; color:#2C3E50; margin:0;">
            {items}
        </ul>
    </div>
    """, unsafe_allow_html=True)

def render_nutrition_card(nutri):
    if not nutri: return
    
    # Data dari Backend sudah bersih (misal: "500 kkal", "20g")
    cal = nutri.get('calories', '-')
    prot = nutri.get('protein', '-')
    carbs = nutri.get('carbs', '-') 
    fat = nutri.get('fat', '-')
    
    st.markdown(f"""
    <div class="info-card" style="background: #F1F8E9; border: 1px dashed #66BB6A;">
        <div class="card-header" style="color:#2E7D32 !important; margin-bottom: 10px;">🍎 Info Gizi (Per Porsi)</div>
        <div style="display:flex; justify-content:space-around; align-items:center;">
            <div style="text-align:center;">
                <span style="font-size: 1.5rem;">🔥</span><br>
                <b style="font-size: 1.2rem; color: #2C3E50;">{cal}</b><br>
                <small style="color:#666; text-transform:uppercase;">Kalori</small>
            </div>
            <div style="border-left: 1px solid #CCC; height: 40px;"></div>
            <div style="text-align:center;">
                <span style="font-size: 1.5rem;">💪</span><br>
                <b style="font-size: 1.2rem; color: #2C3E50;">{prot}</b><br>
                <small style="color:#666; text-transform:uppercase;">Protein</small>
            </div>
            <div style="border-left: 1px solid #CCC; height: 40px;"></div>
            <div style="text-align:center;">
                <span style="font-size: 1.5rem;">🍞</span><br>
                <b style="font-size: 1.2rem; color: #2C3E50;">{carbs}</b><br>
                <small style="color:#666; text-transform:uppercase;">Karbo</small>
            </div>
            <div style="border-left: 1px solid #CCC; height: 40px;"></div>
            <div style="text-align:center;">
                <span style="font-size: 1.5rem;">💧</span><br>
                <b style="font-size: 1.2rem; color: #2C3E50;">{fat}</b><br>
                <small style="color:#666; text-transform:uppercase;">Lemak</small>
            </div>
            
        
    </div>
    """, unsafe_allow_html=True)

def render_step_card(idx, total, instruction, image_path):
    st.markdown(f"""
    <div style="
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        overflow: hidden;
        border: 1px solid #E0E0E0;
        margin-bottom: 20px;
        display: flex;
        flex-direction: column;
    ">
        <div style="
            background: #D35400; 
            color: white; 
            padding: 10px 20px; 
            font-weight: 700;
            display: flex; justify-content: space-between;
            font-size: 0.95rem;
        ">
            <span>🔥 Langkah {idx + 1}</span>
            <span>{idx + 1}/{total}</span>
        </div>
    """, unsafe_allow_html=True)
    
    # --- AREA GAMBAR RESPONSIF ---
    st.markdown("""
    <style>
        .step-image-container {
            width: 100%;
            max-height: 350px;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #F9FAFB;
        }
        .step-image-container img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
    </style>
    <div class="step-image-container">
    """, unsafe_allow_html=True)

    if image_path and image_path.startswith("http"):
        st.image(image_path, use_container_width=True)
    elif image_path and os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
    else:
        st.markdown(f"""
        <div style='padding:40px; text-align:center; color:#9CA3AF;'>
            <span style='font-size:2rem;'>🍳</span><br>
            <small>Menyiapkan ilustrasi...</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style="padding: 20px 24px;">
            <p style="font-size: 1.05rem; line-height: 1.6; color: #374151; margin: 0;">
                {instruction}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_shopping_card(shopping_list):
    """
    Versi FINAL: Tanpa Regex Cleaner (karena Backend sudah bersih).
    """
    if not shopping_list: return

    # CSS Layout Tombol
    st.markdown("""
    <style>
        .shop-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid #F0F0F0;
            gap: 15px;
        }
        .shop-info-col { flex: 1; padding-right: 10px; }
        .shop-name {
            font-weight: 600; color: #2C3E50; font-size: 0.95rem;
            display: block; margin-bottom: 4px; line-height: 1.3;
        }
        .shop-cat {
            font-size: 0.7rem; color: #7f8c8d; background: #F4F6F7;
            padding: 2px 8px; border-radius: 4px;
            display: inline-block; text-transform: uppercase;
        }
        .shop-actions-col { display: flex; gap: 6px; flex-shrink: 0; align-items: center; }
        .shop-btn {
            text-decoration: none !important; padding: 6px 12px;
            border-radius: 6px; font-size: 0.75rem; font-weight: 700;
            display: inline-flex; align-items: center; justify-content: center;
            min-width: 80px; height: 30px;
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
        <p style="font-size:0.9rem; color:black !important; margin-bottom:15px;">
            Klik tombol untuk beli langsung:
        </p>
    """, unsafe_allow_html=True)

    for item in shopping_list:
        # Backend sudah mengirim 'name' yang bersih (search_term) jika diinginkan,
        # atau 'display_name' lengkap.
        # Karena kita sudah optimasi backend agar 'name' itu Display Name yang bagus, 
        # kita tampilkan apa adanya.
        
        display_name = item['name']
        category = item['category']
        
        st.markdown(f"""
        <div class="shop-row">
            <div class="shop-info-col">
                <span class="shop-name">{display_name}</span>
                <span class="shop-cat">{category}</span>
            </div>
            <div class="shop-actions-col">
                <a href="{item['link_toped']}" target="_blank" class="shop-btn btn-toped">Tokopedia</a>
                <a href="{item['link_shopee']}" target="_blank" class="shop-btn btn-shopee">Shopee</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)