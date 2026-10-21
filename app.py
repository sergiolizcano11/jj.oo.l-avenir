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
import json

# ==========================================================
# 1. CONFIGURACIÓN Y DICCIONARIOS
# ==========================================================
st.set_page_config(page_title="J.O. De l'Avenir", layout="wide", initial_sidebar_state="collapsed", page_icon="🏅")

if 'lang' not in st.session_state: st.session_state.lang = 'Français'
if 'chapter' not in st.session_state: st.session_state.chapter = 1

translations = {
    'Français': {
        'tools': "Boîte à Outils", 'tts': "🗣️ Lecteur (TTS)", 'listen': "Écouter 🔊", 'mic': "🎙️ Micro (Oral)",
        'card': "🎒 Carte Élève", 'name': "Ton Nom:", 'trait': "Ton Atout:", 
        'traits': ["Vitesse", "Force", "Stratégie", "Créativité", "Éloquence"], 'download_pdf': "📄 Ma Carte",
        'admin': "🔐 Zone Professeur", 'pass': "Mot de passe:", 'chap_control': "Contrôle Chapitres", 'chap': "Chapitre:",
        'chap_titles': {1: "Chap. 1: L'Appel", 2: "Chap. 2: L'Équipe", 3: "Chap. 3: L'Action", 4: "Chap. 4: Les Règles", 5: "Chap. 5: L'Énergie", 6: "Chap. 6: La Gloire"},
        'create_athlete': "CRÉEZ VOTRE ATHLÈTE", 'choose_champ': "CHOISISSEZ VOTRE CHAMPION",
        'name_label': "NOM", 'power_label': "SUPER-POUVOIR", 'enter_stadium': "ENTRER DANS LE STADE",
        'global_impact': "IMPACT GLOBAL", 'class': "CLASSE", 'obj_comm': "Objectif commun (ODD 17)",
        'missions_btn': "MISSIONS", 'map_btn': "PLAN", 'journal_btn': "JOURNAL", 'arcade_btn': "ARCADE", 'oscars_btn': "VOTE & ÉVALUATION",
        'progression': "ROAD TO PARIS", 'secret_codes_title': "CODES SECRETS", 'secret_codes_desc': "As-tu un code caché ? (ex: MATH-50)",
        'back': "Retour", 'campus_map': "PLAN DU CAMPUS", 'legend': "LÉGENDE", 'arcade_title': "ARCADE INTERDISCIPLINAIRE", 'quit': "Quitter",
        'locked_chap': "Chapitre Requis", 'validate': "VALIDER", 'close': "Fermer",
        'legend_unlocked': "LÉGENDE DÉBLOQUÉE", 'org_top': "🏅 ORGANISATEURS TOP 🏅",
        'win_msg': "La classe a atteint 100% d'Impact Global ! Vous êtes les maîtres des Jeux.",
        'amazing': "INCROYABLE !", 'journal_title': "JOURNAL DE BORD", 'mood': "HUMEUR", 'reflection': "Réflexion...", 'photo': "PHOTO", 'post': "POSTER L'ENTRÉE",
        'oscars_title': "CO-ÉVALUATION GYMKHANA", 'vote_btn': "VOTER", 'vote_thanks': "Vote enregistré ! +20 XP", 'already_voted': "Vous avez déjà voté !",
        'p_start': "Départ", 'p_end': "Arrivée", 'p_food': "Ravito", 'p_recyc': "Recyclage", 'p_water': "Eau", 'p_med': "Secours",
        'alert_profile': "Complétez votre profil !", 'code_used': "Code déjà utilisé !", 'code_invalid': "Code invalide.",
        'validated_xp': "Validé ! +100 XP", 'incorrect': "Incorrect", 'end_score': "Fin! Score: ",
        'm1_title': "Conférence ODD", 'm1_desc': "Création monnaie solidaire.", 'm2_title': "Équipes Inclusives", 'm2_desc': "Création des équipes.", 
        'm3_title': "Obstacles Avenir", 'm3_desc': "Design d'épreuves.", 'm4_title': "Règlement", 'm4_desc': "Pacte de Fair-play.", 
        'm5_title': "Ravitaillement", 'm5_desc': "Snacks sains.", 'm6_title': "Plan Parcours", 'm6_desc': "Tracé sur le campus."
    },
    'Español': {
        'tools': "Herramientas", 'tts': "🗣️ Lector (TTS)", 'listen': "Escuchar 🔊", 'mic': "🎙️ Micrófono",
        'card': "🎒 Carnet Alumno", 'name': "Tu Nombre:", 'trait': "Habilidad:", 
        'traits': ["Velocidad", "Fuerza", "Estrategia", "Creatividad", "Elocuencia"], 'download_pdf': "📄 Mi Carnet",
        'admin': "🔐 Zona Profesor", 'pass': "Contraseña:", 'chap_control': "Control Capítulos", 'chap': "Capítulo:",
        'chap_titles': {1: "Cap. 1: La Llamada", 2: "Cap. 2: El Equipo", 3: "Cap. 3: La Acción", 4: "Cap. 4: Las Reglas", 5: "Cap. 5: La Energía", 6: "Cap. 6: La Gloria"},
        'create_athlete': "CREA TU ATLETA", 'choose_champ': "ELIGE TU CAMPEÓN",
        'name_label': "NOMBRE", 'power_label': "SUPERPODER", 'enter_stadium': "ENTRAR AL ESTADIO",
        'global_impact': "IMPACTO GLOBAL", 'class': "CLASE", 'obj_comm': "Objetivo común (ODS 17)",
        'missions_btn': "MISIONES", 'map_btn': "MAPA", 'journal_btn': "DIARIO", 'arcade_btn': "ARCADE", 'oscars_btn': "EVALUACIÓN",
        'progression': "ROAD TO PARIS", 'secret_codes_title': "CÓDIGOS SECRETOS", 'secret_codes_desc': "¿Tienes un código oculto? (ej: MATH-50)",
        'back': "Volver", 'campus_map': "MAPA DEL CAMPUS", 'legend': "LEYENDA", 'arcade_title': "ARCADE INTERDISCIPLINAR", 'quit': "Salir",
        'locked_chap': "Capítulo Requerido", 'validate': "VALIDAR", 'close': "Cerrar",
        'legend_unlocked': "LEYENDA DESBLOQUEADA", 'org_top': "🏅 ORGANIZADORES TOP 🏅",
        'win_msg': "¡La clase ha alcanzado el 100% de Impacto Global! Sois los maestros de los Juegos.",
        'amazing': "¡INCREÍBLE!", 'journal_title': "DIARIO DE A BORDO", 'mood': "ESTADO DE ÁNIMO", 'reflection': "Reflexión...", 'photo': "FOTO", 'post': "PUBLICAR ENTRADA",
        'oscars_title': "COEVALUACIÓN GYMKHANA", 'vote_btn': "VOTAR", 'vote_thanks': "¡Voto registrado! +20 XP", 'already_voted': "¡Ya has votado!",
        'p_start': "Salida", 'p_end': "Meta", 'p_food': "Snacks", 'p_recyc': "Reciclaje", 'p_water': "Agua", 'p_med': "Botiquín",
        'alert_profile': "¡Completa tu perfil!", 'code_used': "¡Código ya usado!", 'code_invalid': "Código inválido.",
        'validated_xp': "¡Validado! +100 XP", 'incorrect': "Incorrecto", 'end_score': "¡Fin! Puntuación: ",
        'm1_title': "Conferencia ODS", 'm1_desc': "Creación moneda solidaria.", 'm2_title': "Equipos Inclusivos", 'm2_desc': "Formación de equipos.", 
        'm3_title': "Obstáculos Futuro", 'm3_desc': "Diseño de pruebas.", 'm4_title': "Reglamento", 'm4_desc': "Pacto Fair-play.", 
        'm5_title': "Avituallamiento", 'm5_desc': "Snacks saludables.", 'm6_title': "Plano Recorrido", 'm6_desc': "Trazado en campus."
    }
}
t = translations.get(st.session_state.lang, translations['Français'])
dynamic_title = t['chap_titles'][st.session_state.chapter]

