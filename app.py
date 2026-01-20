import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from PIL import Image, ImageOps
from fpdf import FPDF
from gtts import gTTS
from st_audiorec import st_audiorec
import io

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="J.O. De l'Avenir",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🏅"
)

# --- FUNCIONES BACKEND ---

def generate_excel():
    data = {
        'Équipe': ['Les Titans', 'Eco-Warriors', 'Cyber-Français', 'Green Team'],
        'Missions Complétées': [5, 4, 6, 3],
        'Score Global': [1200, 950, 1400, 800],
        'Statut Fair-Play': ['Signé', 'Signé', 'Signé', 'Non Signé']
    }
    df = pd.DataFrame(data)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Suivi_Classe')
    return buffer.getvalue()

def create_player_card(name, trait):
    pdf = FPDF()
    pdf.add_page()
    # Fondo Blanco
    pdf.set_fill_color(255, 255, 255)
    pdf.rect(0, 0, 210, 297, 'F')
    # Borde Azul Olímpico
    pdf.set_draw_color(0, 102, 204)
    pdf.set_line_width(3)
    pdf.rect(20, 20, 170, 257)
    
    # Título
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(0, 0, 0)
    pdf.set_xy(0, 40)
    pdf.cell(210, 15, "J.O. DE L'AVENIR", 0, 1, 'C')
    
    # Nombre
    pdf.set_font("Arial", 'B', 40)
    pdf.set_text_color(220, 0, 0) # Rojo
    pdf.cell(210, 25, name.upper(), 0, 1, 'C')
    
    # Trait
    pdf.set_font("Arial", 'I', 18)
    pdf.set_text_color(0, 153, 51) # Verde
    pdf.cell(210, 10, f"Atout: {trait}", 0, 1, 'C')
    
    return pdf.output(dest='S').encode('latin-1')

# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>🏅</h1>", unsafe_allow_html=True)
    st.title("Boîte à Outils")
    
    with st.expander("🗣️ Lecteur (TTS)"):
        text_to_speak = st.text_input("Texte en français:", "Allez les bleus!")
        if st.button("Écouter 🔊"):
            try:
                tts = gTTS(text=text_to_speak, lang='fr')
                audio_bytes = io.BytesIO()
                tts.write_to_fp(audio_bytes)
                st.audio(audio_bytes, format='audio/mp3')
            except:
                st.error("Erreur audio.")

    with st.expander("🎙️ Micro (Oral)"):
        wav_audio_data = st_audiorec()
        if wav_audio_data is not None:
            st.audio(wav_audio_data, format='audio/wav')
            st.success("Enregistré!")

    st.divider()
    
    player_name = st.text_input("Ton Nom:", "Athlète")
    player_trait = st.selectbox("Ton Atout:", ["Vitesse", "Force", "Stratégie", "Créativité"])
    if st.button("📄 Ma Carte Officielle"):
        pdf_data = create_player_card(player_name, player_trait)
        st.download_button("📥 Télécharger PDF", pdf_data, file_name="carte_jo.pdf", mime="application/pdf")

    st.divider()
    
    password = st.text_input("Mot de passe Prof:", type="password")
    if password == "prof123":
        st.success("Mode Admin")
        st.download_button("📊 Excel Classe", data=generate_excel(), file_name="notes.xlsx")

