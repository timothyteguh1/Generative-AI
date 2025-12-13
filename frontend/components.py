import streamlit as st
import os
import time
import textwrap # PENTING: Untuk memperbaiki masalah tampilan HTML

# --- FILE: frontend/components.py ---

def render_header():
    # Menggunakan dedent agar HTML tidak dianggap sebagai code block
    html_code = textwrap.dedent("""
        <div class="hero-container" style="text-align: center; padding: 30px 0;">
            <div class="hero-title" style="font-size: 3rem; font-weight: 800; color: #D35400;">👨‍🍳 ChefBot Pro</div>
            <small style="color:#888; font-size: 1.1rem;">Asisten Masak Pribadimu dengan AI</small>
        </div>
    """)
    st.markdown(html_code, unsafe_allow_html=True)

def render_chat_message(role, content):
    if role == "user":
        avatar = "👤"
        row_class = "row-user"
        bubble_class = "bubble-user"
        avatar_class = "avatar-user"
        align_style = "text-align: right;"
        bg_color = "#E3F2FD"
    else:
        avatar = "👨‍🍳"
        row_class = "row-bot"
        bubble_class = "bubble-bot"
        avatar_class = "avatar-bot"
        align_style = "text-align: left;"
        bg_color = "#FFF3E0"

    html_code = textwrap.dedent(f"""
    <div class="chat-row {row_class}" style="display: flex; gap: 10px; margin-bottom: 15px; align-items: flex-start;">
        <div class="chat-avatar {avatar_class}" style="font-size: 1.5rem; flex-shrink: 0;">{avatar}</div>
        <div class="chat-bubble {bubble_class}" style="background: {bg_color}; padding: 12px 16px; border-radius: 15px; max-width: 80%; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <div style="{align_style}; color: #2C3E50; line-height: 1.5;">{content}</div>
        </div>
    </div>
    """)
    st.markdown(html_code, unsafe_allow_html=True)

def render_ingredient_card(ingredients):
    items_html = ""
    for i in ingredients:
        text = ""
        if isinstance(i, dict):
            name = i.get('name', '')
            amount = i.get('amount', '')
            text = f"<b>{amount}</b> {name}".strip()
        else:
            text = str(i)
        items_html += f"<li style='margin-bottom:8px; color:#2C3E50; font-size: 0.95rem;'>{text}</li>"
    
    html_code = textwrap.dedent(f"""
    <div class="info-card" style="border-top: 4px solid #F39C12; background: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); margin-bottom: 20px;">
        <div class="card-header" style="background: #F39C12; color: white; padding: 10px 15px; font-weight: 700; border-radius: 12px 12px 0 0;">🛒 Bahan-Bahan</div>
        <ul style="padding: 15px 20px 15px 35px; margin:0;">
            {items_html}
        </ul>
    </div>
    """)
    st.markdown(html_code, unsafe_allow_html=True)

def render_nutrition_card(nutri):
    if not nutri: return
    cal = nutri.get('calories', '-')
    prot = nutri.get('protein', '-')
    carbs = nutri.get('carbs', '-') 
    fat = nutri.get('fat', '-')
    
    html_code = textwrap.dedent(f"""
    <div class="info-card" style="background: #F1F8E9; border: 2px dashed #66BB6A; border-radius: 12px; margin-bottom: 20px;">
        <div class="card-header" style="color:#2E7D32 !important; padding: 10px 15px; font-weight: 700;">🍎 Info Gizi (Per Porsi)</div>
        <div style="display:flex; justify-content:space-around; align-items:center; padding: 15px;">
            <div style="text-align:center;">
                <span style="font-size: 1.8rem;">🔥</span><br>
                <b style="font-size: 1.1rem; color: #2C3E50;">{cal}</b><br>
                <small style="color:#666;">Kalori</small>
            </div>
            <div style="text-align:center;">
                <span style="font-size: 1.8rem;">💪</span><br>
                <b style="font-size: 1.1rem; color: #2C3E50;">{prot}</b><br>
                <small style="color:#666;">Protein</small>
            </div>
            <div style="text-align:center;">
                <span style="font-size: 1.8rem;">🍞</span><br>
                <b style="font-size: 1.1rem; color: #2C3E50;">{carbs}</b><br>
                <small style="color:#666;">Karbo</small>
            </div>
            <div style="text-align:center;">
                <span style="font-size: 1.8rem;">💧</span><br>
                <b style="font-size: 1.1rem; color: #2C3E50;">{fat}</b><br>
                <small style="color:#666;">Lemak</small>
            </div>
        </div>
    </div>
    """)
    st.markdown(html_code, unsafe_allow_html=True)


