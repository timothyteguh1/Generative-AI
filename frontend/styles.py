import streamlit as st

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700&display=swap');

    /* --- 1. RESET GLOBAL --- */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
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

    /* --- 3. CUSTOM CHAT INPUT (Gaya Gambar Ke-2: Capsule Gray) --- */
    
    /* Area Sticky di Bawah */
    [data-testid="stBottom"] {
        background-color: #FFFBF2 !important; 
        border-top: 1px solid #F0F0F0;
        padding-bottom: 20px;
        padding-top: 20px;
    }

    /* KOTAK INPUT UTAMA (PILL SHAPE) */
    .stChatInput textarea {
        background-color: #F3F4F6 !important; /* Abu-abu muda persis referensi */
        color: #374151 !important; /* Teks abu gelap */
        border: 1px solid transparent !important; /* Hilangkan border default */
        border-radius: 9999px !important; /* Membuat ujungnya bulat sempurna (Capsule) */
        padding: 14px 24px !important; /* Padding luas biar lega */
        box-shadow: none !important; /* Flat design */
        font-size: 0.95rem;
        transition: all 0.2s ease;
    }
    
    /* Efek saat diklik/fokus: Jadi Putih dengan Shadow halus */
    .stChatInput textarea:focus {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
    }

    /* TOMBOL KIRIM (Paper Plane) */
    .stChatInput button {
        color: #9CA3AF !important; /* Abu-abu soft */
        background: transparent !important;
        border: none !important;
        transition: 0.3s;
        margin-right: 10px; /* Geser dikit dari kanan */
    }
    
    /* Tombol Kirim saat Hover */
    .stChatInput button:hover {
        color: #D35400 !important; /* Jadi Oranye */
        background-color: rgba(211, 84, 0, 0.1) !important;
        border-radius: 50%;
    }

    /* Sembunyikan instruksi 'Press Enter to send' */
    .stChatInput div[data-testid="stInputInstructions"] {
        display: none;
    }

    /* --- 4. NEW: CUSTOM CHAT BUBBLES --- */
    .chat-row {
        display: flex;
        gap: 12px;
        width: 100%;
        margin-bottom: 15px;
        align-items: flex-start;
    }
    .row-user { flex-direction: row-reverse; } 
    .row-bot { flex-direction: row; }

    /* Avatar Kotak */
    .chat-avatar {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        flex-shrink: 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .avatar-bot { background: #FFFFFF; border: 1px solid #E0E0E0; }
    .avatar-user { background: #D35400; color: white; }

    /* Bubble Chat */
    .chat-bubble {
        padding: 12px 18px;
        border-radius: 18px; /* Lebih bulat */
        max-width: 80%;
        line-height: 1.5;
        font-size: 0.95rem;
        position: relative;
    }

    /* Bot: Putih */
    .bubble-bot {
        background: #FFFFFF;
        border: 1px solid #F3F4F6;
        color: #2C3E50;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        border-top-left-radius: 4px;
    }
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

    /* User: Oranye Pudar */
    .bubble-user {
        background: #FFF3E0; /* Cream Oranye */
        color: #B45309;
        border-top-right-radius: 4px;
    }

    /* --- 5. KARTU RESEP & INFO --- */
    .info-card {
        background: #FFFFFF;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        border: 1px solid #F3F4F6;
        margin-bottom: 15px;
    }
    .card-header {
        font-weight: 700;
        color: #D35400 !important;
        margin-bottom: 10px;
        font-size: 1.1rem;
    }

    /* --- 6. TOMBOL UMUM & UPLOAD --- */
    .stButton button {
        background: #D35400 !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0.5rem 2rem !important;
        font-weight: 600;
    }
    .stButton button:hover {
        background: #E65100 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(211, 84, 0, 0.2);
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