def get_tts_lang(lang_choice):
    return 'es' if lang_choice == 'Español' else 'fr'

# ==========================================================
# 2. FIREBASE & BACKEND (MOCKS)
# ==========================================================
FIREBASE_CONFIG = """
  apiKey: "TU_API_KEY",
  authDomain: "tu-proyecto.firebaseapp.com",
  projectId: "tu-proyecto",
  storageBucket: "tu-proyecto.appspot.com",
  messagingSenderId: "TUS_SENDER_ID",
  appId: "TU_APP_ID"
"""

def get_mock_data():
    return pd.DataFrame({'Équipe': ['Les Titans', 'Eco-Warriors', 'Cyber-Français', 'Green Team'], 'Missions Validées': [5, 4, 6, 3], 'XP Moyen': [850, 620, 1100, 450]})

def generate_excel(df):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Suivi')
    return buffer.getvalue()

def create_player_card(name, trait, awards_json="[]"):
    try:
        awards = json.loads(awards_json)
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
        
        qr = qrcode.make(f"Athlete: {name} | Specialite: {trait} | ODD: 2030")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            qr.save(tmpfile.name)
            pdf.image(tmpfile.name, x=75, y=120, w=60)
        os.remove(tmpfile.name)
        return pdf.output(dest='S').encode('latin-1')
    except Exception as e:
        print(f"Error generando PDF: {e}")
        return None

# ==========================================================
# 3. INTERFAZ PROFESOR CON MANEJO DE ERRORES PYTHON
# ==========================================================
with st.sidebar:
    st.selectbox("🌐 Langue / Idioma", ["Français", "Español"], key='lang')
    t = translations.get(st.session_state.lang, translations['Français'])
    
    st.title(t['tools'])
    with st.expander(t['tts']):
        text_to_speak = st.text_input("", "Allez!")
        if st.button(t['listen']):
            # 🛡️ CAPTURA DE ERROR: API de Google TTS
            try:
                tts = gTTS(text=text_to_speak, lang=get_tts_lang(st.session_state.lang))
                audio_bytes = io.BytesIO()
                tts.write_to_fp(audio_bytes)
                st.audio(audio_bytes, format='audio/mp3')
            except Exception as e:
                st.error("⚠️ Erreur de connexion au serveur vocal (Vérifiez internet).")
                print(f"Error TTS: {e}")

    with st.expander(t['mic']):
        wav_audio_data = st_audiorec()
        if wav_audio_data is not None:
            st.audio(wav_audio_data, format='audio/wav')

    st.divider()
    st.markdown(f"### {t['card']}")
    player_name = st.text_input(t['name'], "Athlète")
    player_trait = st.selectbox(t['trait'], t['traits'])
    if st.button(t['download_pdf']):
        # 🛡️ CAPTURA DE ERROR: Generación de PDF
        try:
            pdf_data = create_player_card(player_name, player_trait)
            if pdf_data:
                st.download_button("📥 PDF", pdf_data, file_name="carte.pdf", mime="application/pdf")
                st.success("PDF Généré avec succès !")
            else:
                st.error("⚠️ Erreur lors de la création du PDF.")
        except Exception as e:
            st.error("⚠️ Une erreur inattendue est survenue.")
            print(f"Error GenPDF: {e}")

    st.divider()
    st.markdown(f"### {t['admin']}")
    password = st.text_input(t['pass'], type="password")
    if password == "prof123": 
        st.success("Admin OK")
        col1, col2, col3 = st.columns([1,2,1])
        if col1.button("⏪"): st.session_state.chapter = max(1, st.session_state.chapter - 1)
        col2.markdown(f"<div style='text-align:center; font-weight:bold;'>{t['chap']} {st.session_state.chapter}</div>", unsafe_allow_html=True)
        if col3.button("⏩"): st.session_state.chapter = min(6, st.session_state.chapter + 1)
        st.download_button("📥 Rapport Excel", data=generate_excel(get_mock_data()), file_name="rapport.xlsx")

st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;} .block-container {padding:0;}</style>", unsafe_allow_html=True)
dynamic_title = t['chap_titles'][st.session_state.chapter]

