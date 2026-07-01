import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from fpdf import FPDF
from gtts import gTTS
from st_audiorec import st_audiorec
import io
import qrcode
import tempfile
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="J.O. De l'Avenir",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🏅"
)

# --- SISTEMA MULTI-IDIOMA ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'Français'
if 'chapter' not in st.session_state:
    st.session_state.chapter = 1

translations = {
    'Français': {
        'tools': "Boîte à Outils", 'tts': "🗣️ Lecteur (TTS)", 'tts_help': "Écrivez pour écouter.", 
        'listen': "Écouter 🔊", 'mic': "🎙️ Micro (Oral)", 'mic_help': "Enregistrez-vous.",
        'card': "🎒 Carte Élève", 'name': "Ton Nom:", 'trait': "Ton Atout:", 
        'traits': ["Vitesse", "Force", "Stratégie", "Créativité"], 'download_pdf': "📄 Ma Carte (+ QR)",
        'admin': "🔐 Zone Professeur", 'pass': "Mot de passe Prof:",
        'chap_control': "Contrôle de l'Histoire", 'chap': "Chapitre:", 
        'data_link': "Lien Base de Données:", 'reset': "🗑️ Effacer (Test)",
        'chap_titles': {1: "Chapitre 1: L'Appel", 2: "Chapitre 2: L'Équipe", 3: "Chapitre 3: L'Action", 4: "Chapitre 4: Le Défi", 5: "Chapitre 5: La Gloire"}
    },
    'Español': {
        'tools': "Herramientas", 'tts': "🗣️ Lector (TTS)", 'tts_help': "Escribe para escuchar.", 
        'listen': "Escuchar 🔊", 'mic': "🎙️ Micrófono", 'mic_help': "Grábate.",
        'card': "🎒 Carnet Alumno", 'name': "Tu Nombre:", 'trait': "Tu Habilidad:", 
        'traits': ["Velocidad", "Fuerza", "Estrategia", "Creatividad"], 'download_pdf': "📄 Mi Carnet (+ QR)",
        'admin': "🔐 Zona Profesor", 'pass': "Contraseña:",
        'chap_control': "Control Historia", 'chap': "Capítulo:", 
        'data_link': "Enlace Base de Datos:", 'reset': "🗑️ Borrar (Test)",
        'chap_titles': {1: "Cap. 1: La Llamada", 2: "Cap. 2: El Equipo", 3: "Cap. 3: La Acción", 4: "Cap. 4: El Reto", 5: "Cap. 5: La Gloria"}
    },
    'English': {
        'tools': "Toolkit", 'tts': "🗣️ Text Reader", 'tts_help': "Type to listen.", 
        'listen': "Listen 🔊", 'mic': "🎙️ Microphone", 'mic_help': "Record.",
        'card': "🎒 Student ID", 'name': "Name:", 'trait': "Skill:", 
        'traits': ["Speed", "Strength", "Strategy", "Creativity"], 'download_pdf': "📄 Download ID (+ QR)",
        'admin': "🔐 Teacher Zone", 'pass': "Password:",
        'chap_control': "Story Control", 'chap': "Chapter:", 
        'data_link': "Database Link:", 'reset': "🗑️ Delete (Test)",
        'chap_titles': {1: "Chapter 1: The Call", 2: "Chapter 2: The Team", 3: "Chapter 3: The Action", 4: "Chapter 4: Challenge", 5: "Chapter 5: Glory"}
    }
}
t = translations[st.session_state.lang]

def get_tts_lang(lang_choice):
    if lang_choice == 'Français': return 'fr'
    elif lang_choice == 'Español': return 'es'
    else: return 'en'

# --- FUNCIONES BACKEND ---
def get_mock_data():
    return pd.DataFrame({
        'Équipe': ['Les Titans', 'Eco-Warriors', 'Cyber-Français', 'Green Team'],
        'Missions Validées': [5, 4, 6, 3],
        'XP Moyen': [850, 620, 1100, 450]
    })

def generate_excel(df):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Suivi')
    return buffer.getvalue()

def create_player_card(name, trait):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(250, 250, 250)
    pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_draw_color(0, 102, 204)
    pdf.set_line_width(4)
    pdf.rect(15, 15, 180, 267)
    pdf.set_font("Arial", 'B', 28)
    pdf.set_text_color(0, 51, 153)
    pdf.set_xy(0, 40)
    pdf.cell(210, 15, "ACCRÉDITATION OFFICIELLE", 0, 1, 'C')
    pdf.set_font("Arial", 'B', 45)
    pdf.set_text_color(220, 20, 60)
    pdf.cell(210, 30, name.upper(), 0, 1, 'C')
    pdf.set_font("Arial", 'I', 20)
    pdf.set_text_color(0, 153, 51)
    pdf.cell(210, 15, f"Spécialité : {trait}", 0, 1, 'C')
    
    qr = qrcode.make(f"Athlete: {name} | Spécialité: {trait} | ODD: 2030")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        qr.save(tmpfile.name)
        pdf.image(tmpfile.name, x=75, y=120, w=60)
    os.remove(tmpfile.name)
    return pdf.output(dest='S').encode('latin-1')