# --- FUNGSI UI TIMER (DIPERBAIKI DENGAN LOGIKA STOP) ---
def render_timer_feature(step_key, default_duration):
    # Kunci Unik untuk Session State Timer ini
    timer_state_key = f"timer_end_time_{step_key}"

    with st.container():
        st.markdown("""
            <div style="background-color: #FFF3E0; padding: 15px; border-radius: 10px; border: 2px solid #FFE0B2;">
                <h5 style="color: #D35400; margin-top: 0; display: flex; align-items: center;">
                    ⏱️ Pengingat Waktu (Timer)
                </h5>
        """, unsafe_allow_html=True)

        try: val = int(default_duration)
        except: val = 2
        if val < 1: val = 1

        # Cek apakah timer sedang berjalan (ada end_time di session state dan waktu belum habis)
        is_running = False
        remaining_seconds = 0
        
        if timer_state_key in st.session_state:
            end_time = st.session_state[timer_state_key]
            remaining_seconds = int(end_time - time.time())
            if remaining_seconds > 0:
                is_running = True
            else:
                # Waktu habis
                del st.session_state[timer_state_key]
                st.balloons()
                st.success("⏰ WAKTU HABIS! Langkah selesai.")
                st.rerun()

        # Layout Kolom
        col_input, col_btn = st.columns([3, 2], gap="medium", vertical_alignment="bottom")

        with col_input:
            # Jika running, disable input biar user stop dulu kalau mau ubah
            duration = st.number_input(
                "Atur Menit:", 
                min_value=1, value=val, step=1, 
                key=f"time_input_{step_key}",
                disabled=is_running
            )
        
        with col_btn:
            if is_running:
                # TOMBOL STOP
                if st.button("⏹️ STOP TIMER", key=f"btn_stop_{step_key}", use_container_width=True, type="secondary"):
                    del st.session_state[timer_state_key] # Hapus state timer
                    st.rerun() # Refresh halaman
            else:
                # TOMBOL START
                if st.button("▶️ MULAI TIMER", key=f"btn_start_{step_key}", use_container_width=True, type="primary"):
                    # Set waktu selesai = sekarang + durasi
                    st.session_state[timer_state_key] = time.time() + (duration * 60)
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        # --- LOGIKA TAMPILAN COUNTDOWN ---
        if is_running:
            mins, secs = divmod(remaining_seconds, 60)
            timer_str = f"{mins:02d}:{secs:02d}"
            
            st.markdown(f"""
            <div style="
                text-align:center; 
                font-size: 3.5rem; 
                font-weight: 800; 
                color: #D35400;
                background-color: #FFF3E0;
                padding: 20px;
                border-radius: 12px;
                border: 3px solid #D35400;
                margin: 20px 0;
                box-shadow: 0 4px 10px rgba(211, 84, 0, 0.2);
            ">
                {timer_str}
            </div>
            <p style="text-align:center; color:#666;">Sedang berjalan...</p>
            """, unsafe_allow_html=True)
            
            # Auto-refresh setiap 1 detik
            time.sleep(1)
            st.rerun()


def render_step_card(idx, total, instruction, duration_minutes):
    # PERBAIKAN: Menggunakan textwrap.dedent agar HTML tidak dianggap sebagai CODE BLOCK
    html_card_top = f"""
    <div style="background: white; border-radius: 15px; box-shadow: 0 6px 20px rgba(0,0,0,0.1); overflow: hidden; border: 1px solid #EEE; margin-bottom: 25px;">
        <div style="background: linear-gradient(90deg, #D35400, #E67E22); color: white; padding: 12px 25px; font-weight: 700; display: flex; justify-content: space-between; align-items: center;">
            <span>🔥 Langkah {idx + 1}</span>
            <span style="background: rgba(255,255,255,0.2); padding: 2px 10px; border-radius: 10px; font-size: 0.9rem;">{idx + 1} dari {total}</span>
        </div>
        <div style="padding: 30px 25px;">
            <p style="font-size: 1.3rem; line-height: 1.6; color: #2C3E50; margin: 0 0 25px 0; font-weight: 500;">
                {instruction}
            </p>
            <hr style="border: 0; border-top: 2px dashed #FFE0B2; margin-bottom: 10px;">
    """
    
    st.markdown(html_card_top, unsafe_allow_html=True)
    
    # --- PANGGIL PANEL TIMER ---
    render_timer_feature(idx, duration_minutes)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def render_shopping_card(shopping_list):
    if not shopping_list: return
    
    css = textwrap.dedent("""
    <style>
        .shop-row { display: flex; align-items: center; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #F0F0F0; gap: 15px; }
        .shop-info-col { flex: 1; padding-right: 10px; }
        .shop-name { font-weight: 600; color: #2C3E50; font-size: 0.95rem; display: block; margin-bottom: 4px; line-height: 1.3; }
        .shop-cat { font-size: 0.7rem; color: #7f8c8d; background: #F4F6F7; padding: 2px 8px; border-radius: 4px; display: inline-block; text-transform: uppercase; }
        .shop-actions-col { display: flex; gap: 6px; flex-shrink: 0; align-items: center; }
        .shop-btn { text-decoration: none !important; padding: 6px 12px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; display: inline-flex; align-items: center; justify-content: center; min-width: 80px; height: 30px; transition: all 0.2s;}
        .btn-toped { background-color: #E5F9F1; color: #03AC0E !important; border: 1px solid #03AC0E; }
        .btn-toped:hover { background-color: #03AC0E; color: white !important; transform: translateY(-2px); box-shadow: 0 2px 5px rgba(3, 172, 14, 0.2);}
        .btn-shopee { background-color: #FFF0F0; color: #EE4D2D !important; border: 1px solid #EE4D2D; }
        .btn-shopee:hover { background-color: #EE4D2D; color: white !important; transform: translateY(-2px); box-shadow: 0 2px 5px rgba(238, 77, 45, 0.2);}
    </style>
    """)
    st.markdown(css, unsafe_allow_html=True)

    header_html = textwrap.dedent("""
    <div class="info-card" style="border: 1px solid #F0F0F0; background:white; border-radius:12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08);">
        <div class="card-header" style="background:#F8F9FA; padding:10px 15px; font-weight:700; border-radius:12px 12px 0 0;">🛒 Belanja Bahan</div>
        <div style="padding: 15px;">
    """)
    st.markdown(header_html, unsafe_allow_html=True)

    for item in shopping_list:
        row_html = textwrap.dedent(f"""
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
        """)
        st.markdown(row_html, unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)