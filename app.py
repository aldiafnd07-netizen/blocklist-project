import hashlib
import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import random
import base64
import os

# --- 1. SISTEM DATABASE & KEAMANAN ---
def hash_password(password):
    salt = "S2SEJATISLOT_RAHASIA_77" 
    password_plus_salt = password + salt
    return hashlib.sha256(password_plus_salt.encode()).hexdigest()

def init_db():
    conn = sqlite3.connect('database_s2.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT, email TEXT, telepon TEXT,
                  bank TEXT, norek TEXT, narek TEXT, referral TEXT)''')
    conn.commit()
    conn.close()

def cek_login(u, p):
    conn = sqlite3.connect('database_s2.db')
    c = conn.cursor()
    p_hashed = hash_password(p)
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p_hashed))
    data = c.fetchone()
    conn.close()
    return data

def simpan_pendaftar(u, p, e, t, b, nr, na, ref):
    try:
        conn = sqlite3.connect('database_s2.db')
        c = conn.cursor()
        p_hashed = hash_password(p)
        c.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?,?)", (u, p_hashed, e, t, b, nr, na, ref))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

init_db()

# --- 2. LOGIKA NAVIGASI & STATE ---
if 'v_code' not in st.session_state:
    st.session_state.v_code = str(random.randint(1000, 9999))

if 'page' not in st.session_state:
    st.session_state.page = 'lobby'

if 'current_game_url' not in st.session_state:
    st.session_state.current_game_url = ""

def pindah_ke_game(url):
    st.session_state.current_game_url = url
    st.session_state.page = 'game'

def kembali_ke_lobby():
    st.session_state.page = 'lobby'

# --- 3. FUNGSI TAMPILAN GAME (IFRAME) ---
def tampilan_game():
    st.markdown("""
        <style>
            header, footer { visibility: hidden !important; }
            .stApp { background-color: #000 !important; }
        </style>
    """, unsafe_allow_html=True)
    
    if st.button("⬅️ KEMBALI KE LOBBY", type="primary"):
        kembali_ke_lobby()
        st.rerun()
    
    # Menampilkan game secara penuh
    components.iframe(st.session_state.current_game_url, height=800, scrolling=True)

# --- 4. LOGIKA HALAMAN LOBBY ---
if st.session_state.page == 'lobby':
    
    # Video Background & Global CSS
    def get_base64_video():
        nama_video = "undefined - Imgur.mp4"
        paths = [nama_video, f"/sdcard/Download/{nama_video}", f"home/S2-Sejatislot/{nama_video}"]
        for p in paths:
            if os.path.exists(p):
                with open(p, "rb") as f:
                    return base64.b64encode(f.read()).decode()
        return None

    bin_str = get_base64_video()
    if bin_str:
        st.markdown(f'''
        <style>
            header, footer, #MainMenu, .stDeployButton {{ visibility: hidden !important; }}
            .stApp {{ background: transparent !important; }}
            #video-container {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; overflow: hidden; }}
            #bg-video {{ width: 100%; height: 100%; object-fit: cover; }}
            .block-container {{ padding: 0.5rem !important; padding-bottom: 160px !important; background-color: rgba(0,0,0,0.4); }}
        </style>
        <div id="video-container">
            <video autoplay loop muted playsinline id="bg-video">
                <source src="data:video/mp4;base64,{bin_str}" type="video/mp4">
            </video>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''<style>header, footer, #MainMenu, .stDeployButton { visibility: hidden !important; } .stApp { background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url("https://i.imgur.com/39Y3aPz.mp4"); background-size: cover; }</style>''', unsafe_allow_html=True)

    st.markdown("""<style>.stTextInput input { background-color: rgba(26, 29, 36, 0.9) !important; color: #00e676 !important; border: 1px solid #ffd700 !important; } div.stButton > button[kind="primary"] { background: linear-gradient(180deg, #00e676 0%, #00c853 100%) !important; color: white !important; font-weight: 800 !important; border: 2px solid #ffd700 !important; border-radius: 12px !important; }</style>""", unsafe_allow_html=True)

    # Dialog Login & Daftar
    @st.dialog("HALAMAN MASUK")
    def login_dialog():
        u = st.text_input("User Name", key="l_u")
        p = st.text_input("Kata Sandi", type="password", key="l_p")
        if st.button("PROSES MASUK", type="primary", use_container_width=True):
            if cek_login(u, p): st.success(f"✅ Halo {u}, Selamat Bermain!"); st.balloons()
            else: st.error("⚠️ Akun tidak ditemukan!")

    @st.dialog("PENDAFTARAN", width="large")
    def register_dialog():
        st.markdown("### 📝 DAFTAR AKUN BARU")
        col1, col2 = st.columns(2)
        with col1:
            u = st.text_input("* User Name", key="reg_u")
            p = st.text_input("* Kata sandi", type="password", key="reg_p")
            p2 = st.text_input("* Ulang Kata sandi", type="password", key="reg_p2")
            e = st.text_input("Email (Opsional)", key="reg_e")
        with col2:
            t = st.text_input("* No Telepon", key="reg_t")
            b = st.selectbox("* Bank", ["BCA", "MANDIRI", "BNI", "BRI", "DANA", "OVO", "GOPAY"])
            nr = st.text_input("* Nomor Rekening", key="reg_nr")
            ref = st.text_input("Kode Referral", key="reg_ref")
        na = st.text_input("* Nama Pemilik Rekening", key="reg_na")
        st.markdown(f"**Kode Validasi: :red[{st.session_state.v_code}]**")
        v_in = st.text_input("* Masukkan Kode", key="reg_v")
        if st.button("DAFTAR SEKARANG", type="primary", use_container_width=True):
            if p != p2: st.error("❌ Kata sandi tidak cocok!")
            elif v_in != st.session_state.v_code: st.error("❌ Kode validasi salah!")
            elif u and p and nr and na:
                if simpan_pendaftar(u, p, e, t, b, nr, na, ref):
                    st.success("✅ Berhasil! Silakan Login.")
                    st.session_state.v_code = str(random.randint(1000, 9999))
                else: st.error("⚠️ Username sudah ada!")

    # Header
    c1, c2 = st.columns([2, 1])
    with c1: st.image("https://i.imgur.com/pjj1xQo.png", width=200)
    with c2:
        if st.button("MASUK", use_container_width=True): login_dialog()
        if st.button("DAFTAR", use_container_width=True): register_dialog()

    # Fitur HTML (Lobby Mewah)
    fitur_html = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
        .s-container { width: 100%; overflow: hidden; border-radius: 15px; border: 2px solid #ffd700; position: relative; }
        .s-wrapper { display: flex; overflow-x: auto; scroll-snap-type: x mandatory; scrollbar-width: none; }
        .s-wrapper::-webkit-scrollbar { display: none; }
        .s-wrapper img { width: 100%; flex-shrink: 0; scroll-snap-align: start; }
        .marquee-rgb { margin-top: 10px; padding: 3px; border-radius: 10px; background: linear-gradient(90deg, red, yellow, lime, cyan, blue, magenta, red); background-size: 400%; animation: rgb 5s linear infinite; }
        .marquee-inner { background: #1a1d24; border-radius: 8px; padding: 10px; overflow: hidden; }
        .m-text { display: inline-block; white-space: nowrap; color: #ffd700; font-weight: bold; animation: jalan 15s linear infinite; }
        .jp-card { background: #000; border: 2px solid #ffd700; border-radius: 15px; padding: 10px; text-align: center; margin-top: 10px; }
        .jp-text { color: red; font-size: 24px; font-weight: 900; text-shadow: 0 0 5px red; font-family: 'Orbitron', sans-serif; }
        .game-section { position: relative; margin-top: 15px; padding: 0 5px; }
        .nav-btn { background: rgba(0,0,0,0.8); color: gold; border: 1px solid gold; border-radius: 50%; width: 30px; height: 30px; position: absolute; top: 60%; transform: translateY(-50%); z-index: 10; cursor: pointer; font-weight: bold; }
        .btn-l { left: -5px; } .btn-r { right: -5px; }
        .game-header { color: gold; font-weight: bold; font-size: 14px; margin-bottom: 8px; }
        .game-scroll { display: flex; overflow-x: auto; scroll-behavior: smooth; gap: 12px; scrollbar-width: none; }
        .game-scroll::-webkit-scrollbar { display: none; }
        .game-card { flex: 0 0 130px; background: #111; border: 1px solid gold; border-radius: 12px; overflow: hidden; }
        .game-card img { width: 100%; height: 130px; object-fit: cover; }
        .game-info { padding: 6px 2px; font-size: 11px; color: white; font-weight: bold; text-align: center; }
        .rtp-container { background: #333; border-radius: 20px; margin: 0 8px 8px 8px; height: 16px; position: relative; overflow: hidden; }
        .rtp-fill { height: 100%; border-radius: 20px; display: flex; align-items: center; justify-content: center; font-size: 10px; color: black; font-weight: 900; }
        @keyframes rgb { 0%{background-position:0%} 100%{background-position:100%} }
        @keyframes jalan { from { transform: translateX(100%); } to { transform: translateX(-100%); } }
    </style>
    <div class="s-container"><div class="s-wrapper" id="slider"><img src="https://i.imgur.com/IA1m2GF.png"><img src="https://i.imgur.com/vUeCcl3.png"><img src="https://i.imgur.com/kek6NF4.png"></div></div>
    <div class="marquee-rgb"><div class="marquee-inner"><div class="m-text">🔥 S2 SEJATI - SITUS GACOR TERPERCAYA - WD BERAPAPUN PASTI DIBAYAR LUNAS! 🔥</div></div></div>
    <div class="jp-card"><div style="color:#ffd700; font-size:10px; font-weight:bold;">✨ PROGRESSIVE JACKPOT ✨</div><div class="jp-text">RP <span id="jp-val">8.715.820.442</span></div></div>
    <div class="game-section">
        <div class="game-header">🎰 GAME HOT HARI INI</div>
        <button class="nav-btn btn-l" onclick="sc(-140)">&#10094;</button><button class="nav-btn btn-r" onclick="sc(140)">&#10095;</button>
        <div class="game-scroll" id="gs">
            <div class="game-card"><img src="https://i.imgur.com/Bt3aCqC.jpeg"><div class="game-info">Olympus</div><div class="rtp-container"><div class="rtp-fill" style="width: 98%; background: #00e676;">98%</div></div></div>
            <div class="game-card"><img src="https://i.imgur.com/qI9UKNO.jpeg"><div class="game-info">Starlight</div><div class="rtp-container"><div class="rtp-fill" style="width: 97%; background: #00e676;">97%</div></div></div>
            <div class="game-card"><img src="https://i.imgur.com/Sh4Y4Jz.jpeg"><div class="game-info">Mahjong 2</div><div class="rtp-container"><div class="rtp-fill" style="width: 95%; background: gold;">95%</div></div></div>
            <div class="game-card"><img src="https://i.imgur.com/qI9UKNO.jpeg"><div class="game-info">Bonanza</div><div class="rtp-container"><div class="rtp-fill" style="width: 93%; background: #00e676;">93%</div></div></div>
        </div>
    </div>
    <div id="chat-btn" onclick="toggleChat(true)" style="position: fixed; bottom: 100px; right: 20px; width: 60px; height: 60px; background: radial-gradient(circle, #ffd700, #ff8c00); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 30px; box-shadow: 0 0 15px gold; z-index: 999; cursor: pointer;">💬</div>
    <div id="chat-overlay" onclick="toggleChat(false)" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 10000;"></div>
    <div id="chat-popup" style="display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 300px; background: #1a1d24; border: 2px solid gold; border-radius: 20px; overflow: hidden; z-index: 10001;">
        <div style="background:gold; padding:10px; color:black; font-weight:bold; display:flex; justify-content:space-between;"><span>CS ONLINE</span><span onclick="toggleChat(false)" style="cursor:pointer">X</span></div>
        <div style="padding:10px;">
            <a href="https://wa.me/6285724785177" style="display:block; padding:10px; color:white; text-decoration:none; border-bottom:1px solid #333;">WhatsApp</a>
            <a href="https://t.me/aldiafnd07" style="display:block; padding:10px; color:white; text-decoration:none;">Telegram</a>
        </div>
    </div>
    <script>
    const slider = document.getElementById('slider');
    let idx = 0; setInterval(() => { if(slider){ idx = (idx + 1) % 3; slider.scrollTo({left: slider.offsetWidth * idx, behavior: 'smooth'}); }}, 4500);
    let jpVal = 8715820442; setInterval(() => { jpVal += Math.floor(Math.random()*100); if(document.getElementById('jp-val')) document.getElementById('jp-val').innerText = jpVal.toLocaleString('id-ID'); }, 200);
    function toggleChat(s) { document.getElementById('chat-overlay').style.display = s?'block':'none'; document.getElementById('chat-popup').style.display = s?'block':'none'; }
    const g = document.getElementById('gs');
    function sc(v) { g.scrollBy({left: v, behavior:'smooth'}); }
    setInterval(() => { if(g) { if(g.scrollLeft >= (g.scrollWidth - g.offsetWidth - 1)) g.scrollLeft = 0; else g.scrollBy({left: 1, behavior: 'auto'}); }}, 40);
    </script>
    """
    components.html(fitur_html, height=850)

    # Login Area & Tombol Game
    st.markdown("### 🔑 LOGIN UTAMA")
    u_m = st.text_input("Username", key="main_u")
    p_m = st.text_input("Password", type="password", key="main_p")
    if st.button("MASUK SEKARANG", type="primary", use_container_width=True):
        if cek_login(u_m, p_m): st.success("✅ Login Berhasil!"); st.balloons()
        else: st.error("⚠️ Username/Password salah!")

    st.markdown("---")
    st.markdown("### 🎮 PILIH GAME ANDA")
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        if st.button("🎰 GATES OF OLYMPUS", use_container_width=True):
            pindah_ke_game("https://demogamesfree.pragmaticplay.net/gs2c/openGame.do?gameSymbol=vs20olympgate&lang=id")
            st.rerun()
    with col_g2:
        if st.button("👸 STARLIGHT PRINCESS", use_container_width=True):
            pindah_ke_game("https://demogamesfree.pragmaticplay.net/gs2c/openGame.do?gameSymbol=vs20starlight&lang=id")
            st.rerun()

    # Navigasi Bawah
    st.markdown("""
    <style>
        .nav { position: fixed; bottom: 0; left: 0; width: 100%; height: 75px; background: #111; display: flex; align-items: center; z-index: 9999; border-top: 2px solid gold; }
        .nav-item { text-align: center; color: white; font-size: 10px; font-weight: bold; width: 20%; }
        .btn-center { position: fixed; bottom: 25px; left: 50%; transform: translateX(-50%); width: 75px; height: 75px; background: radial-gradient(circle, #ffd700, #ff8c00); border-radius: 50%; border: 3px solid #111; color: black; font-weight: 900; display: flex; align-items: center; justify-content: center; z-index: 10000; }
    </style>
    <div class="btn-center">MASUK</div>
    <div class="nav">
        <div class="nav-item">🏠<br>HOME</div>
        <div class="nav-item">🎁<br>PROMO</div>
        <div style="width:20%"></div>
        <div class="nav-item">📲<br>APK</div>
        <div class="nav-item">💬<br>CHAT</div>
    </div>
    """, unsafe_allow_html=True)

else:
    # Tampilkan halaman game jika state bukan lobby
    tampilan_game()

