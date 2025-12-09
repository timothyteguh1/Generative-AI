import streamlit as st

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700&display=swap');

    /* --- 1. RESET GLOBAL & RESPONSIVE FIX --- */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Background Utama */
    .stApp {
        background-color: #FFFBF2 !important;
    }
    /* --- FIX: WARNA TEKS SPINNER (LOADING) --- */
    /* Ini yang bikin teks 'Chef sedang meracik...' jadi Hitam */
    div[data-testid="stSpinner"] {
        color: #2C3E50 !important;
    }
    div[data-testid="stSpinner"] > div {
        color: #2C3E50 !important;
        font-weight: 600 !important; /* Biar agak tebal */
    }
    

    /* PENTING: Mencegah gambar melebar keluar layar di HP */
    img {
        max-width: 100% !important;
        height: auto !important;
        border-radius: 12px;
    }

    /* --- 2. HEADER --- */
    .hero-container {
        background: #FFFFFF;
        padding: 2rem 1rem; /* Padding lebih kecil di mobile */
        border-radius: 24px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(211, 84, 0, 0.08);
        margin-bottom: 2rem;
        border-bottom: 4px solid #D35400;
    }
    .hero-title {
        font-size: clamp(1.8rem, 5vw, 2.5rem); /* Font size otomatis mengecil di HP */
        font-weight: 800;
        color: #D35400 !important;
        margin: 0;
    }

    /* --- 3. INPUT CHAT (CAPSULE STYLE) --- */
    [data-testid="stBottom"] {
        background-color: #FFFBF2 !important; 
        border-top: 1px solid #F0F0F0;
        padding-bottom: 20px;
        padding-top: 20px;
    }
    .stChatInput textarea {
        background-color: #F3F4F6 !important;
        color: #374151 !important;
        border: 1px solid transparent !important;
        border-radius: 9999px !important;
        padding: 14px 24px !important;
        box-shadow: none !important;
    }
    .stChatInput textarea:focus {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
    }
    .stChatInput button {
        color: #9CA3AF !important;
        background: transparent !important;
        border: none !important;
        margin-right: 10px;
    }
    .stChatInput button:hover {
        color: #D35400 !important;
        background-color: rgba(211, 84, 0, 0.1) !important;
        border-radius: 50%;
    }
    .stChatInput div[data-testid="stInputInstructions"] { display: none; }

    /* --- 4. CHAT BUBBLES (Zebra Style) --- */
    .chat-row {
        display: flex;
        gap: 12px;
        width: 100%;
        margin-bottom: 12px;
        align-items: flex-end;
    }
    .row-user { flex-direction: row-reverse; } 
    .row-bot { flex-direction: row; }

    .chat-avatar {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        flex-shrink: 0;
    }
    .avatar-bot { background: #FFFFFF; border: 1px solid #EEE; color: #D35400; }
    .avatar-user { background: #D35400; color: white; }

    .chat-bubble {
        padding: 12px 18px;
        border-radius: 16px;
        max-width: 85%; /* Lebih lebar dikit */
        line-height: 1.5;
        font-size: 0.95rem;
        position: relative;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .bubble-bot {
        background-color: #FFFFFF; 
        color: #2C3E50;
        border: 1px solid #E5E7EB;
        border-bottom-left-radius: 2px;
    }
    .bubble-user {
        background-color: #FFE0B2; 
        color: #8C3200;
        border: none;
        border-bottom-right-radius: 2px;
    }

    /* --- 5. KARTU CONTENT --- */
    .info-card {
        background: #FFFFFF;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: 1px solid #F0F0F0;
        margin-bottom: 15px;
        width: 100%; /* Pastikan full width */
    }
    .card-header { font-weight: 700; color: #D35400 !important; margin-bottom: 10px; font-size: 1.1rem; }

    /* BUTTONS */
    .stButton button {
        background: #D35400 !important; color: white !important;
        border-radius: 8px !important; border: none !important;
        padding: 0.5rem 2rem !important; font-weight: 600;
        width: 100%; /* Tombol full width di mobile */
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)