# --- BARRA LATERAL ---
with st.sidebar:
    st.selectbox("🌐 Langue / Idioma", ["Français", "Español", "English"], key='lang')
    t = translations[st.session_state.lang] 
    
    st.title(t['tools'])
    
    with st.expander(t['tts']):
        text_to_speak = st.text_input("", "Allez!")
        if st.button(t['listen']):
            try:
                tts = gTTS(text=text_to_speak, lang=get_tts_lang(st.session_state.lang))
                audio_bytes = io.BytesIO()
                tts.write_to_fp(audio_bytes)
                st.audio(audio_bytes, format='audio/mp3')
            except:
                pass

    with st.expander(t['mic']):
        wav_audio_data = st_audiorec()
        if wav_audio_data is not None:
            st.audio(wav_audio_data, format='audio/wav')

    st.divider()
    
    st.markdown(f"### {t['card']}")
    player_name = st.text_input(t['name'], "Athlète")
    player_trait = st.selectbox(t['trait'], t['traits'])
    if st.button(t['download_pdf']):
        pdf_data = create_player_card(player_name, player_trait)
        st.download_button("📥 PDF", pdf_data, file_name="carte.pdf", mime="application/pdf")

    st.divider()
    
    st.markdown(f"### {t['admin']}")
    password = st.text_input(t['pass'], type="password")
    if password == "prof123":
        st.success("Admin OK")
        st.markdown(f"**{t['chap_control']}**")
        col1, col2, col3 = st.columns([1,2,1])
        if col1.button("⏪"): st.session_state.chapter = max(1, st.session_state.chapter - 1)
        col2.markdown(f"<div style='text-align:center; font-weight:bold;'>{t['chap']} {st.session_state.chapter}</div>", unsafe_allow_html=True)
        if col3.button("⏩"): st.session_state.chapter = min(5, st.session_state.chapter + 1)
        
        st.text_input(t['data_link'], "https://docs.google.com/forms/...")
        if st.button(t['reset']):
            st.warning("Données effacées!")
        
        st.download_button("📥 Rapport Excel", data=generate_excel(get_mock_data()), file_name="rapport.xlsx")

