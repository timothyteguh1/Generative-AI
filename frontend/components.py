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