# --- CSS ---
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding: 0 !important; margin: 0 !important;}
        iframe {height: 100vh !important;}
        [data-testid="stSidebar"] { background-color: #f8f9fa; border-right: 1px solid #ddd; }
        .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #0066cc; color: white; }
    </style>
""", unsafe_allow_html=True)

# --- FRONTEND HTML/JS ---
html_code = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>J.O. App</title>
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Montserrat:wght@800&family=Reenie+Beanie&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>

    <style>
        :root {
            /* PALETA VIVA OLÍMPICA */
            --primary: #0066CC;
            --accent: #FFB100;
            --success: #009933;
            --danger: #CC0000;
            --card-bg: rgba(255, 255, 255, 0.95);
            --text-main: #222222;
            --font-head: 'Montserrat', sans-serif;
            --font-body: 'Poppins', sans-serif;
            --font-hand: 'Reenie Beanie', cursive;
        }

        body {
            /* FONDO DEPORTIVO CON FILTRO CLARO */
            background-image: url('https://images.unsplash.com/photo-1533107862482-0e6974b06ec4?q=80&w=2574&auto=format&fit=crop');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: var(--text-main);
            font-family: var(--font-body);
            margin: 0; padding: 0;
            overflow-x: hidden;
            padding-bottom: 90px;
        }

        body::before {
            content: ''; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(255, 255, 255, 0.5); /* Filtro blanco para legibilidad */
            z-index: -1;
        }

        /* --- UI COMPONENTES --- */
        .solid-panel {
            background-color: var(--card-bg); border-radius: 15px; padding: 20px;
            margin-bottom: 15px; border: 1px solid rgba(0,0,0,0.1);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1); backdrop-filter: blur(10px);
        }

        /* --- MAPA DRAGGABLE --- */
        .map-container {
            position: relative; width: 100%; height: 450px; background: #eee;
            border-radius: 15px; overflow: hidden; border: 4px solid white;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .map-frame {
            width: 100%; height: 100%; border: 0; 
            pointer-events: none; /* El mapa no se mueve, los pines sí */
        }
        /* Capa transparente para soltar los pines */
        .map-overlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            z-index: 5;
        }
        .map-pin {
            position: absolute; width: 55px; height: 55px; background: var(--accent);
            border-radius: 50%; display: flex; align-items: center; justify-content: center;
            color: #000; font-weight: 900; cursor: grab; border: 3px solid #fff;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3); font-size: 1.8rem; z-index: 10;
            transform: translate(-50%, -50%);
        }
        .map-pin:active { cursor: grabbing; transform: translate(-50%, -50%) scale(1.1); }

        /* --- BOTONES --- */
        .btn-solid {
            background-color: var(--primary); color: white; border: none; border-radius: 10px;
            padding: 12px; width: 100%; font-weight: 800; text-transform: uppercase;
            font-family: var(--font-head); margin-top: 10px; cursor: pointer; transition: 0.2s;
            box-shadow: 0 4px 0 #004c99;
        }
        .btn-solid:active { transform: translateY(4px); box-shadow: none; }
        
        .btn-outline {
            background: white; border: 2px solid #ccc; color: #555; border-radius: 10px;
            padding: 10px; width: 100%; font-weight: 700; margin-top: 5px; cursor: pointer;
        }
        .btn-outline.active { border-color: var(--success); color: var(--success); background: #e6ffea; }

        .custom-file-input { width: 100%; padding: 10px; background: #222; color: white; border-radius: 8px; cursor: pointer; margin-bottom: 10px; }
        .solid-input, .solid-textarea {
            background-color: #f8f9fa; border: 2px solid #ddd; color: #333;
            padding: 12px; border-radius: 10px; width: 100%; font-size: 1rem;
            margin-bottom: 10px; font-family: var(--font-body); text-align: center;
        }
        .solid-textarea { text-align: left; }

        /* --- THERMOS & HOME --- */
        .thermo-container { background: white; border-radius: 15px; padding: 15px; margin-bottom: 20px; border: 1px solid #eee; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
        .progress-bar-bg { background: #e9ecef; height: 20px; border-radius: 10px; overflow: hidden; margin-top: 8px; }
        .fill-team { background: linear-gradient(90deg, #4D79FF, #00d2ff); height: 100%; width: 0%; transition: width 1s ease-out; }
        .fill-global { background: linear-gradient(90deg, #FFD93D, #FF6B6B); height: 100%; width: 35%; transition: width 1s ease-out; }
        
        .home-btn { background-color: white; border: none; border-radius: 18px; padding: 20px 10px; text-align: center; cursor: pointer; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 110px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); transition: transform 0.2s; }
        .home-btn:active { transform: scale(0.95); }
        .home-btn i { font-size: 2rem; margin-bottom: 8px; }
        .home-btn h3 { font-size: 0.8rem; margin: 0; font-weight: 800; color: #333; text-transform: uppercase; }

        /* --- OTHERS --- */
        .phase-card { cursor: pointer; border-left: 6px solid #ccc; background: white; padding: 15px; margin-bottom: 10px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        .phase-card.completed { border-left-color: var(--success); background: #f0fff4; }
        .phase-card h6 { color: #333; }
        .odd-badge { font-size: 0.65rem; background: #333; padding: 2px 6px; border-radius: 4px; color: var(--accent); font-weight: bold; margin-bottom: 4px; display: inline-block; }
        
        .dock-nav { position: fixed; bottom: 0; left: 0; width: 100%; background-color: white; border-top: 1px solid #eee; display: flex; justify-content: space-around; padding: 15px 0; z-index: 1000; box-shadow: 0 -5px 20px rgba(0,0,0,0.1); }
        .dock-item { font-size: 1.6rem; color: #aaa; cursor: pointer; transition: 0.2s; }
        .dock-item.active { color: var(--primary); transform: translateY(-5px); }
        
        .game-opt { background: #f0f0f0; padding: 15px; margin-bottom: 10px; border-radius: 8px; cursor: pointer; text-align: center; font-weight: bold; transition: 0.2s; }
        .game-opt:active { transform: scale(0.98); }
        .game-opt.correct { border-color: var(--success); background: #d4edda; }
        .game-opt.wrong { border-color: var(--danger); background: #f8d7da; }
        
        .journal-entry { background: white; border-left: 4px solid var(--accent); padding: 15px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        .journal-img { width: 100%; border-radius: 8px; margin-top: 10px; border: 1px solid #eee; }
        
        /* Modals & Utils */
        .view { display: none; padding: 20px; min-height: 100vh; }
        .active-view { display: block; animation: fadeIn 0.4s; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        
        .custom-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 2000; justify-content: center; align-items: center; }
        .custom-modal.show { display: flex; }
        .modal-content-solid { background: white; border-radius: 15px; padding: 30px; width: 90%; max-width: 400px; text-align: center; color: #333; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
        .mood-btn { font-size: 2.5rem; background: #fff; border: 2px solid #eee; border-radius: 12px; padding: 5px; cursor: pointer; flex: 1; text-align: center; margin: 0 3px; }
        .mood-btn.selected { background: #e6f0ff; border-color: var(--primary); transform: scale(1.1); }
        .vote-card { background: white; padding: 15px; border-radius: 8px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #eee; }
    </style>
</head>
<body>

    <section id="view-avatar" class="view active-view">
        <div class="text-center mt-4 mb-4"><h2 style="font-family: var(--font-head); font-weight: 900; color: #222;">CRÉEZ VOTRE ATHLÈTE</h2><p class="text-secondary small">CHOISISSEZ VOTRE CHAMPION</p></div>
        <div class="avatar-grid" id="sprite-container" style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px;"></div>
        <div class="solid-panel mt-4">
            <label class="small text-secondary mb-2 d-block text-start">NOM</label>
            <input type="text" id="player-name" class="solid-input" placeholder="Pseudo...">
            <label class="small text-secondary mb-2 d-block text-start mt-3">SUPER-POUVOIR</label>
            <div class="trait-selector" id="trait-container" style="display: flex; overflow-x: auto; padding-bottom: 10px;"></div>
            <input type="hidden" id="selected-trait">
        </div>
        <button onclick="app.saveProfile()" class="btn-solid mt-2">ENTRER DANS LE STADE <i class="fa-solid fa-person-running"></i></button>
    </section>

    <section id="view-home" class="view">
        <div class="d-flex align-items-center justify-content-between mb-4 mt-3">
            <div><h1 style="font-family: var(--font-head); font-weight: 900; font-size: 2rem; color: #222; line-height: 1;">J.O. AVENIR</h1><small class="text-secondary fw-bold">LYCÉE OLYMPIQUE</small></div>
            <div class="text-center" onclick="app.showView('view-avatar')" style="cursor:pointer"><div id="mini-avatar" style="font-size: 2rem; color: var(--primary); background: white; padding: 5px; border-radius: 50%; box-shadow: 0 2px 5px rgba(0,0,0,0.1);"></div></div>
        </div>
        <div class="thermo-container">
            <div class="d-flex justify-content-between align-items-end"><h6 class="mb-0 fw-bold text-dark"><i class="fa-solid fa-earth-americas text-primary me-2"></i> IMPACT GLOBAL</h6><small class="text-danger fw-bold">CLASSE</small></div>
            <div class="progress-bar-bg"><div class="fill-global"></div></div>
            <small class="text-secondary" style="font-size: 0.7rem;">Objectif commun (ODD 17)</small>
        </div>
        <div id="home-team-badge" class="badge bg-secondary mb-4 px-3 py-2 w-100" style="font-size: 0.9rem;"><i class="fa-solid fa-users-slash me-2"></i> Pas d'équipe</div>
        <div class="row g-3">
            <div class="col-6"><div class="home-btn" onclick="app.nav('dashboard', 'nav-dash')"><i class="fa-solid fa-list-check text-dark"></i><h3>PHASES</h3></div></div>
            <div class="col-6"><div class="home-btn" onclick="app.nav('journal', 'nav-journal')"><i class="fa-solid fa-book-open text-info"></i><h3>JOURNAL</h3></div></div>
            <div class="col-6"><div class="home-btn" onclick="app.nav('map', 'nav-games')"><i class="fa-solid fa-map-location-dot text-success"></i><h3>PLAN</h3></div></div>
            <div class="col-6"><div class="home-btn" onclick="app.nav('games', 'nav-games')"><i class="fa-solid fa-gamepad text-primary"></i><h3>ARCADE</h3></div></div>
            <div class="col-12"><div class="home-btn flex-row gap-3 py-3" style="min-height: auto;" onclick="app.nav('oscars', 'nav-oscars')"><i class="fa-solid fa-award text-accent mb-0"></i><h3 class="mb-0">VOTE & ÉVALUATION</h3></div></div>
        </div>
    </section>

    <section id="view-dashboard" class="view">
        <h4 class="fw-bold mb-3 text-dark">PROGRESSION</h4>
        <div class="thermo-container">
            <div class="d-flex justify-content-between align-items-end"><h6 class="mb-0 fw-bold text-dark"><i class="fa-solid fa-people-group text-primary me-2"></i> MON ÉQUIPE</h6><small id="team-percent-text" class="text-primary fw-bold">0%</small></div>
            <div class="progress-bar-bg"><div id="team-progress-bar" class="fill-team"></div></div>
        </div>
        <div id="missions-list"></div>
    </section>

    <section id="view-map" class="view">
        <h4 class="fw-bold mb-3 text-dark">PLAN DU CAMPUS</h4>
        <p class="text-secondary small">Glissez les icônes sur le collège !</p>
        
        <div class="map-container" id="map-area">
            <iframe class="map-frame" 
                src="https://maps.google.com/maps?q=38.975694,-3.944361&t=k&z=20&ie=UTF8&iwloc=&output=embed" 
                frameborder="0" scrolling="no" marginheight="0" marginwidth="0">
            </iframe>
            
            <div class="map-overlay" ondrop="app.drop(event)" ondragover="app.allowDrop(event)">
                <div id="pin1" class="map-pin" draggable="true" ondragstart="app.drag(event)" style="top: 20%; left: 20%;">🏋️</div>
                <div id="pin2" class="map-pin" draggable="true" ondragstart="app.drag(event)" style="top: 50%; left: 50%;">🏁</div>
                <div id="pin3" class="map-pin" draggable="true" ondragstart="app.drag(event)" style="top: 80%; left: 30%;">🍎</div>
            </div>
        </div>
        
        <div class="solid-panel mt-3">
            <h6 class="text-dark mb-2"><i class="fa-solid fa-hand-pointer text-primary"></i> Organisez les épreuves</h6>
            <ul class="list-unstyled text-secondary small mb-0">
                <li>🏋️ Zone Obstacles</li>
                <li>🍎 Ravitaillement</li>
                <li>🏁 Arrivée</li>
            </ul>
        </div>
        <button onclick="app.nav('home')" class="btn btn-link text-secondary w-100">Retour</button>
    </section>

    <section id="view-debate" class="view">
        <div class="text-center mt-4 mb-3"><h2 style="font-family: var(--font-head); color: #222;">ZONE DE DÉBAT</h2><p class="text-secondary small">PHASE 2: ÉQUIPES</p></div>
        <div class="radar-container mb-3" style="background: white; border: 1px solid #eee; border-radius: 15px; padding: 10px;"><canvas id="radarChart"></canvas></div>
        <div class="solid-panel">
            <h6 class="fw-bold mb-3 text-dark">L'ÉQUIPE</h6>
            <input type="text" id="team-name-create" class="solid-input mb-3" placeholder="NOM DE L'ÉQUIPE">
            <div class="p-3 border rounded mb-3">
                <label class="small text-secondary mb-2">VALIDATION</label>
                <button id="check-mixed" class="btn-outline" onclick="this.classList.toggle('active')">Équipe Mixte</button>
                <button id="check-skills" class="btn-outline" onclick="this.classList.toggle('active')">Compétences Variées</button>
                <button id="check-class" class="btn-outline" onclick="this.classList.toggle('active')">Validé par la classe</button>
            </div>
            <button onclick="app.finalizeTeam()" class="btn-solid">CONFIRMER</button>
        </div>
        <button onclick="app.nav('dashboard')" class="btn btn-link text-secondary w-100">Retour</button>
    </section>

    <section id="view-rules" class="view">
        <h4 class="fw-bold mb-3 text-dark">RÈGLEMENT</h4>
        <div class="parchment mb-4" style="background: #fffbe6; color: #333; padding: 20px; border-radius: 5px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); border: 2px solid #d4a017;">
            <h4 class="text-center">PACTE DE FAIR-PLAY</h4>
            <p class="small">Nous nous engageons à :</p>
            <ul class="small ps-3"><li>Respecter les adversaires.</li><li>Accepter la défaite.</li><li>Jouer sans tricher.</li></ul>
            <div class="text-center mt-4"><strong>Signature :</strong><div class="signature-pad" id="sign-pad" onclick="app.signPact(this)" style="width: 100%; height: 100px; border: 2px dashed #ccc; background: white; margin-top: 20px; display: flex; align-items: center; justify-content: center; font-family: 'Reenie Beanie', cursive; font-size: 2.5rem; color: #000080; cursor: pointer;">Cliquez pour signer</div></div>
        </div>
        <button onclick="app.nav('dashboard')" class="btn btn-link text-secondary w-100">Retour</button>
    </section>

    <section id="view-journal" class="view">
        <h4 class="fw-bold mb-3 text-dark">JOURNAL DE BORD</h4>
        <div class="solid-panel">
            <label class="small text-secondary mb-2">MOOD</label>
            <div class="d-flex justify-content-between mb-3">
                <div class="mood-btn" onclick="app.selectMood(this, '🤩')">🤩</div>
                <div class="mood-btn" onclick="app.selectMood(this, '🙂')">🙂</div>
                <div class="mood-btn" onclick="app.selectMood(this, '😐')">😐</div>
                <div class="mood-btn" onclick="app.selectMood(this, '🥱')">🥱</div>
            </div>
            <input type="hidden" id="selected-mood">
            
            <textarea id="journal-text" class="solid-textarea mt-2" rows="2" placeholder="Réflexion..."></textarea>
            
            <label class="small text-secondary mb-2 mt-2">PHOTO</label>
            <input type="file" id="journal-photo" class="custom-file-input" accept="image/*">
            
            <button onclick="app.saveJournal()" class="btn-solid">POSTER L'ENTRÉE</button>
        </div>
        <div id="journal-feed" class="mt-4"></div>
    </section>

    <section id="view-games" class="view">
        <h4 class="fw-bold mb-3 text-dark">SALLE D'ARCADE</h4>
        <div id="game-menu">
            <div class="row g-2">
                <div class="col-6"><div class="solid-panel p-3 mb-2 text-center" onclick="app.startGame('num')"><i class="fa-solid fa-calculator fa-2x text-primary mb-2"></i><br><h6 class="mb-0 text-dark fw-bold small">NOMBRES</h6></div></div>
                <div class="col-6"><div class="solid-panel p-3 mb-2 text-center" onclick="app.startGame('fut')"><i class="fa-solid fa-rocket fa-2x text-warning mb-2"></i><br><h6 class="mb-0 text-dark fw-bold small">FUTUR</h6></div></div>
                <div class="col-6"><div class="solid-panel p-3 mb-2 text-center" onclick="app.startGame('part')"><i class="fa-solid fa-pizza-slice fa-2x text-danger mb-2"></i><br><h6 class="mb-0 text-dark fw-bold small">PARTITIFS</h6></div></div>
                <div class="col-6"><div class="solid-panel p-3 mb-2 text-center" onclick="app.startGame('sport')"><i class="fa-solid fa-person-running fa-2x text-success mb-2"></i><br><h6 class="mb-0 text-dark fw-bold small">SPORT</h6></div></div>
                <div class="col-6"><div class="solid-panel p-3 mb-2 text-center" onclick="app.startGame('imp')"><i class="fa-solid fa-bullhorn fa-2x text-info mb-2"></i><br><h6 class="mb-0 text-dark fw-bold small">IMPÉRATIF</h6></div></div>
                <div class="col-6"><div class="solid-panel p-3 mb-2 text-center" onclick="app.startGame('odd')"><i class="fa-solid fa-earth-europe fa-2x text-primary mb-2"></i><br><h6 class="mb-0 text-dark fw-bold small">QUIZ ODD</h6></div></div>
            </div>
        </div>
        <div id="game-interface" style="display:none;">
            <div class="solid-panel"><h5 id="game-question" class="fw-bold mb-4 text-center text-dark">...</h5><div id="game-options"></div></div>
            <button onclick="app.exitGame()" class="btn btn-outline w-100">Quitter</button>
        </div>
    </section>

    <section id="view-oscars" class="view">
        <h2 class="text-center fw-bold mb-4 text-dark">VOTEZ !</h2>
        <div id="oscars-menu">
            <div class="solid-panel text-center mb-3" onclick="app.showNominees('ling')"><h6 class="mb-1 text-dark">Francophones d'Or</h6><small id="status-ling" class="text-secondary">Non voté</small></div>
            <div class="solid-panel text-center mb-3" onclick="app.showNominees('soc')"><h6 class="mb-1 text-dark">Esprit d'Équipe</h6><small id="status-soc" class="text-secondary">Non voté</small></div>
        </div>
        <div id="oscars-voting" style="display:none;">
            <h5 id="voting-cat-title" class="fw-bold mb-3 text-warning text-center">...</h5>
            <div id="nominees-list"></div>
            <button onclick="app.exitVoting()" class="btn btn-link text-secondary w-100 mt-3">Retour</button>
        </div>
    </section>

    <div id="app-dock" class="dock-nav" style="display:none;">
        <div id="nav-home" class="dock-item active" onclick="app.nav('home', this)"><i class="fa-solid fa-house"></i></div>
        <div id="nav-dash" class="dock-item" onclick="app.nav('dashboard', this)"><i class="fa-solid fa-list-check"></i></div>
        <div id="nav-games" class="dock-item" onclick="app.nav('games', this)"><i class="fa-solid fa-gamepad"></i></div>
        <div id="nav-journal" class="dock-item" onclick="app.nav('journal', this)"><i class="fa-solid fa-book-open"></i></div>
        <div id="nav-oscars" class="dock-item" onclick="app.nav('oscars', this)"><i class="fa-solid fa-award"></i></div>
    </div>

    <div id="customModal" class="custom-modal">
        <div class="modal-content-solid">
            <h4 id="modal-title" class="fw-bold mb-2">...</h4>
            <div class="badge bg-warning text-dark mb-2" id="modal-odd">ODD</div>
            <p id="modal-desc" class="text-secondary small mb-4">...</p>
            <input type="text" id="user-input" class="solid-input text-uppercase" placeholder="CODE PROFESSEUR">
            <button onclick="app.validate()" class="btn-solid mb-2">VALIDER</button>
            <button onclick="app.closeModal()" class="btn btn-link text-secondary text-decoration-none">Fermer</button>
            <div id="feedback-msg" class="mt-3 small fw-bold"></div>
        </div>
    </div>

    <script>
        const SPRITES = ["fa-dragon", "fa-ghost", "fa-robot", "fa-cat", "fa-bolt", "fa-fire", "fa-snowflake", "fa-leaf"];
        const TRAITS = ["Fort", "Rapide", "Stratège", "Sociable", "Créatif"];

        const DATA = {
            user: { sprite: "", name: "", trait: "" },
            teamName: "",
            missions: [
                { id: 1, type: "code", code: "MONNAIE", title: "L'Argent Solidaire", odd: "ODD 1 & 12", icon: "fa-coins", desc: "Sept-Oct: Création monnaie.", completed: false },
                { id: 2, type: "team", title: "Équipes Inclusives", odd: "ODD 5 & 10", icon: "fa-users", desc: "Nov-Dec: Création équipes.", completed: false },
                { id: 3, type: "code", code: "ECO", title: "Obstacles Avenir", odd: "ODD 13", icon: "fa-recycle", desc: "Jan-Fév: Design épreuves.", completed: false },
                { id: 4, type: "rules", title: "Règlement", odd: "ODD 16", icon: "fa-scale-balanced", desc: "Fév-Mars: Fair-play.", completed: false },
                { id: 5, type: "code", code: "FOOD", title: "Ravitaillement", odd: "ODD 3", icon: "fa-apple-whole", desc: "Avril-Mai: Snacks sains.", completed: false },
                { id: 6, type: "code", code: "MAP", title: "Plan Parcours", odd: "ODD 11", icon: "fa-map", desc: "Mai-Juin: Tracé plan.", completed: false }
            ],
            journal: [],
            votes: { ling: false, soc: false },
            nominees: ["Les Titans", "Eco-Warriors", "Cyber-Français"],
            currentId: null
        };

        // --- PREGUNTAS JUEGOS AMPLIADAS ---
        const QUIZ = {
            num: [{ q: "10 stylos = 20€. 1 stylo = ?", a: ["2€", "5€", "1€"], c: 0 }, { q: "90 + 9 = ?", a: ["99", "89", "19"], c: 0 }],
            fut: [{ q: "Demain je ___ (manger)", a: ["mangerai", "mangerais", "mange"], c: 0 }, { q: "Nous ___ (finir)", a: ["finirons", "finissons", "finiront"], c: 0 }],
            part: [{ q: "Je veux ___ eau", a: ["de l'", "du", "de la"], c: 0 }, { q: "Il mange ___ pain", a: ["du", "de la", "des"], c: 0 }],
            sport: [{ q: "Le sport dans l'eau ?", a: ["Natation", "Judo", "Tennis"], c: 0 }, { q: "Pour courir il faut des...", a: ["Baskets", "Gants", "Lunettes"], c: 0 }],
            imp: [{ q: "(Courir) ___ vite !", a: ["Cours", "Coures", "Courir"], c: 0 }, { q: "(Arrêter) ___ de parler !", a: ["Arrêtez", "Arrêter", "Arrêtes"], c: 0 }],
            odd: [{ q: "ODD 13 c'est pour...", a: ["Le Climat", "La Faim", "L'Eau"], c: 0 }, { q: "ODD 5 c'est...", a: ["Égalité", "Santé", "Villes"], c: 0 }]
        };
        
        let currentQuiz = [], qIndex = 0, score = 0;
        let chart = null, radarChart = null;

        const app = {
            init: () => {
                const grid = document.getElementById('sprite-container');
                SPRITES.forEach(icon => {
                    const div = document.createElement('div'); div.className = "avatar-item"; div.innerHTML = `<i class="fa-solid ${icon} fa-2x"></i>`;
                    div.onclick = () => { document.querySelectorAll('.avatar-item').forEach(el => el.classList.remove('selected')); div.classList.add('selected'); DATA.user.sprite = icon; };
                    grid.appendChild(div);
                });
                const tCont = document.getElementById('trait-container');
                TRAITS.forEach(t => {
                    const span = document.createElement('span'); span.className = "trait-tag"; span.innerText = t;
                    span.onclick = () => { document.querySelectorAll('.trait-tag').forEach(el => el.classList.remove('selected')); span.classList.add('selected'); DATA.user.trait = t; document.getElementById('selected-trait').value = t; };
                    tCont.appendChild(span);
                });
            },

            saveProfile: () => {
                const name = document.getElementById('player-name').value;
                if(!DATA.user.sprite || !name || !DATA.user.trait) return alert("Complétez votre profil !");
                DATA.user.name = name;
                document.getElementById('mini-avatar').innerHTML = `<i class="fa-solid ${DATA.user.sprite}"></i>`;
                app.showView('view-home');
                document.getElementById('app-dock').style.display = 'flex';
            },

            nav: (viewName, el) => {
                document.querySelectorAll('.dock-item').forEach(i => i.classList.remove('active'));
                if(el) { if(typeof el === 'string') document.getElementById(el).classList.add('active'); else el.classList.add('active'); }
                app.showView('view-' + viewName);
                if(viewName === 'dashboard') { app.renderList(); setTimeout(app.updateThermo, 100); }
                if(viewName === 'journal') app.renderJournal();
            },

            showView: (id) => {
                document.querySelectorAll('.view').forEach(v => v.classList.remove('active-view'));
                document.getElementById(id).classList.add('active-view');
            },

            // --- DRAG & DROP ---
            allowDrop: (ev) => { ev.preventDefault(); },
            drag: (ev) => { ev.dataTransfer.setData("text", ev.target.id); },
            drop: (ev) => {
                ev.preventDefault();
                var data = ev.dataTransfer.getData("text");
                var el = document.getElementById(data);
                var rect = ev.currentTarget.getBoundingClientRect();
                var x = ev.clientX - rect.left;
                var y = ev.clientY - rect.top;
                el.style.left = ((x / rect.width) * 100) + "%";
                el.style.top = ((y / rect.height) * 100) + "%";
            },

            // --- FASES ---
            renderList: () => {
                const list = document.getElementById('missions-list'); list.innerHTML = "";
                DATA.missions.forEach(m => {
                    const status = m.completed ? 'completed' : '';
                    const locked = (!m.completed && m.id > 1 && !DATA.missions[m.id-2].completed) ? 'locked' : '';
                    const iconCheck = m.completed ? 'fa-check text-success' : (locked ? 'fa-lock text-secondary' : 'fa-play text-primary');
                    let action = `app.openModal(${m.id})`;
                    if (m.id === 2 && !locked) action = `app.goToDebate()`;
                    if (m.id === 4 && !locked) action = `app.nav('rules')`;
                    list.innerHTML += `<div class="solid-panel phase-card d-flex align-items-center ${status} ${locked}" onclick="${action}"><div class="me-3 text-center" style="width: 40px;"><i class="fa-solid ${m.icon} fa-xl text-secondary"></i></div><div class="flex-grow-1"><span class="odd-badge">${m.odd}</span><h6 class="mb-0 fw-bold text-dark">${m.title}</h6></div><i class="fa-solid ${iconCheck}"></i></div>`;
                });
            },

            openModal: (id) => {
                DATA.currentId = id; const m = DATA.missions.find(x => x.id === id); if(m.completed) return;
                document.getElementById('modal-title').innerText = m.title; document.getElementById('modal-desc').innerText = m.desc; document.getElementById('modal-odd').innerText = m.odd;
                document.getElementById('user-input').value = ""; document.getElementById('feedback-msg').innerText = ""; document.getElementById('customModal').classList.add('show');
            },
            closeModal: () => document.getElementById('customModal').classList.remove('show'),
            validate: () => {
                const inp = document.getElementById('user-input').value.trim().toUpperCase();
                const m = DATA.missions.find(x => x.id === DATA.currentId);
                if(inp === m.code) {
                    m.completed = true; document.getElementById('feedback-msg').innerText = "Validé !"; document.getElementById('feedback-msg').style.color = "#28a745"; confetti();
                    setTimeout(() => { app.closeModal(); app.renderList(); app.updateThermo(); }, 1000);
                } else { document.getElementById('feedback-msg').innerText = "Incorrect"; document.getElementById('feedback-msg').style.color = "#dc3545"; }
            },

            goToDebate: () => { if(DATA.missions[1].completed) return; app.showView('view-debate'); setTimeout(app.initRadar, 200); },
            initRadar: () => {
                if(radarChart) radarChart.destroy();
                const ctx = document.getElementById('radarChart').getContext('2d');
                radarChart = new Chart(ctx, { type: 'radar', data: { labels: TRAITS, datasets: [{ label: 'Équilibre', data: [8,6,7,9,5], backgroundColor: 'rgba(0, 102, 204, 0.4)', borderColor: '#0066cc', pointBackgroundColor: '#fff' }] }, options: { scales: { r: { grid: { color: '#ccc' }, angleLines: { color: '#ccc' }, suggesteMin: 0, suggestedMax: 10, ticks: { display: false } } }, plugins: { legend: { display: false } } } });
            },
            finalizeTeam: () => {
                const team = document.getElementById('team-name-create').value; if(!team || !document.getElementById('check-class').classList.contains('active')) return alert("Nom + Validation requis!");
                DATA.teamName = team; DATA.missions[1].completed = true; DATA.nominees.push(team);
                document.getElementById('home-team-badge').innerText = "Équipe: " + team; document.getElementById('home-team-badge').classList.replace('bg-secondary', 'bg-success');
                confetti(); app.nav('dashboard');
            },
            signPact: (el) => { el.innerHTML = "<i>Signé : " + DATA.user.name + "</i>"; el.classList.add("signed"); el.style.fontFamily = "var(--font-hand)"; DATA.missions[3].completed = true; confetti(); setTimeout(() => { app.nav('dashboard'); }, 1500); },
            
            startGame: (t) => { currentQuiz = QUIZ[t]; qIndex=0; score=0; document.getElementById('game-menu').style.display='none'; document.getElementById('game-interface').style.display='block'; app.renderQuestion(); },
            renderQuestion: () => { if(qIndex>=currentQuiz.length){ alert("Fin! Score: "+score); app.exitGame(); return;} const q=currentQuiz[qIndex]; document.getElementById('game-question').innerText=q.q; const o=document.getElementById('game-options'); o.innerHTML=""; q.a.forEach((ans,i)=>{ o.innerHTML+=`<div class='game-opt' onclick='app.checkAnswer(${i})'>${ans}</div>`}); },
            checkAnswer: (i) => { if(i===currentQuiz[qIndex].c){score+=10; confetti();} setTimeout(()=>{qIndex++; app.renderQuestion()},500); },
            exitGame: () => { document.getElementById('game-interface').style.display='none'; document.getElementById('game-menu').style.display='block'; },
            
            selectMood: (e,m) => { document.querySelectorAll('.mood-btn').forEach(b=>b.classList.remove('selected')); e.classList.add('selected'); document.getElementById('selected-mood').value=m; },
            saveJournal: () => { 
                const m=document.getElementById('selected-mood').value, t=document.getElementById('journal-text').value, f=document.getElementById('journal-photo'); 
                if(!m||!t) return alert("Remplissez !"); 
                const e={d:new Date().toLocaleDateString(), m, t, i:null}; 
                if(f.files && f.files[0]){ 
                    const r=new FileReader(); 
                    r.onload=(ev)=>{e.i=ev.target.result; DATA.journal.unshift(e); app.renderJournal();}; 
                    r.readAsDataURL(f.files[0]); 
                } else { DATA.journal.unshift(e); app.renderJournal(); } 
                document.getElementById('journal-text').value=""; confetti(); 
            },
            renderJournal: () => { const c=document.getElementById('journal-feed'); c.innerHTML=""; DATA.journal.forEach(e=>{ c.innerHTML+=`<div class='journal-entry'><div class='d-flex justify-content-between'><span>${e.d}</span><span>${e.m}</span></div><p class='text-dark'>${e.t}</p>${e.i?`<img src='${e.i}' class='journal-img'>`:''}</div>`}); },

            showNominees: (c) => { if(DATA.votes[c]) return alert("Déjà voté!"); document.getElementById('oscars-menu').style.display='none'; document.getElementById('oscars-voting').style.display='block'; const l=document.getElementById('nominees-list'); l.innerHTML=""; DATA.nominees.forEach(t=>{ if(t!==DATA.teamName) l.innerHTML+=`<div class='vote-card'><span class='text-dark fw-bold'>${t}</span><button class='btn btn-sm btn-outline-warning' onclick='app.submitVote("${c}","${t}")'>VOTER</button></div>` }); },
            submitVote: (c,t) => { if(confirm("Sûr?")){ DATA.votes[c]=true; app.exitVoting(); confetti(); } },
            exitVoting: () => { document.getElementById('oscars-voting').style.display='none'; document.getElementById('oscars-menu').style.display='block'; },

            updateThermo: () => {
                const c = DATA.missions.filter(m => m.completed).length; const t = DATA.missions.length; const pct = Math.round((c/t)*100);
                document.getElementById('team-progress-bar').style.width = pct + "%"; document.getElementById('team-percent-text').innerText = pct + "%";
            }
        };
        app.init();
    </script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=True)