# --- CSS BASE ---
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
        .block-container {padding: 0 !important; margin: 0 !important;}
        iframe {height: 100vh !important;}
        [data-testid="stSidebar"] { background-color: #f8f9fa; border-right: 1px solid #ddd; }
        .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #0066cc; color: white; }
    </style>
""", unsafe_allow_html=True)

dynamic_title = t['chap_titles'][st.session_state.chapter]

# --- FRONTEND HTML/JS ---
html_code = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>J.O. App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Montserrat:wght@800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>

    <style>
        :root {{ --primary: #0066CC; --accent: #FFB100; --success: #009933; --danger: #CC0000; --card-bg: rgba(255, 255, 255, 0.95); --text-main: #222222; --font-head: 'Montserrat', sans-serif; --font-body: 'Poppins', sans-serif; }}
        body {{ background-image: url('https://images.unsplash.com/photo-1533107862482-0e6974b06ec4?q=80&w=2574&auto=format&fit=crop'); background-size: cover; background-position: center; background-attachment: fixed; color: var(--text-main); font-family: var(--font-body); margin: 0; padding: 0; overflow-x: hidden; padding-bottom: 90px; }}
        body::before {{ content: ''; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(255, 255, 255, 0.5); z-index: -1; }}

        /* HUD MAPA (ROTADO 90 GRADOS) */
        .map-container {{ position: relative; width: 100%; height: 650px; background: #eee; border-radius: 15px; overflow: hidden; border: 4px solid white; box-shadow: 0 5px 25px rgba(0,0,0,0.3); display: flex; justify-content: center; align-items: center; }}
        .map-frame {{ width: 150%; height: 150%; border: 0; pointer-events: none; transform: rotate(90deg); flex-shrink: 0; filter: contrast(1.1) saturate(1.1); }}
        .map-overlay {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 5; }}
        .map-pin {{ position: absolute; width: 55px; height: 55px; background: var(--accent); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #000; font-weight: 900; cursor: grab; border: 3px solid #fff; box-shadow: 0 6px 12px rgba(0,0,0,0.5); font-size: 1.8rem; z-index: 10; transform: translate(-50%, -50%); transition: transform 0.1s; }}
        .map-pin:active {{ cursor: grabbing; transform: translate(-50%, -50%) scale(1.1); }}
        .pin-pulse {{ animation: gps-pulse 2s infinite; }}
        @keyframes gps-pulse {{ 0% {{ box-shadow: 0 0 0 0 rgba(255, 177, 0, 0.7); }} 70% {{ box-shadow: 0 0 0 20px rgba(255, 177, 0, 0); }} 100% {{ box-shadow: 0 0 0 0 rgba(255, 177, 0, 0); }} }}
        .map-hud {{ position: absolute; bottom: 15px; left: 15px; right: 15px; background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(10px); border-radius: 12px; padding: 15px; z-index: 20; border: 1px solid rgba(255,255,255,0.5); box-shadow: 0 10px 30px rgba(0,0,0,0.2); pointer-events: none; }}

        /* UI Common */
        .solid-panel {{ background-color: var(--card-bg); border-radius: 15px; padding: 20px; margin-bottom: 15px; border: 1px solid rgba(0,0,0,0.1); box-shadow: 0 4px 15px rgba(0,0,0,0.1); backdrop-filter: blur(10px); }}
        .btn-solid {{ background-color: var(--primary); color: white; border: none; border-radius: 10px; padding: 12px; width: 100%; font-weight: 800; text-transform: uppercase; font-family: var(--font-head); margin-top: 10px; cursor: pointer; transition: 0.2s; box-shadow: 0 4px 0 #004c99; }}
        .btn-solid:active {{ transform: translateY(4px); box-shadow: none; }}
        .solid-input {{ background-color: #f8f9fa; border: 2px solid #ddd; color: #333; padding: 12px; border-radius: 10px; width: 100%; font-size: 1rem; margin-bottom: 10px; font-family: var(--font-body); text-align: center; }}
        
        .avatar-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 20px; }}
        .avatar-item {{ background: white; border: 2px solid #ccc; border-radius: 10px; padding: 15px; text-align: center; cursor: pointer; transition: transform 0.1s; }}
        .avatar-item.selected {{ background: #e6f0ff; border-color: var(--primary); border-width: 4px; box-shadow: 0 0 10px rgba(0,102,204,0.3); }}
        .trait-selector {{ display: flex; overflow-x: auto; padding-bottom: 10px; gap: 8px; }}
        .trait-tag {{ background: white; border: 2px solid #ccc; color: #333; padding: 8px 15px; border-radius: 20px; white-space: nowrap; cursor: pointer; font-size: 0.9rem; }}
        .trait-tag.selected {{ background: var(--accent); color: black; font-weight: 800; border-color: #e6a000; transform: scale(1.05); }}

        .home-btn {{ background-color: white; border: none; border-radius: 18px; padding: 20px 10px; text-align: center; cursor: pointer; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 110px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); transition: transform 0.2s; }}
        .dock-nav {{ position: fixed; bottom: 0; left: 0; width: 100%; background-color: white; border-top: 1px solid #eee; display: flex; justify-content: space-around; padding: 15px 0; z-index: 1000; box-shadow: 0 -5px 20px rgba(0,0,0,0.1); }}
        .dock-item {{ font-size: 1.6rem; color: #aaa; cursor: pointer; transition: 0.2s; }}
        .dock-item.active {{ color: var(--primary); transform: translateY(-5px); }}
        .view {{ display: none; padding: 20px; min-height: 100vh; }}
        .active-view {{ display: block; animation: fadeIn 0.4s; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        
        .thermo-container {{ background: white; border-radius: 15px; padding: 15px; margin-bottom: 20px; border: 1px solid #eee; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }}
        .progress-bar-bg {{ background: #e9ecef; height: 20px; border-radius: 10px; overflow: hidden; margin-top: 8px; }}
        .fill-team {{ background: linear-gradient(90deg, #4D79FF, #00d2ff); height: 100%; width: 0%; transition: width 1s ease-out; }}
        .fill-global {{ background: linear-gradient(90deg, #FFD93D, #FF6B6B); height: 100%; width: 0%; transition: width 1s ease-out; }}
        
        .game-opt {{ background: #f0f0f0; padding: 15px; margin-bottom: 10px; border-radius: 8px; cursor: pointer; text-align: center; font-weight: bold; transition: 0.2s; }}
        .xp-badge {{ background: var(--accent); color: #000; font-weight: 900; padding: 5px 15px; border-radius: 20px; font-size: 0.9rem; box-shadow: 0 2px 5px rgba(0,0,0,0.2); border: 2px solid #fff; display: inline-block;}}
        .chap-title {{ font-family: var(--font-head); font-weight: 900; font-size: 1.5rem; color: var(--primary); margin-top: 10px; text-transform: uppercase; }}
        
        .secret-box {{ border: 2px dashed #ccc; background: #fafafa; border-radius: 10px; padding: 15px; margin-top: 15px; text-align: center; }}
        
        /* MEDALLAS */
        .medal-box {{ display: flex; gap: 10px; margin-top: 10px; }}
        .medal {{ width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; background: #eee; color: #aaa; border: 2px solid #ccc; transition: 0.3s; }}
        .medal.unlocked.bronze {{ background: #cd7f32; color: white; border-color: #8c5622; box-shadow: 0 0 10px rgba(205,127,50,0.5); }}
        .medal.unlocked.silver {{ background: #c0c0c0; color: white; border-color: #888; box-shadow: 0 0 10px rgba(192,192,192,0.5); }}
        .medal.unlocked.gold {{ background: #ffd700; color: white; border-color: #b8860b; box-shadow: 0 0 15px rgba(255,215,0,0.8); }}

        /* ESTRELLA DORADA FINAL */
        #golden-star {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 4rem; text-shadow: 0 0 20px #FFD700; cursor: pointer; z-index: 100; display: none; animation: pulse-star 1.5s infinite; }}
        @keyframes pulse-star {{ 0% {{ transform: translate(-50%, -50%) scale(1); }} 50% {{ transform: translate(-50%, -50%) scale(1.3); }} 100% {{ transform: translate(-50%, -50%) scale(1); }} }}
        
        /* MODAL DE INSIGNIA LEGENDARIA */
        .custom-modal {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 2000; justify-content: center; align-items: center; }}
        .custom-modal.show {{ display: flex; }}
        .modal-content-solid {{ background: white; border-radius: 15px; padding: 30px; width: 90%; max-width: 400px; text-align: center; color: #333; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }}
    </style>
</head>
<body>

    <section id="view-avatar" class="view active-view">
        <div class="text-center mt-4 mb-4"><h2 style="font-family: var(--font-head); font-weight: 900; color: #222;">CRÉEZ VOTRE ATHLÈTE</h2><p class="text-secondary small">CHOISISSEZ VOTRE CHAMPION</p></div>
        <div class="avatar-grid" id="sprite-container"></div>
        <div class="solid-panel mt-4">
            <label class="small text-secondary mb-2 d-block text-start">NOM</label>
            <input type="text" id="player-name" class="solid-input" placeholder="Pseudo...">
            <label class="small text-secondary mb-2 d-block text-start mt-3">SUPER-POUVOIR</label>
            <div class="trait-selector" id="trait-container"></div>
            <input type="hidden" id="selected-trait">
        </div>
        <button onclick="app.saveProfile()" class="btn-solid mt-2">ENTRER DANS LE STADE <i class="fa-solid fa-person-running"></i></button>
    </section>

    <section id="view-home" class="view">
        <div class="d-flex align-items-center justify-content-between mb-2 mt-3">
            <div>
                <h1 style="font-family: var(--font-head); font-weight: 900; font-size: 2rem; color: #222; line-height: 1; margin:0;">J.O. AVENIR</h1>
                <div class="chap-title">{dynamic_title}</div>
                <div class="xp-badge mt-2"><i class="fa-solid fa-star"></i> <span id="xp-counter">0</span> XP</div>
                <div class="medal-box">
                    <div id="m-bronze" class="medal"><i class="fa-solid fa-medal"></i></div>
                    <div id="m-silver" class="medal"><i class="fa-solid fa-medal"></i></div>
                    <div id="m-gold" class="medal"><i class="fa-solid fa-trophy"></i></div>
                </div>
            </div>
            <div class="text-center" onclick="app.nav('avatar')" style="cursor:pointer"><div id="mini-avatar" style="font-size: 2.2rem; color: var(--primary); background: white; padding: 15px; border-radius: 50%; box-shadow: 0 2px 5px rgba(0,0,0,0.1);"><i class="fa-solid fa-user"></i></div></div>
        </div>
        
        <div class="thermo-container mt-4">
            <div class="d-flex justify-content-between align-items-end"><h6 class="mb-0 fw-bold text-dark"><i class="fa-solid fa-earth-americas text-primary me-2"></i> IMPACT GLOBAL</h6><small class="text-danger fw-bold">CLASSE</small></div>
            <div class="progress-bar-bg"><div class="fill-global"></div></div>
            <small class="text-secondary" style="font-size: 0.7rem;">Objectif commun (ODD 17)</small>
        </div>

        <div class="row g-3">
            <div class="col-6"><div class="home-btn" onclick="app.nav('dashboard', 'nav-dash')"><i class="fa-solid fa-list-check text-dark mb-2"></i><h3 class="mb-0">MISSIONS</h3></div></div>
            <div class="col-6"><div class="home-btn" onclick="app.nav('map', 'nav-map')"><i class="fa-solid fa-map-location-dot text-success mb-2"></i><h3 class="mb-0">PLAN</h3></div></div>
            <div class="col-12"><div class="home-btn flex-row gap-3 py-3" style="min-height: auto;" onclick="app.nav('games', 'nav-games')"><i class="fa-solid fa-gamepad text-primary mb-0"></i><h3 class="mb-0">ARCADE / TESTS</h3></div></div>
        </div>
    </section>

    <!-- MISSIONS & ZONA SECRETA -->
    <section id="view-dashboard" class="view">
        <h4 class="fw-bold mb-3 text-dark">PROGRESSION</h4>
        <div id="missions-list"></div>
        
        <!-- ZONA SECRETA PARA CÓDIGOS -->
        <div class="secret-box">
            <h6 class="fw-bold text-dark"><i class="fa-solid fa-user-secret text-danger"></i> CODES SECRETS</h6>
            <p class="small text-secondary mb-2">As-tu un code caché ? Remplissez pour obtenir de l'XP !</p>
            <div class="d-flex gap-2">
                <input type="text" id="secret-code-input" class="solid-input mb-0" placeholder="CODE...">
                <button class="btn btn-dark" style="border-radius: 8px; font-weight:bold;" onclick="app.checkSecretCode()">GO</button>
            </div>
            <div id="secret-msg" class="small mt-2 fw-bold"></div>
        </div>
        <button onclick="app.nav('home')" class="btn btn-outline text-secondary w-100 mt-3">Retour</button>
    </section>

    <!-- MAPA CON HUEVO DE PASCUA -->
    <section id="view-map" class="view">
        <h4 class="fw-bold mb-3 text-dark">PLAN DU CAMPUS</h4>
        <p class="text-secondary small">Glissez les icônes sur le collège !</p>
        <div class="map-container" id="map-area">
            <iframe class="map-frame" src="https://maps.google.com/maps?q=38.9763185,-3.9443803&t=k&z=19&ie=UTF8&iwloc=&output=embed" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"></iframe>
            <div class="map-overlay" ondrop="app.drop(event)" ondragover="app.allowDrop(event)">
                <div id="pin1" class="map-pin pin-pulse" draggable="true" ondragstart="app.drag(event)" style="top: 10%; left: 10%; background:#FFD93D;">🚀</div>
                <div id="pin2" class="map-pin" draggable="true" ondragstart="app.drag(event)" style="top: 10%; left: 30%; background:#FF6B6B;">🏁</div>
                <div id="pin3" class="map-pin" draggable="true" ondragstart="app.drag(event)" style="top: 10%; left: 50%; background:#4D79FF;">🍎</div>
                <div id="pin4" class="map-pin" draggable="true" ondragstart="app.drag(event)" style="top: 10%; left: 70%; background:#28a745;">♻️</div>
                <div id="pin5" class="map-pin" draggable="true" ondragstart="app.drag(event)" style="top: 30%; left: 10%; background:#17a2b8;">💧</div>
                <div id="pin6" class="map-pin" draggable="true" ondragstart="app.drag(event)" style="top: 30%; left: 30%; background:#e83e8c;">🏥</div>
                <!-- ESTRELLA DORADA FINAL OCULTA -->
                <div id="golden-star" onclick="app.claimUltimateReward()">🌟</div>
            </div>
            <div class="map-hud">
                <h6 class="text-dark mb-2 fw-bold" style="font-size: 0.85rem;"><i class="fa-solid fa-hand-pointer text-primary"></i> LÉGENDE</h6>
                <div class="row g-1 small text-dark" style="font-size: 0.7rem; font-weight: bold;">
                    <div class="col-4">🚀 Départ</div> <div class="col-4">🏁 Arrivée</div> <div class="col-4">🍎 Ravito</div>
                    <div class="col-4">♻️ Recyclage</div> <div class="col-4">💧 Eau</div> <div class="col-4">🏥 Secours</div>
                </div>
            </div>
        </div>
        <button onclick="app.nav('home')" class="btn btn-outline text-secondary w-100 mt-3">Retour</button>
    </section>

    <!-- ARCADE / PRUEBAS INTERDISCIPLINARES -->
    <section id="view-games" class="view">
        <h4 class="fw-bold mb-3 text-dark">ARCADE INTERDISCIPLINAIRE</h4>
        <div id="game-menu">
            <div class="row g-2">
                <div class="col-6"><div class="solid-panel p-3 text-center" onclick="app.startGame('bio')"><i class="fa-solid fa-leaf fa-2x text-success mb-2"></i><br><h6 class="mb-0 text-dark fw-bold small">SVT (ODD 12/13)</h6></div></div>
                <div class="col-6"><div class="solid-panel p-3 text-center" onclick="app.startGame('geo')"><i class="fa-solid fa-globe fa-2x text-info mb-2"></i><br><h6 class="mb-0 text-dark fw-bold small">GÉO & HIST</h6></div></div>
                <div class="col-6"><div class="solid-panel p-3 text-center" onclick="app.startGame('math')"><i class="fa-solid fa-calculator fa-2x text-primary mb-2"></i><br><h6 class="mb-0 text-dark fw-bold small">MATHS</h6></div></div>
                <div class="col-6"><div class="solid-panel p-3 text-center" onclick="app.startGame('fra')"><i class="fa-solid fa-comment-dots fa-2x text-danger mb-2"></i><br><h6 class="mb-0 text-dark fw-bold small">FRANÇAIS</h6></div></div>
            </div>
        </div>
        <div id="game-interface" style="display:none;">
            <div class="solid-panel">
                <div class="d-flex justify-content-center align-items-center mb-3">
                    <h5 id="game-question" class="fw-bold mb-0 text-center text-dark">...</h5>
                    <button class="tts-btn" onclick="app.speakQuestion()" style="background:none; border:none; font-size:1.5rem; margin-left:10px;">🔊</button>
                </div>
                <div id="game-options"></div>
            </div>
            <button onclick="app.exitGame()" class="btn btn-outline w-100">Quitter</button>
        </div>
    </section>

    <!-- DOCK MENU -->
    <div id="app-dock" class="dock-nav" style="display:none;">
        <div id="nav-home" class="dock-item active" onclick="app.nav('home', this)"><i class="fa-solid fa-house"></i></div>
        <div id="nav-dash" class="dock-item" onclick="app.nav('dashboard', this)"><i class="fa-solid fa-list-check"></i></div>
        <div id="nav-map" class="dock-item" onclick="app.nav('map', this)"><i class="fa-solid fa-map"></i></div>
        <div id="nav-games" class="dock-item" onclick="app.nav('games', this)"><i class="fa-solid fa-gamepad"></i></div>
    </div>

    <!-- MODAL MISIONES NORMALES -->
    <div id="customModal" class="custom-modal">
        <div class="modal-content-solid">
            <h4 id="modal-title" class="fw-bold mb-2">...</h4>
            <div class="badge bg-warning text-dark mb-2" id="modal-odd">ODD</div>
            <p id="modal-desc" class="text-secondary small mb-4">...</p>
            <input type="text" id="user-input" class="solid-input text-uppercase" placeholder="CODE">
            <button onclick="app.validate()" class="btn-solid mb-2">VALIDER</button>
            <button onclick="app.closeModal()" class="btn btn-link text-secondary text-decoration-none">Fermer</button>
            <div id="feedback-msg" class="mt-3 small fw-bold"></div>
        </div>
    </div>
    
    <!-- MODAL RECOMPENSA FINAL OCULTA -->
    <div id="ultimateModal" class="custom-modal">
        <div class="modal-content-solid" style="border: 4px solid #FFD700; background: linear-gradient(135deg, #fff 0%, #fff8dc 100%);">
            <i class="fa-solid fa-crown fa-4x mb-3" style="color: #FFD700; text-shadow: 0 4px 10px rgba(255,215,0,0.5);"></i>
            <h2 class="fw-bold text-dark">LÉGENDE DÉBLOQUÉE</h2>
            <h4 class="fw-bold text-danger mb-3">🏅 ORGANISATEURS TOP 🏅</h4>
            <p class="text-secondary small mb-4">La classe a atteint 100% d'Impact Global ! Vous êtes officiellement les maîtres des Jeux de l'Avenir. Le comité vous accorde l'Insigne Ultime.</p>
            <button onclick="document.getElementById('ultimateModal').classList.remove('show')" class="btn-solid mb-2" style="background:#FFD700; color:#000; border:2px solid #b8860b;">INCROYABLE !</button>
        </div>
    </div>

    <script>
        const SPRITES = ["fa-dragon", "fa-ghost", "fa-robot", "fa-cat", "fa-bolt", "fa-fire", "fa-snowflake", "fa-leaf"];
        const TRAITS = ["Vitesse", "Force", "Stratégie", "Créativité"];

        // CÓDIGOS SECRETOS INDEPENDIENTES
        const SECRET_CODES = {{
            "PARIS2024": {{ xp: 100, msg: "Bonus Olympique ! (+100 XP)" }},
            "COUBERTIN": {{ xp: 50, msg: "Histoire trouvée ! (+50 XP)" }}
        }};

        let DATA = {{
            user: {{ sprite: "", name: "", trait: "", xp: 0, usedCodes: [] }},
            teamName: "",
            missions: [
                {{ id: 1, type: "code", code: "MONNAIE", title: "Conférence ODD", odd: "Tous les ODD", icon: "fa-coins", desc: "Création monnaie solidaire.", completed: false }},
                {{ id: 2, type: "code", code: "ECO", title: "Obstacles Avenir", odd: "ODD 13", icon: "fa-recycle", desc: "Design d'épreuves.", completed: false }},
                {{ id: 3, type: "code", code: "MAP", title: "Plan Parcours", odd: "ODD 11", icon: "fa-map", desc: "Tracé sur le campus.", completed: false }}
            ],
            currentId: null
        }};

        // PRUEBAS DE ARCADE POR ASIGNATURA (4º ESO)
        const QUIZ = {{
            bio: [
                {{ q: "Où jeter une bouteille en plastique ? (ODD 12)", a: ["Poubelle Jaune", "Poubelle Verte", "Poubelle Bleue"], c: 0 }}, 
                {{ q: "Quel gaz cause l'effet de serre ? (ODD 13)", a: ["Le CO2", "L'Oxygène", "L'Azote"], c: 0 }}
            ],
            geo: [
                {{ q: "Où sont nés les Jeux Olympiques ?", a: ["En Grèce", "En France", "En Italie"], c: 0 }},
                {{ q: "Combien d'anneaux sur le drapeau olympique ?", a: ["5", "6", "4"], c: 0 }}
            ],
            math: [
                {{ q: "Un athlète court 100m en 10s. Vitesse ?", a: ["10 m/s", "100 m/s", "1 m/s"], c: 0 }},
                {{ q: "Si un terrain fait 50m x 20m, quelle est l'aire ?", a: ["1000 m²", "100 m²", "500 m²"], c: 0 }}
            ],
            fra: [
                {{ q: "Il faut que nous _____ (participer).", a: ["participions", "participons", "participerons"], c: 0 }},
                {{ q: "Trouve le synonyme de 'Gagner'", a: ["Remporter", "Perdre", "Échouer"], c: 0 }}
            ]
        }};
        
        let currentQuiz = [], qIndex = 0, score = 0;

        const app = {{
            init: () => {{
                const savedData = localStorage.getItem("jo_avenir_data");
                if(savedData) DATA = JSON.parse(savedData);
                if(!DATA.user.usedCodes) DATA.user.usedCodes = [];

                const grid = document.getElementById('sprite-container');
                SPRITES.forEach(icon => {{
                    const div = document.createElement('div');
                    div.className = "avatar-item";
                    if(DATA.user.sprite === icon) div.classList.add('selected');
                    div.innerHTML = `<i class="fa-solid ${{icon}}"></i>`;
                    div.onclick = function() {{
                        document.querySelectorAll('.avatar-item').forEach(el => el.classList.remove('selected'));
                        this.classList.add('selected');
                        DATA.user.sprite = icon;
                    }};
                    grid.appendChild(div);
                }});

                const tCont = document.getElementById('trait-container');
                TRAITS.forEach(t => {{
                    const span = document.createElement('span');
                    span.className = "trait-tag";
                    if(DATA.user.trait === t) span.classList.add('selected');
                    span.innerText = t;
                    span.onclick = function() {{
                        document.querySelectorAll('.trait-tag').forEach(el => el.classList.remove('selected'));
                        this.classList.add('selected');
                        DATA.user.trait = t;
                    }};
                    tCont.appendChild(span);
                }});

                if(DATA.user.name !== "") {{
                    document.getElementById('player-name').value = DATA.user.name;
                    app.updateHeader();
                    app.showView('view-home');
                    document.getElementById('app-dock').style.display = 'flex';
                }}
            }},

            saveData: () => {{
                localStorage.setItem("jo_avenir_data", JSON.stringify(DATA));
                app.updateHeader();
            }},

            addXP: (amount) => {{
                DATA.user.xp = (DATA.user.xp || 0) + amount;
                app.saveData();
                confetti();
            }},

            updateHeader: () => {{
                const xp = DATA.user.xp || 0;
                document.getElementById('xp-counter').innerText = xp;
                if(DATA.user.sprite) document.getElementById('mini-avatar').innerHTML = `<i class="fa-solid ${{DATA.user.sprite}}"></i>`;
                
                if (xp >= 100) document.getElementById('m-bronze').classList.add('unlocked', 'bronze');
                if (xp >= 300) document.getElementById('m-silver').classList.add('unlocked', 'silver');
                if (xp >= 500) document.getElementById('m-gold').classList.add('unlocked', 'gold');

                // BARRA GLOBAL Y ESTRELLA MISTERIOSA
                const globalMax = 1000; 
                let globalPct = Math.min((xp / globalMax) * 100, 100);
                const globalBar = document.querySelector('.fill-global');
                if(globalBar) globalBar.style.width = globalPct + "%";

                if (globalPct >= 100) {{
                    document.getElementById('golden-star').style.display = 'block';
                }}
            }},

            checkSecretCode: () => {{
                const input = document.getElementById('secret-code-input').value.trim().toUpperCase();
                const msgBox = document.getElementById('secret-msg');
                
                if(DATA.user.usedCodes.includes(input)) {{
                    msgBox.innerText = "Code déjà utilisé !"; msgBox.style.color = "#dc3545"; return;
                }}
                if(SECRET_CODES[input]) {{
                    DATA.user.usedCodes.push(input);
                    app.addXP(SECRET_CODES[input].xp);
                    msgBox.innerText = SECRET_CODES[input].msg; msgBox.style.color = "#28a745";
                    document.getElementById('secret-code-input').value = "";
                }} else {{
                    msgBox.innerText = "Code invalide."; msgBox.style.color = "#dc3545";
                }}
            }},

            claimUltimateReward: () => {{
                confetti({{ particleCount: 300, spread: 160, origin: {{ y: 0.4 }} }});
                document.getElementById('golden-star').style.display = 'none'; 
                document.getElementById('ultimateModal').classList.add('show');
            }},

            saveProfile: () => {{
                const name = document.getElementById('player-name').value;
                if(!DATA.user.sprite || !name || !DATA.user.trait) return alert("Complétez votre profil !");
                DATA.user.name = name;
                if(DATA.user.xp === undefined) DATA.user.xp = 0;
                app.saveData();
                app.showView('view-home');
                document.getElementById('app-dock').style.display = 'flex';
            }},

            nav: (viewName, el) => {{
                document.querySelectorAll('.dock-item').forEach(i => i.classList.remove('active'));
                if(el) {{ if(typeof el === 'string') document.getElementById(el).classList.add('active'); else el.classList.add('active'); }}
                app.showView('view-' + viewName);
                if(viewName === 'dashboard') {{ app.renderList(); }}
            }},

            showView: (id) => {{
                document.querySelectorAll('.view').forEach(v => v.classList.remove('active-view'));
                document.getElementById(id).classList.add('active-view');
            }},

            allowDrop: (ev) => {{ ev.preventDefault(); }},
            drag: (ev) => {{ ev.dataTransfer.setData("text", ev.target.id); }},
            drop: (ev) => {{
                ev.preventDefault();
                var data = ev.dataTransfer.getData("text");
                var el = document.getElementById(data);
                var rect = ev.currentTarget.getBoundingClientRect();
                var x = ev.clientX - rect.left;
                var y = ev.clientY - rect.top;
                el.style.left = ((x / rect.width) * 100) + "%";
                el.style.top = ((y / rect.height) * 100) + "%";
            }},

            renderList: () => {{
                const list = document.getElementById('missions-list'); list.innerHTML = "";
                DATA.missions.forEach(m => {{
                    const status = m.completed ? 'completed' : '';
                    const iconCheck = m.completed ? 'fa-check text-success' : 'fa-play text-primary';
                    list.innerHTML += `<div class="solid-panel phase-card d-flex align-items-center ${{status}}" onclick="app.openModal(${{m.id}})"><div class="me-3 text-center" style="width: 40px;"><i class="fa-solid ${{m.icon}} fa-xl text-secondary"></i></div><div class="flex-grow-1"><span class="odd-badge">${{m.odd}}</span><h6 class="mb-0 fw-bold text-dark">${{m.title}}</h6></div><i class="fa-solid ${{iconCheck}}"></i></div>`;
                }});
            }},

            openModal: (id) => {{
                DATA.currentId = id; const m = DATA.missions.find(x => x.id === id); if(m.completed) return;
                document.getElementById('modal-title').innerText = m.title; document.getElementById('modal-desc').innerText = m.desc; document.getElementById('modal-odd').innerText = m.odd;
                document.getElementById('user-input').value = ""; document.getElementById('feedback-msg').innerText = ""; document.getElementById('customModal').classList.add('show');
            }},
            closeModal: () => document.getElementById('customModal').classList.remove('show'),
            validate: () => {{
                const inp = document.getElementById('user-input').value.trim().toUpperCase();
                const m = DATA.missions.find(x => x.id === DATA.currentId);
                if(inp === m.code) {{
                    m.completed = true; document.getElementById('feedback-msg').innerText = "Validé ! +100 XP"; document.getElementById('feedback-msg').style.color = "#28a745"; 
                    app.addXP(100);
                    setTimeout(() => {{ app.closeModal(); app.renderList(); }}, 1200);
                }} else {{ document.getElementById('feedback-msg').innerText = "Incorrect"; document.getElementById('feedback-msg').style.color = "#dc3545"; }}
            }},

            speakText: (text) => {{
                window.speechSynthesis.cancel();
                const msg = new SpeechSynthesisUtterance(); msg.text = text; msg.lang = 'fr-FR'; 
                window.speechSynthesis.speak(msg);
            }},
            speakQuestion: () => {{ app.speakText(document.getElementById('game-question').innerText); }},

            startGame: (t) => {{ currentQuiz = QUIZ[t]; qIndex=0; score=0; document.getElementById('game-menu').style.display='none'; document.getElementById('game-interface').style.display='block'; app.renderQuestion(); }},
            renderQuestion: () => {{ if(qIndex>=currentQuiz.length){{ alert("Fin! Score: "+score); app.addXP(score); app.exitGame(); return;}} const q=currentQuiz[qIndex]; document.getElementById('game-question').innerText=q.q; const o=document.getElementById('game-options'); o.innerHTML=""; q.a.forEach((ans,i)=>{{ o.innerHTML+=`<div class='game-opt' onclick='app.checkAnswer(${{i}})'>${{ans}}</div>`}}); }},
            checkAnswer: (i) => {{ app.speakText(currentQuiz[qIndex].a[i]); if(i===currentQuiz[qIndex].c){{score+=10; confetti();}} setTimeout(()=>{{qIndex++; app.renderQuestion()}}, 1200); }},
            exitGame: () => {{ document.getElementById('game-interface').style.display='none'; document.getElementById('game-menu').style.display='block'; }}
        }};
        
        app.init();
    </script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=True)