# ==========================================================
# 4. CSS (GLASSMORPHISM Y UI PREMIUM)
# ==========================================================
CSS_CODE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Montserrat:wght@800&display=swap');
    :root { --primary: #0066CC; --accent: #FFB100; --font-head: 'Montserrat', sans-serif; --font-body: 'Poppins', sans-serif; }
    body { background-image: url('https://images.unsplash.com/photo-1533107862482-0e6974b06ec4?q=80&w=2574&auto=format&fit=crop'); background-size: cover; background-attachment: fixed; color: #111; font-family: var(--font-body); margin: 0; padding-bottom: 90px; transition: background 0.3s; }
    
    /* 🧠 MODO ZEN (DUA) */
    body.mode-zen { background-image: none !important; background-color: #FDF6E3 !important; font-family: 'Comic Sans MS', sans-serif !important; color: #111 !important; }
    body.mode-zen .glass-panel { box-shadow: none !important; border: 2px solid #ccc !important; background-color: #fff !important; backdrop-filter: none; }
    body.mode-zen .map-frame { filter: none !important; }
    .btn-zen { background: #fff; border: 2px solid #ccc; border-radius: 20px; padding: 5px 15px; cursor: pointer; font-weight: bold; color: #333; transition: 0.2s; }
    
    /* PANELES DE CRISTAL (GLASSMORPHISM) */
    .glass-panel { background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.4); border-radius: 20px; padding: 20px; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2); margin-bottom: 20px; }
    
    /* CAMINO DE MISIONES ESTILO DUOLINGO */
    .path-container { display: flex; flex-direction: column; align-items: center; position: relative; padding: 20px 0; }
    .path-container::before { content: ''; position: absolute; width: 6px; background: rgba(255,255,255,0.8); top: 0; bottom: 0; left: 50%; transform: translateX(-50%); z-index: 0; border-radius: 10px; }
    .mission-node { position: relative; z-index: 1; width: 85%; background: white; border-radius: 20px; padding: 15px; display: flex; align-items: center; box-shadow: 0 5px 15px rgba(0,0,0,0.2); margin-bottom: 30px; border: 4px solid transparent; transition: 0.3s; cursor: pointer; }
    .mission-node.left { align-self: flex-start; margin-right: 10%; }
    .mission-node.right { align-self: flex-end; margin-left: 10%; flex-direction: row-reverse; text-align: right; }
    .mission-node.locked { background: rgba(220,220,220,0.9); filter: grayscale(1); cursor: not-allowed; opacity: 0.8; }
    .mission-node.active { border-color: var(--primary); transform: scale(1.05); animation: pulse 2s infinite; }
    .mission-node.completed { border-color: #00b894; background: #f0fff4; }
    .node-icon { width: 60px; height: 60px; background: #eee; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; margin: 0 15px; border: 3px solid #ccc; }
    .completed .node-icon { background: #00b894; color: white; border-color: #00b894; }
    .active .node-icon { background: var(--primary); color: white; border-color: var(--primary); }
    @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(0, 102, 204, 0.4); } 70% { box-shadow: 0 0 0 15px rgba(0, 102, 204, 0); } 100% { box-shadow: 0 0 0 0 rgba(0, 102, 204, 0); } }

    /* BOTONES */
    .btn-glass { background: rgba(0, 102, 204, 0.9); color: white; border: none; border-radius: 12px; padding: 12px 20px; font-weight: bold; width: 100%; transition: 0.2s; box-shadow: 0 4px 0 #004c99; }
    .btn-glass:active { transform: translateY(4px); box-shadow: none; }
    .btn-outline { background: white; border: 2px solid #ccc; color: #555; border-radius: 10px; padding: 10px; width: 100%; font-weight: 700; margin-top: 5px; cursor: pointer; }
    .solid-input, .solid-textarea { background-color: #f8f9fa; border: 2px solid #ddd; color: #333; padding: 12px; border-radius: 10px; width: 100%; font-size: 1rem; margin-bottom: 10px; font-family: var(--font-body); text-align: center; }
    .home-btn { background-color: white; border: none; border-radius: 18px; padding: 15px 10px; text-align: center; cursor: pointer; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 100px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); transition: transform 0.2s; }
    
    /* AVATARES */
    .avatar-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-bottom: 20px; }
    .avatar-item { background: white; border: 2px solid #ccc; border-radius: 10px; padding: 12px; text-align: center; cursor: pointer; transition: transform 0.1s; font-size: 1.5rem; color: #333; }
    .avatar-item.selected { background: #e6f0ff; border-color: var(--primary); border-width: 4px; box-shadow: 0 0 10px rgba(0,102,204,0.3); transform: scale(1.1); }
    .avatar-item.locked { background: #444; border-color: #222; color: #777; }
    .avatar-item.unlocked { background: #FFD700; border-color: #b8860b; color: #222; box-shadow: 0 0 10px rgba(255,215,0,0.5); }
    .trait-selector { display: flex; overflow-x: auto; padding-bottom: 10px; gap: 8px; }
    .trait-tag { background: white; border: 2px solid #ccc; color: #333; padding: 8px 15px; border-radius: 20px; white-space: nowrap; cursor: pointer; font-size: 0.9rem; }
    .trait-tag.selected { background: var(--accent); color: black; font-weight: 800; border-color: #e6a000; transform: scale(1.05); }

    /* NAVEGACIÓN DOCK */
    .dock-nav { position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(15px); border-top: 1px solid rgba(255,255,255,0.5); display: flex; justify-content: space-around; padding: 15px 0; z-index: 1000; box-shadow: 0 -5px 20px rgba(0,0,0,0.1); }
    .dock-item { font-size: 1.6rem; color: #aaa; cursor: pointer; transition: 0.2s; }
    .dock-item.active { color: var(--primary); transform: translateY(-5px); }
    
    /* VARIOS */
    .view { display: none; padding: 20px; min-height: 100vh; animation: fadeIn 0.4s; }
    .active-view { display: block; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    .progress-bar-bg { background: #e9ecef; height: 20px; border-radius: 10px; overflow: hidden; margin-top: 8px; }
    .fill-global { background: linear-gradient(90deg, #FFD93D, #FF6B6B); height: 100%; width: 0%; transition: width 1s ease-out; }
    .game-opt { background: #f0f0f0; padding: 15px; margin-bottom: 10px; border-radius: 8px; cursor: pointer; text-align: center; font-weight: bold; transition: 0.2s; }
    .xp-badge { background: var(--accent); color: #000; font-weight: 900; padding: 5px 15px; border-radius: 20px; font-size: 0.9rem; border: 2px solid #fff; display: inline-block;}
    .chap-title { font-family: var(--font-head); font-weight: 900; font-size: 1.5rem; color: var(--primary); margin-top: 10px; text-transform: uppercase; }
    .secret-box { border: 2px dashed #ccc; background: #fafafa; border-radius: 10px; padding: 15px; margin-top: 15px; text-align: center; }
    .medal-box { display: flex; gap: 10px; margin-top: 10px; }
    .medal { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; background: #eee; color: #aaa; border: 2px solid #ccc; transition: 0.3s; }
    .medal.unlocked.bronze { background: #cd7f32; color: white; border-color: #8c5622; box-shadow: 0 0 10px rgba(205,127,50,0.5); }
    .medal.unlocked.silver { background: #c0c0c0; color: white; border-color: #888; box-shadow: 0 0 10px rgba(192,192,192,0.5); }
    .medal.unlocked.gold { background: #ffd700; color: white; border-color: #b8860b; box-shadow: 0 0 15px rgba(255,215,0,0.8); }
    .mood-btn { font-size: 2.5rem; background: #fff; border: 2px solid #eee; border-radius: 12px; padding: 5px; cursor: pointer; flex: 1; text-align: center; margin: 0 3px; }
    .mood-btn.selected { background: #e6f0ff; border-color: var(--primary); transform: scale(1.1); }
    .custom-file-input { width: 100%; padding: 10px; background: #222; color: white; border-radius: 8px; cursor: pointer; margin-bottom: 10px; }
    .map-container { position: relative; width: 100%; height: 650px; background: #eee; border-radius: 15px; overflow: hidden; border: 4px solid white; box-shadow: 0 5px 25px rgba(0,0,0,0.3); display: flex; justify-content: center; align-items: center; }
    .map-frame { width: 150%; height: 150%; border: 0; pointer-events: none; transform: rotate(90deg); flex-shrink: 0; filter: contrast(1.1) saturate(1.1); }
    .map-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 5; }
    .map-pin { position: absolute; width: 55px; height: 55px; background: var(--accent); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #000; font-weight: 900; cursor: grab; border: 3px solid #fff; box-shadow: 0 6px 12px rgba(0,0,0,0.5); font-size: 1.8rem; z-index: 10; transform: translate(-50%, -50%); transition: transform 0.1s; }
    .map-hud { position: absolute; bottom: 15px; left: 15px; right: 15px; background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(10px); border-radius: 12px; padding: 15px; z-index: 20; border: 1px solid rgba(255,255,255,0.5); box-shadow: 0 10px 30px rgba(0,0,0,0.2); pointer-events: none; }
    #golden-star { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 4rem; text-shadow: 0 0 20px #FFD700; cursor: pointer; z-index: 100; display: none; }
    .custom-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 2000; justify-content: center; align-items: center; }
    .custom-modal.show { display: flex; }
</style>
"""

# ==========================================================
# 5. JAVASCRIPT LOGIC (CON MANEJO EXHAUSTIVO DE ERRORES)
# ==========================================================
JS_CODE = f"""
<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
<script type="module">
    import {{ initializeApp }} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
    import {{ getFirestore, doc, setDoc, getDoc, onSnapshot }} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore.js";

    // Inicialización segura de Firebase
    let db = null;
    try {{
        const firebaseConfig = {{ {FIREBASE_CONFIG} }};
        const fbApp = initializeApp(firebaseConfig);
        db = getFirestore(fbApp);
    }} catch (e) {{
        console.warn("Firebase config manquante ou invalide. Mode hors-ligne activé.");
    }}

    const sfx_coin = new Audio('https://actions.google.com/sounds/v1/cartoon/cartoon_boing.ogg');
    const sfx_unlock = new Audio('https://actions.google.com/sounds/v1/magic/magic_chime.ogg');

    window.app = {{
        currentChapter: {st.session_state.chapter},
        nominees: ["Les Titans", "Eco-Warriors", "Cyber-Français", "Green Team"],
        data: {{
            user: {{ sprite: "", name: "", trait: "", xp: 0, usedCodes: [], unlockedAvatars: [], myVote: "" }},
            missions: [],
            journal: []
        }},

        init: async () => {{
            if(localStorage.getItem('jo_avenir_zen') === 'true') document.body.classList.add('mode-zen');

            window.app.data.missions = [
                {{ id: 1, type: "code", code: "T0RELTc0QQ==", title: "{t['m1_title']}", odd: "ODD 1-17", icon: "fa-coins", desc: "{t['m1_desc']}", completed: false }},
                {{ id: 2, type: "code", code: "RVEtOTJC", title: "{t['m2_title']}", odd: "ODD 5 & 10", icon: "fa-users", desc: "{t['m2_desc']}", completed: false }},
                {{ id: 3, type: "code", code: "RUNPLTE4Qw==", title: "{t['m3_title']}", odd: "ODD 13", icon: "fa-recycle", desc: "{t['m3_desc']}", completed: false }},
                {{ id: 4, type: "code", code: "UkVHLTQ0RA==", title: "{t['m4_title']}", odd: "ODD 16", icon: "fa-scale-balanced", desc: "{t['m4_desc']}", completed: false }},
                {{ id: 5, type: "code", code: "TUlBTS02NkU=", title: "{t['m5_title']}", odd: "ODD 3", icon: "fa-apple-whole", desc: "{t['m5_desc']}", completed: false }},
                {{ id: 6, type: "code", code: "TUFQLTMxRg==", title: "{t['m6_title']}", odd: "ODD 11", icon: "fa-map", desc: "{t['m6_desc']}", completed: false }}
            ];

            // 🛡️ TRY-CATCH: Lectura de LocalStorage
            try {{
                const localData = localStorage.getItem("jo_avenir_2026");
                if (localData) {{
                    const parsedData = JSON.parse(localData);
                    if (parsedData && parsedData.user) window.app.data = parsedData;
                }}
            }} catch (error) {{
                console.error("Erreur critique de LocalStorage:", error);
                localStorage.removeItem("jo_avenir_2026");
                alert("⚠️ Cache corrompu. Réinitialisation du profil en cours.");
            }}

            // 🛡️ TRY-CATCH: Sincronización con Firebase
            try {{
                if (db && window.app.data.user.name !== "") {{
                    const docRef = doc(db, "students", window.app.data.user.name);
                    const docSnap = await getDoc(docRef);
                    if (docSnap.exists()) window.app.data = docSnap.data();
                    
                    onSnapshot(doc(db, "global", "stats"), (doc) => {{
                        if(doc.exists()) {{
                            let pct = (doc.data().totalXP / 100);
                            const gb = document.getElementById('global-xp');
                            if(gb) gb.style.width = pct + "%";
                        }}
                    }});
                }}
            }} catch (error) {{
                console.warn("Erreur de synchronisation Firebase (Travaillant hors-ligne):", error);
            }}

            window.app.renderAvatars();
            
            const tCont = document.getElementById('trait-container');
            tCont.innerHTML = "";
            const TRAITS = ["{t['traits'][0]}", "{t['traits'][1]}", "{t['traits'][2]}", "{t['traits'][3]}", "{t['traits'][4]}"];
            
            TRAITS.forEach(t => {{
                const span = document.createElement('span'); 
                span.className = "trait-tag";
                if(window.app.data.user.trait === t) span.classList.add('selected');
                span.innerText = t;
                span.onclick = function() {{
                    document.querySelectorAll('.trait-tag').forEach(el => el.classList.remove('selected'));
                    this.classList.add('selected');
                    window.app.data.user.trait = t;
                }};
                tCont.appendChild(span);
            }});

            window.app.updateUI();
            if (window.app.data.user.name !== "") {{
                document.getElementById('player-name').value = window.app.data.user.name;
                window.app.nav('dashboard');
                document.getElementById('app-dock').style.display = 'flex';
            }}
        }},

        toggleZen: () => {{
            document.body.classList.toggle('mode-zen');
            localStorage.setItem('jo_avenir_zen', document.body.classList.contains('mode-zen'));
        }},

        saveData: async () => {{
            // 🛡️ TRY-CATCH: Escritura local
            try {{
                localStorage.setItem("jo_avenir_2026", JSON.stringify(window.app.data));
            }} catch(e) {{
                console.error("Erreur sauvegarde locale:", e);
            }}
            
            // 🛡️ TRY-CATCH: Escritura remota
            try {{
                if(db && window.app.data.user.name !== "") {{
                    await setDoc(doc(db, "students", window.app.data.user.name), window.app.data);
                }}
            }} catch(e) {{
                console.warn("Erreur sauvegarde cloud:", e);
            }}
            window.app.updateUI();
        }},

        addXP: (amount) => {{
            sfx_coin.play().catch(e => console.warn("Audio bloqué par navigateur"));
            window.app.data.user.xp += amount;
            window.app.saveData();
            confetti({{ particleCount: 100, spread: 70, origin: {{ y: 0.6 }} }});
        }},

        renderAvatars: () => {{
            const grid = document.getElementById('sprite-container'); 
            grid.innerHTML = "";
            const SPRITES = ["fa-dragon", "fa-ghost", "fa-robot", "fa-cat", "fa-bolt", "fa-fire", "fa-snowflake", "fa-leaf", "fa-crow", "fa-spider", "fa-fish", "fa-bug", "fa-hippo", "fa-otter", "fa-frog", "fa-horse", "fa-dove", "fa-dog", "fa-kiwi-bird", "fa-worm", "fa-locust", "fa-mosquito", "fa-meteor"];
            const HIDDEN_SPRITES = [
                {{ icon: "fa-crown", code: "NOVA-33" }}, {{ icon: "fa-user-astronaut", code: "TITAN-8X" }}, 
                {{ icon: "fa-jedi", code: "NEXUS-V" }}, {{ icon: "fa-user-ninja", code: "PHOENIX-9" }}, 
                {{ icon: "fa-mask", code: "SPARK-44" }}, {{ icon: "fa-hat-wizard", code: "AURA-77" }}, 
                {{ icon: "fa-gem", code: "ECHO-LUM" }}
            ];
            
            SPRITES.forEach(icon => {{
                const div = document.createElement('div');
                div.className = "avatar-item";
                if(window.app.data.user.sprite === icon) div.classList.add('selected');
                div.innerHTML = `<i class="fa-solid ${{icon}}"></i>`;
                div.onclick = function() {{
                    document.querySelectorAll('.avatar-item').forEach(el => el.classList.remove('selected'));
                    this.classList.add('selected');
                    window.app.data.user.sprite = icon;
                }};
                grid.appendChild(div);
            }});
            
            HIDDEN_SPRITES.forEach(h => {{
                const div = document.createElement('div');
                if (window.app.data.user.unlockedAvatars.includes(h.icon)) {{
                    div.className = "avatar-item unlocked";
                    if(window.app.data.user.sprite === h.icon) div.classList.add('selected');
                    div.innerHTML = `<i class="fa-solid ${{h.icon}}"></i>`;
                    div.onclick = function() {{
                        document.querySelectorAll('.avatar-item').forEach(el => el.classList.remove('selected'));
                        this.classList.add('selected');
                        window.app.data.user.sprite = h.icon;
                    }};
                }} else {{
                    div.className = "avatar-item locked";
                    div.innerHTML = `<i class="fa-solid fa-lock"></i>`;
                    div.onclick = function() {{
                        const guess = prompt("Code secret:");
                        if (guess && guess.trim().toUpperCase() === h.code) {{
                            window.app.data.user.unlockedAvatars.push(h.icon);
                            window.app.saveData();
                            window.app.renderAvatars();
                            confetti();
                        }} else if(guess) {{
                            alert("{t['code_invalid']}");
                        }}
                    }};
                }}
                grid.appendChild(div);
            }});
        }},

        updateUI: () => {{
            const xp = window.app.data.user.xp || 0;
            document.getElementById('xp-counter').innerText = xp;
            
            const mini = document.getElementById('mini-avatar');
            if(window.app.data.user.sprite && mini) {{
                mini.innerHTML = `<i class="fa-solid ${{window.app.data.user.sprite}}"></i>`;
            }}
            
            if (xp >= 100) document.getElementById('m-bronze').classList.add('unlocked', 'bronze');
            if (xp >= 300) document.getElementById('m-silver').classList.add('unlocked', 'silver');
            if (xp >= 500) document.getElementById('m-gold').classList.add('unlocked', 'gold');
            
            let globalPct = Math.min((xp / 1000) * 100, 100);
            const gb = document.querySelector('.fill-global');
            if(gb) gb.style.width = globalPct + "%";
            
            if (globalPct >= 100) document.getElementById('golden-star').style.display = 'block';
        }},

        checkSecretCode: () => {{
            const input = document.getElementById('secret-code-input').value.trim().toUpperCase();
            const hashedInput = btoa(input);
            const SECRET_CODES = {{
                "UkVMQUlTLTEwMA==": {{ xp: 100, msg: "+100 XP" }}, 
                "QklPUy01MA==": {{ xp: 50, msg: "+50 XP (SVT)" }}, 
                "QVRMQVMtNTA=": {{ xp: 50, msg: "+50 XP (GÉO)" }}, 
                "TUFUSC01MA==": {{ xp: 50, msg: "+50 XP (MATHS)" }}
            }};
            const msgBox = document.getElementById('secret-msg');
            
            if(window.app.data.user.usedCodes.includes(hashedInput)) {{
                msgBox.innerText = "{t['code_used']}"; msgBox.style.color = "#dc3545";
                return;
            }}
            
            if(SECRET_CODES[hashedInput]) {{
                window.app.data.user.usedCodes.push(hashedInput);
                window.app.addXP(SECRET_CODES[hashedInput].xp);
                msgBox.innerText = SECRET_CODES[hashedInput].msg; 
                msgBox.style.color = "#28a745"; 
                document.getElementById('secret-code-input').value = "";
            }} else {{
                msgBox.innerText = "{t['code_invalid']}"; 
                msgBox.style.color = "#dc3545";
            }}
        }},

        claimUltimateReward: () => {{
            confetti({{ particleCount: 300, spread: 160, origin: {{ y: 0.4 }} }});
            document.getElementById('golden-star').style.display = 'none'; 
            document.getElementById('ultimateModal').classList.add('show');
        }},

        saveProfile: () => {{
            const name = document.getElementById('player-name').value;
            if(!window.app.data.user.sprite || !name || !window.app.data.user.trait) {{
                alert("{t['alert_profile']}");
                return;
            }}
            window.app.data.user.name = name;
            if(window.app.data.user.xp === undefined) window.app.data.user.xp = 0;
            window.app.saveData();
            window.app.nav('dashboard');
            document.getElementById('app-dock').style.display = 'flex';
        }},

        nav: (view) => {{
            document.querySelectorAll('.view').forEach(v => v.classList.remove('active-view'));
            document.getElementById('view-' + view).classList.add('active-view');
            document.querySelectorAll('.dock-item').forEach(i => i.classList.remove('active'));
            if(document.getElementById('nav-' + view)) document.getElementById('nav-' + view).classList.add('active');
            
            if(view === 'dashboard') window.app.renderPath();
            if(view === 'journal') window.app.renderJournal();
            if(view === 'oscars') window.app.renderNominees();
        }},

        renderPath: () => {{
            const container = document.getElementById('path-container'); 
            container.innerHTML = "";
            window.app.data.missions.forEach((m, idx) => {{
                const isLeft = idx % 2 === 0; 
                const reqChapter = idx + 1;
                let statusClass = m.completed ? 'completed' : ''; 
                let iconClass = m.completed ? 'fa-check' : m.icon;
                
                if (window.app.currentChapter < reqChapter) {{
                    statusClass = 'locked'; iconClass = 'fa-lock';
                }} else if (!m.completed && (idx === 0 || window.app.data.missions[idx-1].completed)) {{
                    statusClass = 'active';
                }}
                
                container.innerHTML += `
                <div class="mission-node ${{isLeft ? 'left' : 'right'}} ${{statusClass}}" onclick="window.app.openModal(${{m.id}}, '${{statusClass}}')">
                    <div class="node-icon"><i class="fa-solid ${{iconClass}}"></i></div>
                    <div>
                        <h5 class="mb-0 fw-bold">${{m.title}}</h5>
                        <small class="text-secondary">${{statusClass==='locked' ? "{t['locked_chap']} "+reqChapter : m.desc}}</small>
                    </div>
                </div>`;
            }});
        }},

        openModal: (id, status) => {{
            if(status === 'locked' || status === 'completed') return;
            window.app.currentId = id; 
            const m = window.app.data.missions.find(x => x.id === id);
            document.getElementById('modal-title').innerText = m.title; 
            document.getElementById('modal-desc').innerText = m.desc; 
            document.getElementById('modal-odd').innerText = m.odd;
            document.getElementById('user-input').value = ""; 
            document.getElementById('feedback-msg').innerText = ""; 
            document.getElementById('customModal').classList.add('show');
        }},

        closeModal: () => {{
            document.getElementById('customModal').classList.remove('show');
        }},

        validate: () => {{
            const inp = document.getElementById('user-input').value.trim().toUpperCase(); 
            const hashedInp = btoa(inp); 
            const m = window.app.data.missions.find(x => x.id === window.app.currentId);
            if(hashedInp === m.code) {{
                sfx_unlock.play().catch(e=>console.warn(e)); 
                m.completed = true; 
                document.getElementById('feedback-msg').innerText = "{t['validated_xp']}"; 
                document.getElementById('feedback-msg').style.color = "#28a745"; 
                window.app.addXP(100);
                setTimeout(() => {{ window.app.closeModal(); window.app.renderPath(); }}, 1200);
            }} else {{
                document.getElementById('feedback-msg').innerText = "{t['incorrect']}"; 
                document.getElementById('feedback-msg').style.color = "#dc3545";
            }}
        }},

        renderNominees: () => {{
            const list = document.getElementById('nominees-list'); 
            list.innerHTML = "";
            window.app.nominees.forEach(n => {{
                list.innerHTML += `
                <div class='glass-panel d-flex justify-content-between align-items-center mb-2'>
                    <span class="fw-bold text-dark">${{n}}</span>
                    <button class='btn btn-warning fw-bold' style='border-radius:8px;' onclick='window.app.submitVote("${{n}}")'>{t['vote_btn']}</button>
                </div>`;
            }});
        }},

        submitVote: (name) => {{
            if(window.app.data.user.myVote && window.app.data.user.myVote !== "") {{
                alert("{t['already_voted']}"); 
                return;
            }}
            if(confirm("Voter pour " + name + " ?")) {{
                window.app.data.user.myVote = name; 
                window.app.addXP(20); 
                window.app.saveData(); 
                window.app.renderNominees();
            }}
        }},

        selectMood: (e,m) => {{
            document.querySelectorAll('.mood-btn').forEach(b => b.classList.remove('selected'));
            e.classList.add('selected'); 
            document.getElementById('selected-mood').value = m;
        }},

        saveJournal: () => {{ 
            const m = document.getElementById('selected-mood').value;
            const t = document.getElementById('journal-text').value;
            if(!m || !t) return; 
            
            if(!window.app.data.journal) window.app.data.journal = [];
            window.app.data.journal.unshift({{d: new Date().toLocaleDateString(), m: m, t: t}});
            
            window.app.addXP(20); 
            window.app.saveData(); 
            window.app.renderJournal();
            
            document.getElementById('journal-text').value = ""; 
            document.getElementById('selected-mood').value = "";
            document.querySelectorAll('.mood-btn').forEach(b => b.classList.remove('selected'));
        }},

        renderJournal: () => {{
            const c = document.getElementById('journal-feed'); 
            c.innerHTML = ""; 
            if(!window.app.data.journal) window.app.data.journal = []; 
            window.app.data.journal.forEach(e => {{ 
                c.innerHTML += `
                <div class='glass-panel'>
                    <div class='d-flex justify-content-between mb-2'>
                        <span class="text-secondary small fw-bold">${{e.d}}</span>
                        <span style="font-size:1.5rem;">${{e.m}}</span>
                    </div>
                    <p class='text-dark mb-0'>${{e.t}}</p>
                </div>`;
            }}); 
        }},

        allowDrop: (ev) => {{ ev.preventDefault(); }},
        drag: (ev) => {{ ev.dataTransfer.setData("text", ev.target.id); }},
        drop: (ev) => {{ 
            ev.preventDefault(); 
            const data = ev.dataTransfer.getData("text"); 
            const el = document.getElementById(data); 
            const rect = ev.currentTarget.getBoundingClientRect(); 
            const x = ev.clientX - rect.left; 
            const y = ev.clientY - rect.top; 
            el.style.left = ((x / rect.width) * 100) + "%"; 
            el.style.top = ((y / rect.height) * 100) + "%"; 
        }},

        speakText: (text) => {{
            window.speechSynthesis.cancel(); 
            const msg = new SpeechSynthesisUtterance(); 
            msg.text = text; 
            msg.lang = 'fr-FR'; 
            window.speechSynthesis.speak(msg);
        }},

        speakQuestion: () => {{
            window.app.speakText(document.getElementById('game-question').innerText);
        }},

        startGame: (t) => {{
            const QUIZ = {{
                num: [{{ q: "10 stylos = 20€. 1 stylo = ?", a: ["2€", "5€", "1€"], c: 0 }}],
                fut: [{{ q: "Demain je ___ (manger)", a: ["mangerai", "mangerais", "mange"], c: 0 }}],
                part: [{{ q: "Je veux ___ eau", a: ["de l'", "du", "de la"], c: 0 }}],
                sport: [{{ q: "Le sport dans l'eau ?", a: ["Natation", "Judo", "Tennis"], c: 0 }}],
                imp: [{{ q: "(Courir) ___ vite !", a: ["Cours", "Coures", "Courir"], c: 0 }}],
                odd: [{{ q: "ODD 13 c'est pour...", a: ["Le Climat", "La Faim", "L'Eau"], c: 0 }}],
                bio: [{{ q: "Où jeter une bouteille en plastique ? (ODD 12)", a: ["Poubelle Jaune", "Poubelle Verte"], c: 0 }}],
                geo: [{{ q: "Où sont nés les Jeux Olympiques ?", a: ["En Grèce", "En France"], c: 0 }}],
                math: [{{ q: "Un athlète court 100m en 10s. Vitesse ?", a: ["10 m/s", "100 m/s", "1 m/s"], c: 0 }}],
                fra: [{{ q: "Il faut que nous _____ (participer).", a: ["participions", "participons", "participerons"], c: 0 }}]
            }};
            currentQuiz = QUIZ[t]; 
            qIndex = 0; 
            score = 0; 
            document.getElementById('game-menu').style.display = 'none'; 
            document.getElementById('game-interface').style.display = 'block'; 
            window.app.renderQuestion(); 
        }},

        renderQuestion: () => {{
            if(qIndex >= currentQuiz.length) {{
                alert("{t['end_score']}" + score); 
                window.app.addXP(score); 
                window.app.exitGame(); 
                return;
            }} 
            const q = currentQuiz[qIndex]; 
            document.getElementById('game-question').innerText = q.q; 
            const o = document.getElementById('game-options'); 
            o.innerHTML = ""; 
            q.a.forEach((ans, i) => {{
                o.innerHTML += `<div class='game-opt' onclick='window.app.checkAnswer(${{i}})'>${{ans}}</div>`;
            }}); 
        }},

        checkAnswer: (i) => {{
            const q = currentQuiz[qIndex];
            window.app.speakText(q.a[i]); 
            if(i === q.c) {{
                score += 10; 
                confetti({{ particleCount: 50, spread: 40, origin: {{ y: 0.7 }} }});
            }} 
            setTimeout(() => {{
                qIndex++; 
                window.app.renderQuestion();
            }}, 1200); 
        }},

        exitGame: () => {{
            document.getElementById('game-interface').style.display = 'none'; 
            document.getElementById('game-menu').style.display = 'flex'; 
        }}
    }};

    // Iniciar
    setTimeout(() => window.app.init(), 200);
</script>
"""

# ==========================================================
# 6. HTML FINAL
# ==========================================================
HTML_CODE = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    {CSS_CODE}
</head>
<body>
    <div style="position:fixed; top:10px; right:10px; z-index:9999;">
        <button class="btn-zen" onclick="window.app.toggleZen()">🧠 Mode Zen</button>
    </div>

    <!-- VISTA INICIO -->
    <section id="view-home" class="view active-view">
        <div class="glass-panel text-center mt-4">
            <lottie-player src="https://assets2.lottiefiles.com/packages/lf20_q5pk6p1k.json" background="transparent" speed="1" style="width:150px; height:150px; margin:auto;" loop autoplay></lottie-player>
            <h1 class="fw-bold" style="font-family: var(--font-head); font-size:2.5rem; margin-top:10px;">J.O. AVENIR</h1>
            <h4 class="text-secondary">{dynamic_title}</h4>
        </div>
        <div class="glass-panel mt-4">
            <h4 class="fw-bold">{t['create_athlete']}</h4>
            <div class="avatar-grid" id="sprite-container"></div>
            <input type="text" id="player-name" class="solid-input mb-3" placeholder="{t['name_label']}">
            <div class="trait-selector" id="trait-container"></div>
            <button class="btn-glass mt-2" onclick="window.app.saveProfile()">{t['enter_stadium']} <i class="fa-solid fa-person-running"></i></button>
        </div>
    </section>

    <!-- VISTA DASHBOARD -->
    <section id="view-dashboard" class="view">
        <div class="glass-panel d-flex justify-content-between align-items-center">
            <div>
                <h5 class="fw-bold mb-0">Profil</h5>
                <div class="badge bg-warning text-dark fs-6 mt-1"><i class="fa-solid fa-star"></i> <span id="xp-counter">0</span> XP</div>
                <div class="medal-box mt-2">
                    <div id="m-bronze" class="medal"><i class="fa-solid fa-medal"></i></div>
                    <div id="m-silver" class="medal"><i class="fa-solid fa-medal"></i></div>
                    <div id="m-gold" class="medal"><i class="fa-solid fa-trophy"></i></div>
                </div>
            </div>
            <div id="mini-avatar" style="font-size: 2.2rem; color: var(--primary); background: white; padding: 15px; border-radius: 50%; box-shadow: 0 4px 10px rgba(0,0,0,0.1);"></div>
        </div>

        <div class="glass-panel">
            <h6 class="fw-bold"><i class="fa-solid fa-earth-americas text-primary"></i> {t['global_impact']}</h6>
            <div class="progress" style="height: 15px; border-radius: 10px; background:#fff;">
                <div id="global-xp" class="progress-bar bg-success progress-bar-striped progress-bar-animated" style="width: 10%"></div>
            </div>
            <small class="text-secondary">{t['obj_comm']}</small>
        </div>

        <div class="row g-2 mb-4">
            <div class="col-6"><div class="home-btn" onclick="window.app.nav('map')"><i class="fa-solid fa-map-location-dot text-success mb-1 fs-2"></i><h6 class="fw-bold">{t['map_btn']}</h6></div></div>
            <div class="col-6"><div class="home-btn" onclick="window.app.nav('journal')"><i class="fa-solid fa-book-open text-info mb-1 fs-2"></i><h6 class="fw-bold">{t['journal_btn']}</h6></div></div>
            <div class="col-6"><div class="home-btn" onclick="window.app.nav('games')"><i class="fa-solid fa-gamepad text-primary mb-1 fs-2"></i><h6 class="fw-bold">{t['arcade_btn']}</h6></div></div>
            <div class="col-6"><div class="home-btn" style="background: linear-gradient(135deg, #fff3e0, #ffe0b2);" onclick="window.app.nav('oscars')"><i class="fa-solid fa-award text-warning mb-1 fs-2"></i><h6 class="fw-bold">{t['oscars_btn']}</h6></div></div>
        </div>

        <div class="glass-panel">
            <h6 class="fw-bold text-dark"><i class="fa-solid fa-user-secret text-danger"></i> {t['secret_codes_title']}</h6>
            <div class="d-flex gap-2">
                <input type="text" id="secret-code-input" class="solid-input mb-0" placeholder="CODE...">
                <button class="btn btn-dark" style="border-radius: 8px; font-weight:bold;" onclick="window.app.checkSecretCode()">GO</button>
            </div>
            <div id="secret-msg" class="small mt-2 fw-bold"></div>
        </div>

        <h4 class="fw-bold text-center mt-5 mb-4 text-white" style="text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">{t['progression']}</h4>
        <div id="path-container" class="path-container"></div>
    </section>

    <!-- VISTA MAPA -->
    <section id="view-map" class="view">
        <div class="glass-panel">
            <h4 class="fw-bold text-center">{t['campus_map']}</h4>
            <div class="map-container mt-3">
                 <iframe class="map-frame" src="https://maps.google.com/maps?q=38.9763185,-3.9443803&t=k&z=19&ie=UTF8&iwloc=&output=embed" frameborder="0"></iframe>
                 <div class="map-overlay" ondrop="window.app.drop(event)" ondragover="window.app.allowDrop(event)">
                    <div id="pin1" class="map-pin pin-pulse" draggable="true" ondragstart="window.app.drag(event)" style="top: 10%; left: 10%; background:#FFD93D;">🚀</div>
                    <div id="pin2" class="map-pin" draggable="true" ondragstart="window.app.drag(event)" style="top: 10%; left: 30%; background:#FF6B6B;">🏁</div>
                    <div id="pin3" class="map-pin" draggable="true" ondragstart="window.app.drag(event)" style="top: 10%; left: 50%; background:#4D79FF;">🍎</div>
                    <div id="pin4" class="map-pin" draggable="true" ondragstart="window.app.drag(event)" style="top: 10%; left: 70%; background:#28a745;">♻️</div>
                    <div id="pin5" class="map-pin" draggable="true" ondragstart="window.app.drag(event)" style="top: 30%; left: 10%; background:#17a2b8;">💧</div>
                    <div id="pin6" class="map-pin" draggable="true" ondragstart="window.app.drag(event)" style="top: 30%; left: 30%; background:#e83e8c;">🏥</div>
                    <div id="golden-star" onclick="window.app.claimUltimateReward()">🌟</div>
                </div>
            </div>
        </div>
    </section>

    <!-- VISTA OSCARS (COEVALUACIÓN) -->
    <section id="view-oscars" class="view">
        <h4 class="fw-bold mb-3 text-white" style="text-shadow: 1px 1px 3px rgba(0,0,0,0.5);">{t['oscars_title']}</h4>
        <div id="nominees-list"></div>
    </section>

    <!-- VISTA DIARIO -->
    <section id="view-journal" class="view">
        <h4 class="fw-bold mb-3 text-white" style="text-shadow: 1px 1px 3px rgba(0,0,0,0.5);">{t['journal_title']}</h4>
        <div class="glass-panel">
            <label class="small text-secondary mb-2">{t['mood']}</label>
            <div class="d-flex justify-content-between mb-3">
                <div class="mood-btn" onclick="window.app.selectMood(this, '🤩')">🤩</div>
                <div class="mood-btn" onclick="window.app.selectMood(this, '🙂')">🙂</div>
                <div class="mood-btn" onclick="window.app.selectMood(this, '😐')">😐</div>
                <div class="mood-btn" onclick="window.app.selectMood(this, '🥱')">🥱</div>
            </div>
            <input type="hidden" id="selected-mood">
            <textarea id="journal-text" class="solid-textarea mt-2" rows="2" placeholder="{t['reflection']}"></textarea>
            <button onclick="window.app.saveJournal()" class="btn-glass mt-2">{t['post']}</button>
        </div>
        <div id="journal-feed" class="mt-4"></div>
    </section>

    <!-- VISTA JUEGOS ARCADE -->
    <section id="view-games" class="view">
        <h4 class="fw-bold mb-3 text-white" style="text-shadow: 1px 1px 3px rgba(0,0,0,0.5);">{t['arcade_title']}</h4>
        <div id="game-menu" class="row g-2">
            <div class="col-6"><div class="glass-panel p-3 mb-2 text-center" onclick="window.app.startGame('num')" style="cursor:pointer;"><i class="fa-solid fa-calculator fa-2x text-primary mb-2"></i><br><h6 class="mb-0 fw-bold small">NOMBRES</h6></div></div>
            <div class="col-6"><div class="glass-panel p-3 mb-2 text-center" onclick="window.app.startGame('fut')" style="cursor:pointer;"><i class="fa-solid fa-rocket fa-2x text-warning mb-2"></i><br><h6 class="mb-0 fw-bold small">FUTUR</h6></div></div>
            <div class="col-6"><div class="glass-panel p-3 mb-2 text-center" onclick="window.app.startGame('part')" style="cursor:pointer;"><i class="fa-solid fa-pizza-slice fa-2x text-danger mb-2"></i><br><h6 class="mb-0 fw-bold small">PARTITIFS</h6></div></div>
            <div class="col-6"><div class="glass-panel p-3 mb-2 text-center" onclick="window.app.startGame('sport')" style="cursor:pointer;"><i class="fa-solid fa-person-running fa-2x text-success mb-2"></i><br><h6 class="mb-0 fw-bold small">SPORT</h6></div></div>
            <div class="col-6"><div class="glass-panel p-3 mb-2 text-center" onclick="window.app.startGame('imp')" style="cursor:pointer;"><i class="fa-solid fa-bullhorn fa-2x text-info mb-2"></i><br><h6 class="mb-0 fw-bold small">IMPÉRATIF</h6></div></div>
            <div class="col-6"><div class="glass-panel p-3 mb-2 text-center" onclick="window.app.startGame('odd')" style="cursor:pointer;"><i class="fa-solid fa-earth-europe fa-2x text-primary mb-2"></i><br><h6 class="mb-0 fw-bold small">QUIZ ODD</h6></div></div>
            <div class="col-6"><div class="glass-panel p-3 mb-2 text-center" onclick="window.app.startGame('bio')" style="cursor:pointer;"><i class="fa-solid fa-leaf fa-2x text-success mb-2"></i><br><h6 class="mb-0 fw-bold small">SVT</h6></div></div>
            <div class="col-6"><div class="glass-panel p-3 mb-2 text-center" onclick="window.app.startGame('geo')" style="cursor:pointer;"><i class="fa-solid fa-globe fa-2x text-info mb-2"></i><br><h6 class="mb-0 fw-bold small">GÉO</h6></div></div>
            <div class="col-6"><div class="glass-panel p-3 mb-2 text-center" onclick="window.app.startGame('math')" style="cursor:pointer;"><i class="fa-solid fa-square-root-variable fa-2x text-secondary mb-2"></i><br><h6 class="mb-0 fw-bold small">MATHS</h6></div></div>
            <div class="col-6"><div class="glass-panel p-3 mb-2 text-center" onclick="window.app.startGame('fra')" style="cursor:pointer;"><i class="fa-solid fa-comment-dots fa-2x text-danger mb-2"></i><br><h6 class="mb-0 fw-bold small">FRANÇAIS</h6></div></div>
        </div>
        <div id="game-interface" style="display:none;">
            <div class="glass-panel">
                <div class="d-flex justify-content-center align-items-center mb-3">
                    <h5 id="game-question" class="fw-bold mb-0 text-center">...</h5>
                    <button class="tts-btn" onclick="window.app.speakQuestion()" style="background:none; border:none; font-size:1.5rem; margin-left:10px;">🔊</button>
                </div>
                <div id="game-options"></div>
            </div>
            <button onclick="window.app.exitGame()" class="btn btn-outline w-100">{t['quit']}</button>
        </div>
    </section>

    <!-- NAVEGACIÓN DOCK (BOTTOM BAR) -->
    <div id="app-dock" class="dock-nav" style="display:none;">
        <div id="nav-dashboard" class="dock-item active" onclick="window.app.nav('dashboard')"><i class="fa-solid fa-route"></i></div>
        <div id="nav-map" class="dock-item" onclick="window.app.nav('map')"><i class="fa-solid fa-map-location-dot"></i></div>
        <div id="nav-journal" class="dock-item" onclick="window.app.nav('journal')"><i class="fa-solid fa-book-open"></i></div>
        <div id="nav-oscars" class="dock-item" onclick="window.app.nav('oscars')"><i class="fa-solid fa-award"></i></div>
    </div>

    <!-- MODAL MISIONES -->
    <div id="customModal" class="custom-modal">
        <div class="glass-panel" style="width: 90%; max-width: 400px; text-align: center;">
            <h4 id="modal-title" class="fw-bold mb-2">...</h4>
            <div class="badge bg-warning text-dark mb-2" id="modal-odd">ODD</div>
            <p id="modal-desc" class="text-secondary small mb-4">...</p>
            <input type="text" id="user-input" class="solid-input text-uppercase" placeholder="CODE">
            <button onclick="window.app.validate()" class="btn-glass mb-2">{t['validate']}</button>
            <button onclick="window.app.closeModal()" class="btn btn-outline">{t['close']}</button>
            <div id="feedback-msg" class="mt-3 small fw-bold"></div>
        </div>
    </div>
    
    <!-- MODAL FINAL (ESTRELLA DORADA) -->
    <div id="ultimateModal" class="custom-modal">
        <div class="glass-panel" style="width: 90%; max-width: 400px; text-align: center; border: 4px solid #FFD700;">
            <i class="fa-solid fa-crown fa-4x mb-3" style="color: #FFD700; text-shadow: 0 4px 10px rgba(255,215,0,0.5);"></i>
            <h2 class="fw-bold text-dark">{t['legend_unlocked']}</h2>
            <h4 class="fw-bold text-danger mb-3">{t['org_top']}</h4>
            <p class="text-secondary small mb-4">{t['win_msg']}</p>
            <button onclick="document.getElementById('ultimateModal').classList.remove('show')" class="btn-glass" style="background:#FFD700; color:#000;">{t['amazing']}</button>
        </div>
    </div>

    {JS_CODE}
</body>
</html>
"""

components.html(HTML_CODE, height=900, scrolling=True)
