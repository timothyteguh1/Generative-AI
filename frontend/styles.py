import streamlit as st

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700&display=swap');

    /* --- 1. RESET GLOBAL --- */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    /* Paksa semua teks jadi Abu Gelap agar terbaca */
    p, h1, h2, h3, h4, h5, li, span, label, div {
        color: #2C3E50 !important;
    }
    /* Background Utama Cream Bersih */
    .stApp {
        background-color: #FFFBF2 !important;
    }

    /* --- 2. HEADER MODERN --- */
    .hero-container {
        background: #FFFFFF;
        padding: 2rem;
        border-radius: 24px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(211, 84, 0, 0.08);
        margin-bottom: 2rem;
        border-bottom: 4px solid #D35400;
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #D35400 !important;
        margin: 0;
    }

    /* --- 3. PERBAIKAN INPUT BAR --- */
    [data-testid="stBottom"] {
        background-color: #FFFBF2 !important;
        border-top: 1px solid #E0E0E0;
        padding-bottom: 20px;
        padding-top: 20px;
    }
    .stChatInput textarea {
        background-color: #FFFFFF !important;
        color: #333333 !important;
        border: 2px solid #D35400 !important;
        border-radius: 12px !important; /* Radius diperkecil sedikit agar fit dengan tema kotak */
        padding: 12px 20px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .stChatInput button {
        color: #D35400 !important;
    }

    /* --- 4. NEW: CUSTOM CHAT BUBBLES (Card Style / Shadcn-like) --- */
    /* Container Baris Chat */
    .chat-row {
        display: flex;
        gap: 12px;
        width: 100%;
        margin-bottom: 15px;
        align-items: flex-start;
    }
    .row-user { flex-direction: row-reverse; } /* User di kanan */
    .row-bot { flex-direction: row; } /* Bot di kiri */

    /* Avatar Kotak */
    .chat-avatar {
        width: 36px;
        height: 36px;
        border-radius: 8px; /* Kotak dengan sudut tumpul */
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        flex-shrink: 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .avatar-bot { background: #FFFFFF; border: 1px solid #E0E0E0; }
    .avatar-user { background: #D35400; color: white; }

    /* Bubble Chat (Kotak Rapi) */
    .chat-bubble {
        padding: 12px 16px;
        border-radius: 10px; /* Radius kecil agar terlihat modern/kotak */
        max-width: 80%;
        line-height: 1.5;
        font-size: 0.95rem;
        position: relative;
    }

    /* Gaya Spesifik BOT (Putih Bersih) */
    .bubble-bot {
        background: #FFFFFF;
        border: 1px solid #E0E0E0;
        color: #2C3E50;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    /* Label 'ChefBot' di atas bubble bot */
    .bubble-bot::before {
        content: "ChefBot";
        display: block;
        font-size: 0.65rem;
        font-weight: 700;
        color: #D35400;
        margin-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Gaya Spesifik USER (Cream/Oranye) */
    .bubble-user {
        background: #FFF3E0;
        border: 1px solid #FFCC80;
        color: #E65100;
        text-align: left; /* Tetap rata kiri agar mudah dibaca meski di kanan */
    }

    /* Sembunyikan Chat Default Streamlit agar tidak double */
    div[data-testid="stChatMessage"] {
        display: none;
    }

    /* --- 5. KARTU RESEP & LANGKAH --- */
    .info-card {
        background: #FFFFFF;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #F0F0F0;
        margin-bottom: 15px;
    }
    .card-header {
        font-weight: 700;
        color: #D35400 !important;
        margin-bottom: 10px;
        font-size: 1.1rem;
    }

    /* --- 6. TOMBOL & UPLOAD --- */
    .stButton button {
        background: #D35400 !important;
        color: white !important;
        border-radius: 8px !important; /* Diubah jadi agak kotak dikit */
        border: none !important;
        padding: 0.5rem 2rem !important;
        font-weight: 600;
    }
    .stButton button:hover {
        background: #E65100 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(211, 84, 0, 0.2);
    }

    /* Fix Upload Box */
    .streamlit-expanderHeader {
        background-color: #FFFFFF !important;
        color: #D35400 !important;
        border: 1px solid #D35400 !important;
        border-radius: 8px !important;
    }
    [data-testid="stFileUploader"] {
        background-color: #FFF8E1 !important;
        border: 2px dashed #D35400;
        border-radius: 12px;
    }
    [data-testid="stFileUploader"] section { background: transparent !important; }
    
    /* Hide default elements */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)