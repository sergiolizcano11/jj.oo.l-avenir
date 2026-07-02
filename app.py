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

# --- SISTEMA MULTI-IDIOMA INTEGRAL ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'Français'
if 'chapter' not in st.session_state:
    st.session_state.chapter = 1

translations = {
    'Français': {
        # Sidebar
        'tools': "Boîte à Outils", 'tts': "🗣️ Lecteur (TTS)", 'tts_help': "Écrivez pour écouter.", 
        'listen': "Écouter 🔊", 'mic': "🎙️ Micro (Oral)", 'mic_help': "Enregistrez-vous.",
        'card': "🎒 Carte Élève", 'name': "Ton Nom:", 'trait': "Ton Atout:", 
        'traits': ["Vitesse", "Force", "Stratégie", "Créativité", "Éloquence"], 'download_pdf': "📄 Ma Carte (+ QR)",
        'admin': "🔐 Zone Professeur", 'pass': "Mot de passe Prof:",
        'chap_control': "Contrôle de l'Histoire", 'chap': "Chapitre:", 
        'data_link': "Lien Base de Données:", 'reset': "🗑️ Effacer (Test)",
        'chap_titles': {1: "Chapitre 1: L'Appel", 2: "Chapitre 2: L'Équipe", 3: "Chapitre 3: L'Action", 4: "Chapitre 4: Les Règles", 5: "Chapitre 5: L'Énergie", 6: "Chapitre 6: La Gloire"},
        # App UI
        'create_athlete': "CRÉEZ VOTRE ATHLÈTE", 'choose_champ': "CHOISISSEZ VOTRE CHAMPION",
        'name_label': "NOM", 'power_label': "SUPER-POUVOIR", 'enter_stadium': "ENTRER DANS LE STADE",
        'global_impact': "IMPACT GLOBAL", 'class': "CLASSE", 'obj_comm': "Objectif commun (ODD 17)",
        'no_team': "Pas d'équipe", 'missions_btn': "MISSIONS", 'map_btn': "PLAN", 'journal_btn': "JOURNAL", 'arcade_btn': "ARCADE / TESTS",
        'oscars_btn': "VOTE & ÉVALUATION", 'oscars_title': "CO-ÉVALUATION GYMKHANA", 'vote_btn': "VOTER", 'vote_thanks': "Vote enregistré ! +20 XP", 'already_voted': "Vous avez déjà voté !", 'oscars_desc': "Évaluez l'implication et le Fair-Play des autres équipes (ODD 17).",
        'progression': "PROGRESSION", 'secret_codes_title': "CODES SECRETS", 'secret_codes_desc': "As-tu un code caché ? Remplissez pour obtenir de l'XP !",
        'back': "Retour", 'campus_map': "PLAN DU CAMPUS", 'drag_icons': "Glissez les icônes sur le collège !",
        'legend': "LÉGENDE", 'arcade_title': "ARCADE INTERDISCIPLINAIRE", 'quit': "Quitter",
        'locked_chap': "Chapitre Requis", 'validate': "VALIDER", 'close': "Fermer",
        'legend_unlocked': "LÉGENDE DÉBLOQUÉE", 'org_top': "🏅 ORGANISATEURS TOP 🏅",
        'win_msg': "La classe a atteint 100% d'Impact Global ! Vous êtes officiellement les maîtres des Jeux de l'Avenir. Le comité vous accorde l'Insigne Ultime.",
        'amazing': "INCROYABLE !", 'journal_title': "JOURNAL DE BORD", 'mood': "HUMEUR", 'reflection': "Réflexion...", 'photo': "PHOTO", 'post': "POSTER L'ENTRÉE",
        # Pins & Alerts
        'p_start': "Départ", 'p_end': "Arrivée", 'p_food': "Ravito", 'p_recyc': "Recyclage", 'p_water': "Eau", 'p_med': "Secours",
        'alert_profile': "Complétez votre profil !", 'code_used': "Code déjà utilisé !", 'code_invalid': "Code invalide.",
        'validated_xp': "Validé ! +100 XP", 'incorrect': "Incorrect", 'end_score': "Fin! Score: ",
        # Missions (6)
        'm1_title': "Conférence ODD", 'm1_desc': "Création monnaie solidaire.",
        'm2_title': "Équipes Inclusives", 'm2_desc': "Création des équipes.",
        'm3_title': "Obstacles Avenir", 'm3_desc': "Design d'épreuves.",
        'm4_title': "Règlement", 'm4_desc': "Pacte de Fair-play.",
        'm5_title': "Ravitaillement", 'm5_desc': "Snacks sains et locaux.",
        'm6_title': "Plan Parcours", 'm6_desc': "Tracé sur le campus."
    },
    'Español': {
        # Sidebar
        'tools': "Herramientas", 'tts': "🗣️ Lector (TTS)", 'tts_help': "Escribe para escuchar.", 
        'listen': "Escuchar 🔊", 'mic': "🎙️ Micrófono", 'mic_help': "Grábate.",
        'card': "🎒 Carnet Alumno", 'name': "Tu Nombre:", 'trait': "Tu Habilidad:", 
        'traits': ["Velocidad", "Fuerza", "Estrategia", "Creatividad", "Elocuencia"], 'download_pdf': "📄 Mi Carnet (+ QR)",
        'admin': "🔐 Zona Profesor", 'pass': "Contraseña:",
        'chap_control': "Control Historia", 'chap': "Capítulo:", 
        'data_link': "Enlace Base de Datos:", 'reset': "🗑️ Borrar (Test)",
        'chap_titles': {1: "Cap. 1: La Llamada", 2: "Cap. 2: El Equipo", 3: "Cap. 3: La Acción", 4: "Cap. 4: Las Reglas", 5: "Cap. 5: La Energía", 6: "Cap. 6: La Gloria"},
        # App UI
        'create_athlete': "CREA TU ATLETA", 'choose_champ': "ELIGE TU CAMPEÓN",
        'name_label': "NOMBRE", 'power_label': "SUPERPODER", 'enter_stadium': "ENTRAR AL ESTADIO",
        'global_impact': "IMPACTO GLOBAL", 'class': "CLASE", 'obj_comm': "Objetivo común (ODS 17)",
        'no_team': "Sin equipo", 'missions_btn': "MISIONES", 'map_btn': "MAPA", 'journal_btn': "DIARIO", 'arcade_btn': "ARCADE / TESTS",
        'oscars_btn': "VOTO Y EVALUACIÓN", 'oscars_title': "COEVALUACIÓN GYMKHANA", 'vote_btn': "VOTAR", 'vote_thanks': "¡Voto registrado! +20 XP", 'already_voted': "¡Ya has votado!", 'oscars_desc': "Evalúa la implicación y el Fair-Play de los demás equipos (ODS 17).",
        'progression': "PROGRESIÓN", 'secret_codes_title': "CÓDIGOS SECRETOS", 'secret_codes_desc': "¿Tienes un código oculto? ¡Introdúcelo para ganar XP!",
        'back': "Volver", 'campus_map': "MAPA DEL CAMPUS", 'drag_icons': "¡Arrastra los iconos por el colegio!",
        'legend': "LEYENDA", 'arcade_title': "ARCADE INTERDISCIPLINAR", 'quit': "Salir",
        'locked_chap': "Capítulo Requerido", 'validate': "VALIDAR", 'close': "Cerrar",
        'legend_unlocked': "LEYENDA DESBLOQUEADA", 'org_top': "🏅 ORGANIZADORES TOP 🏅",
        'win_msg': "¡La clase ha alcanzado el 100% de Impacto Global! Sois oficialmente los maestros de los Juegos. El comité os otorga la Insignia Definitiva.",
        'amazing': "¡INCREÍBLE!", 'journal_title': "DIARIO DE A BORDO", 'mood': "ESTADO DE ÁNIMO", 'reflection': "Reflexión...", 'photo': "FOTO", 'post': "PUBLICAR ENTRADA",
        # Pins & Alerts
        'p_start': "Salida", 'p_end': "Meta", 'p_food': "Snacks", 'p_recyc': "Reciclaje", 'p_water': "Agua", 'p_med': "Botiquín",
        'alert_profile': "¡Completa tu perfil!", 'code_used': "¡Código ya usado!", 'code_invalid': "Código inválido.",
        'validated_xp': "¡Validado! +100 XP", 'incorrect': "Incorrecto", 'end_score': "¡Fin! Puntuación: ",
        # Missions (6)
        'm1_title': "Conferencia ODS", 'm1_desc': "Creación moneda solidaria.",
        'm2_title': "Equipos Inclusivos", 'm2_desc': "Formación de equipos.",
        'm3_title': "Obstáculos Futuro", 'm3_desc': "Diseño de pruebas.",
        'm4_title': "Reglamento", 'm4_desc': "Pacto de Fair-play.",
        'm5_title': "Avituallamiento", 'm5_desc': "Snacks saludables.",
        'm6_title': "Plano Recorrido", 'm6_desc': "Trazado en el campus."
    },
    'English': {
        # Sidebar
        'tools': "Toolkit", 'tts': "🗣️ Text Reader", 'tts_help': "Type to listen.", 
        'listen': "Listen 🔊", 'mic': "🎙️ Microphone", 'mic_help': "Record.",
        'card': "🎒 Student ID", 'name': "Name:", 'trait': "Skill:", 
        'traits': ["Speed", "Strength", "Strategy", "Creativity", "Eloquence"], 'download_pdf': "📄 Download ID (+ QR)",
        'admin': "🔐 Teacher Zone", 'pass': "Password:",
        'chap_control': "Story Control", 'chap': "Chapter:", 
        'data_link': "Database Link:", 'reset': "🗑️ Delete (Test)",
        'chap_titles': {1: "Chapter 1: The Call", 2: "Chapter 2: The Team", 3: "Chapter 3: The Action", 4: "Chapter 4: The Rules", 5: "Chapter 5: Energy", 6: "Chapter 6: Glory"},
        # App UI
        'create_athlete': "CREATE YOUR ATHLETE", 'choose_champ': "CHOOSE YOUR CHAMPION",
        'name_label': "NAME", 'power_label': "SUPERPOWER", 'enter_stadium': "ENTER THE STADIUM",
        'global_impact': "GLOBAL IMPACT", 'class': "CLASS", 'obj_comm': "Common goal (SDG 17)",
        'no_team': "No team", 'missions_btn': "MISSIONS", 'map_btn': "MAP", 'journal_btn': "DIARY", 'arcade_btn': "ARCADE / TESTS",
        'oscars_btn': "VOTES & EVALUATION", 'oscars_title': "GYMKHANA CO-EVALUATION", 'vote_btn': "VOTE", 'vote_thanks': "Vote registered! +20 XP", 'already_voted': "You have already voted!", 'oscars_desc': "Evaluate the involvement and Fair-Play of other teams (SDG 17).",
        'progression': "PROGRESSION", 'secret_codes_title': "SECRET CODES", 'secret_codes_desc': "Got a hidden code? Enter it to get XP!",
        'back': "Back", 'campus_map': "CAMPUS MAP", 'drag_icons': "Drag the icons over the school!",
        'legend': "LEGEND", 'arcade_title': "INTERDISCIPLINARY ARCADE", 'quit': "Quit",
        'locked_chap': "Chapter Required", 'validate': "VALIDATE", 'close': "Close",
        'legend_unlocked': "LEGEND UNLOCKED", 'org_top': "🏅 TOP ORGANIZERS 🏅",
        'win_msg': "The class reached 100% Global Impact! You are officially the masters of the Games. The committee grants you the Ultimate Badge.",
        'amazing': "AMAZING!", 'journal_title': "LOGBOOK", 'mood': "MOOD", 'reflection': "Reflection...", 'photo': "PHOTO", 'post': "POST ENTRY",
        # Pins & Alerts
        'p_start': "Start", 'p_end': "Finish", 'p_food': "Snacks", 'p_recyc': "Recycling", 'p_water': "Water", 'p_med': "First Aid",
        'alert_profile': "Complete your profile!", 'code_used': "Code already used!", 'code_invalid': "Invalid code.",
        'validated_xp': "Validated! +100 XP", 'incorrect': "Incorrect", 'end_score': "Finished! Score: ",
        # Missions (6)
        'm1_title': "SDG Conference", 'm1_desc': "Solidarity coin creation.",
        'm2_title': "Inclusive Teams", 'm2_desc': "Team building.",
        'm3_title': "Future Obstacles", 'm3_desc': "Challenge design.",
        'm4_title': "Regulations", 'm4_desc': "Fair-play pact.",
        'm5_title': "Refreshments", 'm5_desc': "Healthy snacks.",
        'm6_title': "Route Plan", 'm6_desc': "Campus layout."
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
    
    qr = qrcode.make(f"Athlete: {name} | Specialite: {trait} | ODD: 2030")
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
            except: pass

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
        if col3.button("⏩"): st.session_state.chapter = min(6, st.session_state.chapter + 1)
        
        st.text_input(t['data_link'], "https://docs.google.com/forms/...")
        if st.button(t['reset']): st.warning("Données effacées!")
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
        .btn-outline {{ background: white; border: 2px solid #ccc; color: #555; border-radius: 10px; padding: 10px; width: 100%; font-weight: 700; margin-top: 5px; cursor: pointer; }}
        .solid-input, .solid-textarea {{ background-color: #f8f9fa; border: 2px solid #ddd; color: #333; padding: 12px; border-radius: 10px; width: 100%; font-size: 1rem; margin-bottom: 10px; font-family: var(--font-body); text-align: center; }}
        
        .avatar-grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-bottom: 20px; }}
        .avatar-item {{ background: white; border: 2px solid #ccc; border-radius: 10px; padding: 12px; text-align: center; cursor: pointer; transition: transform 0.1s; font-size: 1.5rem; color: #333; }}
        .avatar-item.selected {{ background: #e6f0ff; border-color: var(--primary); border-width: 4px; box-shadow: 0 0 10px rgba(0,102,204,0.3); transform: scale(1.1); }}
        .avatar-item.locked {{ background: #444; border-color: #222; color: #777; }}
        .avatar-item.unlocked {{ background: #FFD700; border-color: #b8860b; color: #222; box-shadow: 0 0 10px rgba(255,215,0,0.5); }}
        
        .trait-selector {{ display: flex; overflow-x: auto; padding-bottom: 10px; gap: 8px; }}
        .trait-tag {{ background: white; border: 2px solid #ccc; color: #333; padding: 8px 15px; border-radius: 20px; white-space: nowrap; cursor: pointer; font-size: 0.9rem; }}
        .trait-tag.selected {{ background: var(--accent); color: black; font-weight: 800; border-color: #e6a000; transform: scale(1.05); }}

        .home-btn {{ background-color: white; border: none; border-radius: 18px; padding: 15px 10px; text-align: center; cursor: pointer; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 100px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); transition: transform 0.2s; }}
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

        /* ESTILOS DEL DIARIO */
        .mood-btn {{ font-size: 2.5rem; background: #fff; border: 2px solid #eee; border-radius: 12px; padding: 5px; cursor: pointer; flex: 1; text-align: center; margin: 0 3px; }}
        .mood-btn.selected {{ background: #e6f0ff; border-color: var(--primary); transform: scale(1.1); }}
        .journal-entry {{ background: white; border-left: 4px solid var(--accent); padding: 15px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
        .journal-img {{ width: 100%; border-radius: 8px; margin-top: 10px; border: 1px solid #eee; }}
        .custom-file-input {{ width: 100%; padding: 10px; background: #222; color: white; border-radius: 8px; cursor: pointer; margin-bottom: 10px; }}

        /* ESTRELLA DORADA FINAL */
        #golden-star {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 4rem; text-shadow: 0 0 20px #FFD700; cursor: pointer; z-index: 100; display: none; animation: pulse-star 1.5s infinite; }}
        @keyframes pulse-star {{ 0% {{ transform: translate(-50%, -50%) scale(1); }} 50% {{ transform: translate(-50%, -50%) scale(1.3); }} 100% {{ transform: translate(-50%, -50%) scale(1); }} }}
        
        /* MODAL */
        .custom-modal {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 2000; justify-content: center; align-items: center; }}
        .custom-modal.show {{ display: flex; }}
        .modal-content-solid {{ background: white; border-radius: 15px; padding: 30px; width: 90%; max-width: 400px; text-align: center; color: #333; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }}
    </style>
</head>
<body>

    <section id="view-home" class="view active-view">
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
            <div class="d-flex justify-content-between align-items-end"><h6 class="mb-0 fw-bold text-dark"><i class="fa-solid fa-earth-americas text-primary me-2"></i> {t['global_impact']}</h6><small class="text-danger fw-bold">{t['class']}</small></div>
            <div class="progress-bar-bg"><div class="fill-global"></div></div>
            <small class="text-secondary" style="font-size: 0.7rem;">{t['obj_comm']}</small>
        </div>

        <div class="row g-2">
            <div class="col-6"><div class="home-btn" onclick="app.nav('dashboard', 'nav-dash')"><i class="fa-solid fa-list-check text-dark mb-1"></i><h5 class="mb-0 fw-bold">{t['missions_btn']}</h5></div></div>
            <div class="col-6"><div class="home-btn" onclick="app.nav('map', 'nav-map')"><i class="fa-solid fa-map-location-dot text-success mb-1"></i><h5 class="mb-0 fw-bold">{t['map_btn']}</h5></div></div>
            <div class="col-6"><div class="home-btn" onclick="app.nav('journal', 'nav-journal')"><i class="fa-solid fa-book-open text-info mb-1"></i><h5 class="mb-0 fw-bold">{t['journal_btn']}</h5></div></div>
            <div class="col-6"><div class="home-btn" onclick="app.nav('games', 'nav-games')"><i class="fa-solid fa-gamepad text-primary mb-1"></i><h5 class="mb-0 fw-bold">{t['arcade_btn']}</h5></div></div>
            <div class="col-12"><div class="home-btn flex-row gap-3 py-3" style="min-height: auto; background: linear-gradient(135deg, #fff3e0, #ffe0b2);" onclick="app.nav('oscars', 'nav-oscars')"><i class="fa-solid fa-award text-warning mb-0"></i><h5 class="mb-0 fw-bold">{t['oscars_btn']}</h5></div></div>
        </div>
    </section>

    <section id="view-avatar" class="view">
        <div class="text-center mt-4 mb-4"><h2 style="font-family: var(--font-head); font-weight: 900; color: #222;">{t['create_athlete']}</h2><p class="text-secondary small">{t['choose_champ']}</p></div>
        <div class="avatar-grid" id="sprite-container"></div>
        <div class="solid-panel mt-4">
            <label class="small text-secondary mb-2 d-block text-start">{t['name_label']}</label>
            <input type="text" id="player-name" class="solid-input" placeholder="Pseudo...">
            <label class="small text-secondary mb-2 d-block text-start mt-3">{t['power_label']}</label>
            <div class="trait-selector" id="trait-container"></div>
            <input type="hidden" id="selected-trait">
        </div>
        <button onclick="app.saveProfile()" class="btn-solid mt-2">{t['enter_stadium']} <i class="fa-solid fa-person-running"></i></button>
    </section>

    <section id="view-dashboard" class="view">
        <h4 class="fw-bold mb-3 text-dark">{t['progression']}</h4>
        <div id="missions-list"></div>
        
        <div class="secret-box">
            <h6 class="fw-bold text-dark"><i class="fa-solid fa-user-secret text-danger"></i> {t['secret_codes_title']}</h6>
            <p class="small text-secondary mb-2">{t['secret_codes_desc']}</p>
            <div class="d-flex gap-2">
                <input type="text" id="secret-code-input" class="solid-input mb-0" placeholder="CODE...">
                <button class="btn btn-dark" style="border-radius: 8px; font-weight:bold;" onclick="app.checkSecretCode()">GO</button>
            </div>
            <div id="secret-msg" class="small mt-2 fw-bold"></div>
        </div>
        <button onclick="app.nav('home')" class="btn btn-outline text-secondary w-100 mt-3">{t['back']}</button>
    </section>

    <section id="view-oscars" class="view">
        <h4 class="fw-bold mb-3 text-dark">{t['oscars_title']}</h4>
        <p class="small text-secondary mb-3">{t['oscars_desc']}</p>
        <div id="nominees-list"></div>
        <button onclick="app.nav('home')" class="btn btn-outline w-100 mt-3">{t['back']}</button>
    </section>

    <section id="view-map" class="view">
        <h4 class="fw-bold mb-3 text-dark">{t['campus_map']}</h4>
        <div class="map-container" id="map-area">
            <iframe class="map-frame" src="https://maps.google.com/maps?q=38.9763185,-3.9443803&t=k&z=19&ie=UTF8&iwloc=&output=embed" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"></iframe>
            <div class="map-overlay" ondrop="app.drop(event)" ondragover="app.allowDrop(event)">
                <div id="pin1" class="map-pin pin-pulse" draggable="true" ondragstart="app.drag(event)" style="top: 10%; left: 10%; background:#FFD93D;">🚀</div>
                <div id="pin2" class="map-pin" draggable="true" ondragstart="app.drag(event)" style="top: 10%; left: 30%; background:#FF6B6B;">🏁</div>
                <div id="pin3" class="map-pin" draggable="true" ondragstart="app.drag(event)" style="top: 10%; left: 50%; background:#4D79FF;">🍎</div>
                <div id="pin4" class="map-pin" draggable="true" ondragstart="app.drag(event)" style="top: 10%; left: 70%; background:#28a745;">♻️</div>
                <div id="pin5" class="map-pin" draggable="true" ondragstart="app.drag(event)" style="top: 30%; left: 10%; background:#17a2b8;">💧</div>
                <div id="pin6" class="map-pin" draggable="true" ondragstart="app.drag(event)" style="top: 30%; left: 30%; background:#e83e8c;">🏥</div>
                <div id="golden-star" onclick="app.claimUltimateReward()">🌟</div>
            </div>
            <div class="map-hud">
                <h6 class="text-dark mb-2 fw-bold" style="font-size: 0.85rem;"><i class="fa-solid fa-hand-pointer text-primary"></i> {t['legend']}</h6>
                <div class="row g-1 small text-dark" style="font-size: 0.7rem; font-weight: bold;">
                    <div class="col-4">🚀 {t['p_start']}</div> <div class="col-4">🏁 {t['p_end']}</div> <div class="col-4">🍎 {t['p_food']}</div>
                    <div class="col-4">♻️ {t['p_recyc']}</div> <div class="col-4">💧 {t['p_water']}</div> <div class="col-4">🏥 {t['p_med']}</div>
                </div>
            </div>
        </div>
        <button onclick="app.nav('home')" class="btn btn-outline w-100 mt-3">{t['back']}</button>
    </section>

    <section id="view-journal" class="view">
        <h4 class="fw-bold mb-3 text-dark">{t['journal_title']}</h4>
        <div class="solid-panel">
            <label class="small text-secondary mb-2">{t['mood']}</label>
            <div class="d-flex justify-content-between mb-3">
                <div class="mood-btn" onclick="app.selectMood(this, '🤩')">🤩</div>
                <div class="mood-btn" onclick="app.selectMood(this, '🙂')">🙂</div>
                <div class="mood-btn" onclick="app.selectMood(this, '😐')">😐</div>
                <div class="mood-btn" onclick="app.selectMood(this, '🥱')">🥱</div>
            </div>
            <input type="hidden" id="selected-mood">
            <textarea id="journal-text" class="solid-textarea mt-2" rows="2" placeholder="{t['reflection']}"></textarea>
            <label class="small text-secondary mb-2 mt-2">{t['photo']}</label>
            <input type="file" id="journal-photo" class="custom-file-input" accept="image/*">
            <button onclick="app.saveJournal()" class="btn-solid">{t['post']}</button>
        </div>
        <div id="journal-feed" class="mt-4"></div>
        <button onclick="app.nav('home')" class="btn btn-outline w-100 mt-3">{t['back']}</button>
    </section>

    <section id="view-games" class="view">
        <h4 class="fw-bold mb-3 text-dark">{t['arcade_title']}</h4>
        <div id="game-menu">
            <div class="row g-2">
                <div class="col-6"><div class="solid-panel p-3 mb-2 text-center" onclick="app.startGame('num')"><i class="fa-solid fa-calculator fa-2x text-primary mb-2"></i><br><h6 class="mb-0 text-dark fw-bold small">NOMBRES</h6></div></div>
                <div class="col-6"><div class="solid-panel p-3 mb-2 text-center" onclick="app.startGame('fut')"><i class="fa-solid fa-rocket fa-2x text-warning mb-2"></i><br><h6 class="mb-0 text-dark fw-bold small">FUTUR</h6></div></div>
                <div class="col-6"><div class="solid-panel p-3 mb-2 text-center" onclick="app.startGame('part')"><i class="fa-solid fa-pizza-slice fa-2x text-danger mb-2"></i><br><h6 class="mb-0 text-dark fw-bold small">PARTITIFS</h6></div></div>
                <div class="col-6"><div class="solid-panel p-3 mb-2 text-center" onclick="app.startGame('sport')"><i class="fa-solid fa-person-running fa-2x text-success mb-2"></i><br><h6 class="mb-0 text-dark fw-bold small">SPORT</h6></div></div>
                <div class="col-6"><div class="solid-panel p-3 mb-2 text-center" onclick="app.startGame('imp')"><i class="fa-solid fa-bullhorn fa-2x text-info mb-2"></i><br><h6 class="mb-0 text-dark fw-bold small">IMPÉRATIF</h6></div></div>
                <div class="col-6"><div class="solid-panel p-3 mb-2 text-center" onclick="app.startGame('odd')"><i class="fa-solid fa-earth-europe fa-2x text-primary mb-2"></i><br><h6 class="mb-0 text-dark fw-bold small">QUIZ ODD</h6></div></div>
                <div class="col-6"><div class="solid-panel p-3 mb-2 text-center" onclick="app.startGame('bio')"><i class="fa-solid fa-leaf fa-2x text-success mb-2"></i><br><h6 class="mb-0 text-dark fw-bold small">SVT (ODD)</h6></div></div>
                <div class="col-6"><div class="solid-panel p-3 mb-2 text-center" onclick="app.startGame('geo')"><i class="fa-solid fa-globe fa-2x text-info mb-2"></i><br><h6 class="mb-0 text-dark fw-bold small">GÉO & HIST</h6></div></div>
                <div class="col-6"><div class="solid-panel p-3 mb-2 text-center" onclick="app.startGame('math')"><i class="fa-solid fa-square-root-variable fa-2x text-secondary mb-2"></i><br><h6 class="mb-0 text-dark fw-bold small">MATHS</h6></div></div>
                <div class="col-6"><div class="solid-panel p-3 mb-2 text-center" onclick="app.startGame('fra')"><i class="fa-solid fa-comment-dots fa-2x text-danger mb-2"></i><br><h6 class="mb-0 text-dark fw-bold small">FRANÇAIS</h6></div></div>
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
            <button onclick="app.exitGame()" class="btn btn-outline w-100">{t['quit']}</button>
        </div>
    </section>

    <div id="app-dock" class="dock-nav" style="display:none;">
        <div id="nav-home" class="dock-item active" onclick="app.nav('home', this)"><i class="fa-solid fa-house"></i></div>
        <div id="nav-dash" class="dock-item" onclick="app.nav('dashboard', this)"><i class="fa-solid fa-list-check"></i></div>
        <div id="nav-map" class="dock-item" onclick="app.nav('map', this)"><i class="fa-solid fa-map"></i></div>
        <div id="nav-journal" class="dock-item" onclick="app.nav('journal', this)"><i class="fa-solid fa-book-open"></i></div>
        <div id="nav-games" class="dock-item" onclick="app.nav('games', this)"><i class="fa-solid fa-gamepad"></i></div>
    </div>

    <div id="customModal" class="custom-modal">
        <div class="modal-content-solid">
            <h4 id="modal-title" class="fw-bold mb-2">...</h4>
            <div class="badge bg-warning text-dark mb-2" id="modal-odd">ODD</div>
            <p id="modal-desc" class="text-secondary small mb-4">...</p>
            <input type="text" id="user-input" class="solid-input text-uppercase" placeholder="CODE">
            <button onclick="app.validate()" class="btn-solid mb-2">{t['validate']}</button>
            <button onclick="app.closeModal()" class="btn btn-link text-secondary text-decoration-none">{t['close']}</button>
            <div id="feedback-msg" class="mt-3 small fw-bold"></div>
        </div>
    </div>
    
    <div id="ultimateModal" class="custom-modal">
        <div class="modal-content-solid" style="border: 4px solid #FFD700; background: linear-gradient(135deg, #fff 0%, #fff8dc 100%);">
            <i class="fa-solid fa-crown fa-4x mb-3" style="color: #FFD700; text-shadow: 0 4px 10px rgba(255,215,0,0.5);"></i>
            <h2 class="fw-bold text-dark">{t['legend_unlocked']}</h2>
            <h4 class="fw-bold text-danger mb-3">{t['org_top']}</h4>
            <p class="text-secondary small mb-4">{t['win_msg']}</p>
            <button onclick="document.getElementById('ultimateModal').classList.remove('show')" class="btn-solid mb-2" style="background:#FFD700; color:#000; border:2px solid #b8860b;">{t['amazing']}</button>
        </div>
    </div>

    <script>
        // 23 AVATARES NORMALES
        const SPRITES = [
            "fa-dragon", "fa-ghost", "fa-robot", "fa-cat", "fa-bolt", "fa-fire", "fa-snowflake", "fa-leaf",
            "fa-crow", "fa-spider", "fa-fish", "fa-bug", "fa-hippo", "fa-otter", "fa-frog", "fa-horse",
            "fa-dove", "fa-dog", "fa-kiwi-bird", "fa-worm", "fa-locust", "fa-mosquito", "fa-meteor"
        ];
        
        // 7 AVATARES OCULTOS
        const HIDDEN_SPRITES = [
            {{ icon: "fa-crown", code: "NOVA-33" }}, {{ icon: "fa-user-astronaut", code: "TITAN-8X" }}, 
            {{ icon: "fa-jedi", code: "NEXUS-V" }}, {{ icon: "fa-user-ninja", code: "PHOENIX-9" }}, 
            {{ icon: "fa-mask", code: "SPARK-44" }}, {{ icon: "fa-hat-wizard", code: "AURA-77" }}, 
            {{ icon: "fa-gem", code: "ECHO-LUM" }}
        ];

        const TRAITS = ["{t['traits'][0]}", "{t['traits'][1]}", "{t['traits'][2]}", "{t['traits'][3]}", "{t['traits'][4]}"];

        const SECRET_CODES = {{
            "RELAIS-100": {{ xp: 100, msg: "+100 XP (Bonus)" }},
            "BIOS-50": {{ xp: 50, msg: "+50 XP (SVT)" }},
            "ATLAS-50": {{ xp: 50, msg: "+50 XP (GÉO)" }},
            "MATH-50": {{ xp: 50, msg: "+50 XP (MATHS)" }}
        }};

        let DATA = {{
            user: {{ sprite: "", name: "", trait: "", xp: 0, usedCodes: [], unlockedAvatars: [], myVote: "" }},
            teamName: "",
            missions: [
                {{ id: 1, type: "code", code: "ODD-74A", title: "{t['m1_title']}", odd: "ODD 1-17", icon: "fa-coins", desc: "{t['m1_desc']}", completed: false }},
                {{ id: 2, type: "code", code: "EQ-92B", title: "{t['m2_title']}", odd: "ODD 5 & 10", icon: "fa-users", desc: "{t['m2_desc']}", completed: false }},
                {{ id: 3, type: "code", code: "ECO-18C", title: "{t['m3_title']}", odd: "ODD 13", icon: "fa-recycle", desc: "{t['m3_desc']}", completed: false }},
                {{ id: 4, type: "code", code: "REG-44D", title: "{t['m4_title']}", odd: "ODD 16", icon: "fa-scale-balanced", desc: "{t['m4_desc']}", completed: false }},
                {{ id: 5, type: "code", code: "MIAM-66E", title: "{t['m5_title']}", odd: "ODD 3", icon: "fa-apple-whole", desc: "{t['m5_desc']}", completed: false }},
                {{ id: 6, type: "code", code: "MAP-31F", title: "{t['m6_title']}", odd: "ODD 11", icon: "fa-map", desc: "{t['m6_desc']}", completed: false }}
            ],
            journal: [],
            currentId: null
        }};

        const QUIZ = {{
            num: [{{ q: "10 stylos = 20€. 1 stylo = ?", a: ["2€", "5€", "1€"], c: 0 }}, {{ q: "90 + 9 = ?", a: ["99", "89", "19"], c: 0 }}],
            fut: [{{ q: "Demain je ___ (manger)", a: ["mangerai", "mangerais", "mange"], c: 0 }}, {{ q: "Nous ___ (finir)", a: ["finirons", "finissons", "finiront"], c: 0 }}],
            part: [{{ q: "Je veux ___ eau", a: ["de l'", "du", "de la"], c: 0 }}, {{ q: "Il mange ___ pain", a: ["du", "de la", "des"], c: 0 }}],
            sport: [{{ q: "Le sport dans l'eau ?", a: ["Natation", "Judo", "Tennis"], c: 0 }}, {{ q: "Pour courir il faut des...", a: ["Baskets", "Gants", "Lunettes"], c: 0 }}],
            imp: [{{ q: "(Courir) ___ vite !", a: ["Cours", "Coures", "Courir"], c: 0 }}, {{ q: "(Arrêter) ___ de parler !", a: ["Arrêtez", "Arrêter", "Arrêtes"], c: 0 }}],
            odd: [{{ q: "ODD 13 c'est pour...", a: ["Le Climat", "La Faim", "L'Eau"], c: 0 }}, {{ q: "ODD 5 c'est...", a: ["Égalité", "Santé", "Villes"], c: 0 }}],
            bio: [{{ q: "Où jeter une bouteille en plastique ? (ODD 12)", a: ["Poubelle Jaune", "Poubelle Verte", "Poubelle Bleue"], c: 0 }}, {{ q: "Quel gaz cause l'effet de serre ? (ODD 13)", a: ["Le CO2", "L'Oxygène", "L'Azote"], c: 0 }}],
            geo: [{{ q: "Où sont nés les Jeux Olympiques ?", a: ["En Grèce", "En France", "En Italie"], c: 0 }}, {{ q: "Combien d'anneaux sur le drapeau olympique ?", a: ["5", "6", "4"], c: 0 }}],
            math: [{{ q: "Un athlète court 100m en 10s. Vitesse ?", a: ["10 m/s", "100 m/s", "1 m/s"], c: 0 }}, {{ q: "Si un terrain fait 50m x 20m, quelle est l'aire ?", a: ["1000 m²", "100 m²", "500 m²"], c: 0 }}],
            fra: [{{ q: "Il faut que nous _____ (participer).", a: ["participions", "participons", "participerons"], c: 0 }}, {{ q: "Trouve le synonyme de 'Gagner'", a: ["Remporter", "Perdre", "Échouer"], c: 0 }}]
        }};
        
        let currentQuiz = [], qIndex = 0, score = 0;

        const app = {{
            nominees: ["Les Titans", "Eco-Warriors", "Cyber-Français", "Green Team"], // Nombres ficticios para la demo
            
            init: () => {{
                const savedData = localStorage.getItem("jo_avenir_data");
                if(savedData) DATA = JSON.parse(savedData);
                if(!DATA.user.usedCodes) DATA.user.usedCodes = [];
                if(!DATA.user.unlockedAvatars) DATA.user.unlockedAvatars = [];
                if(!DATA.user.myVote) DATA.user.myVote = "";
                if(!DATA.journal) DATA.journal = [];
                
                if (DATA.missions.length >= 6) {{
                    DATA.missions[0].title = "{t['m1_title']}"; DATA.missions[0].desc = "{t['m1_desc']}";
                    DATA.missions[1].title = "{t['m2_title']}"; DATA.missions[1].desc = "{t['m2_desc']}";
                    DATA.missions[2].title = "{t['m3_title']}"; DATA.missions[2].desc = "{t['m3_desc']}";
                    DATA.missions[3].title = "{t['m4_title']}"; DATA.missions[3].desc = "{t['m4_desc']}";
                    DATA.missions[4].title = "{t['m5_title']}"; DATA.missions[4].desc = "{t['m5_desc']}";
                    DATA.missions[5].title = "{t['m6_title']}"; DATA.missions[5].desc = "{t['m6_desc']}";
                }}

                app.renderAvatars();

                const tCont = document.getElementById('trait-container');
                tCont.innerHTML = "";
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
            
            renderAvatars: () => {{
                const grid = document.getElementById('sprite-container');
                grid.innerHTML = "";
                
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
                
                HIDDEN_SPRITES.forEach(h_sprite => {{
                    const div = document.createElement('div');
                    if (DATA.user.unlockedAvatars.includes(h_sprite.icon)) {{
                        div.className = "avatar-item unlocked";
                        if(DATA.user.sprite === h_sprite.icon) div.classList.add('selected');
                        div.innerHTML = `<i class="fa-solid ${{h_sprite.icon}}"></i>`;
                        div.onclick = function() {{
                            document.querySelectorAll('.avatar-item').forEach(el => el.classList.remove('selected'));
                            this.classList.add('selected');
                            DATA.user.sprite = h_sprite.icon;
                        }};
                    }} else {{
                        div.className = "avatar-item locked";
                        div.innerHTML = `<i class="fa-solid fa-lock"></i>`;
                        div.onclick = function() {{
                            const guess = prompt("Code secret:");
                            if (guess && guess.trim().toUpperCase() === h_sprite.code) {{
                                DATA.user.unlockedAvatars.push(h_sprite.icon);
                                app.saveData();
                                app.renderAvatars();
                                confetti();
                            }} else if (guess) {{
                                alert("{t['code_invalid']}");
                            }}
                        }};
                    }}
                    grid.appendChild(div);
                }});
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
                    msgBox.innerText = "{t['code_used']}"; msgBox.style.color = "#dc3545"; return;
                }}
                if(SECRET_CODES[input]) {{
                    DATA.user.usedCodes.push(input);
                    app.addXP(SECRET_CODES[input].xp);
                    msgBox.innerText = SECRET_CODES[input].msg; msgBox.style.color = "#28a745";
                    document.getElementById('secret-code-input').value = "";
                }} else {{
                    msgBox.innerText = "{t['code_invalid']}"; msgBox.style.color = "#dc3545";
                }}
            }},

            claimUltimateReward: () => {{
                confetti({{ particleCount: 300, spread: 160, origin: {{ y: 0.4 }} }});
                document.getElementById('golden-star').style.display = 'none'; 
                document.getElementById('ultimateModal').classList.add('show');
            }},

            saveProfile: () => {{
                const name = document.getElementById('player-name').value;
                if(!DATA.user.sprite || !name || !DATA.user.trait) return alert("{t['alert_profile']}");
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
                if(viewName === 'journal') {{ app.renderJournal(); }}
                if(viewName === 'oscars') {{ app.renderNominees(); }}
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
                const currentChapter = {st.session_state.chapter};
                
                DATA.missions.forEach((m, idx) => {{
                    const reqChapter = idx + 1; 
                    if (currentChapter >= reqChapter) {{
                        const status = m.completed ? 'completed' : '';
                        const iconCheck = m.completed ? 'fa-check text-success' : 'fa-play text-primary';
                        list.innerHTML += `<div class="solid-panel phase-card d-flex align-items-center ${{status}}" onclick="app.openModal(${{m.id}})"><div class="me-3 text-center" style="width: 40px;"><i class="fa-solid ${{m.icon}} fa-xl text-secondary"></i></div><div class="flex-grow-1"><span class="odd-badge">${{m.odd}}</span><h6 class="mb-0 fw-bold text-dark">${{m.title}}</h6></div><i class="fa-solid ${{iconCheck}}"></i></div>`;
                    }} else {{
                        list.innerHTML += `<div class="solid-panel phase-card d-flex align-items-center locked" style="opacity: 0.6; cursor:not-allowed; background:#f0f0f0;"><div class="me-3 text-center" style="width: 40px;"><i class="fa-solid fa-lock fa-xl text-secondary"></i></div><div class="flex-grow-1"><span class="odd-badge bg-secondary text-light">???</span><h6 class="mb-0 fw-bold text-secondary">{t['locked_chap']} ${{reqChapter}}</h6></div></div>`;
                    }}
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
                    m.completed = true; document.getElementById('feedback-msg').innerText = "{t['validated_xp']}"; document.getElementById('feedback-msg').style.color = "#28a745"; 
                    app.addXP(100);
                    setTimeout(() => {{ app.closeModal(); app.renderList(); }}, 1200);
                }} else {{ document.getElementById('feedback-msg').innerText = "{t['incorrect']}"; document.getElementById('feedback-msg').style.color = "#dc3545"; }}
            }},
            
            // --- LÓGICA DE VOTACIONES (COEVALUACIÓN) ---
            renderNominees: () => {{
                const list = document.getElementById('nominees-list');
                list.innerHTML = "";
                app.nominees.forEach(n => {{
                    // No permitir votarse a sí mismos
                    if(n !== DATA.teamName) {{
                        list.innerHTML += `<div class='solid-panel d-flex justify-content-between align-items-center mb-2'>
                            <span class="fw-bold text-dark">${{n}}</span>
                            <button class='btn btn-warning fw-bold' style='border-radius:8px;' onclick='app.submitVote("${{n}}")'>{t['vote_btn']}</button>
                        </div>`;
                    }}
                }});
            }},
            submitVote: (name) => {{
                if(DATA.user.myVote && DATA.user.myVote !== "") {{
                    alert("{t['already_voted']}");
                    return;
                }}
                if(confirm("Voter pour " + name + " ?")) {{
                    DATA.user.myVote = name;
                    app.addXP(20);
                    app.saveData();
                    app.renderNominees();
                    alert("{t['vote_thanks']}");
                }}
            }},

            selectMood: (e,m) => {{ document.querySelectorAll('.mood-btn').forEach(b=>b.classList.remove('selected')); e.classList.add('selected'); document.getElementById('selected-mood').value=m; }},
            saveJournal: () => {{ 
                const m=document.getElementById('selected-mood').value, t=document.getElementById('journal-text').value, f=document.getElementById('journal-photo'); 
                if(!m||!t) return alert("{t['alert_profile']}"); 
                const e={{d:new Date().toLocaleDateString(), m, t, i:null}}; 
                if(f.files && f.files[0]){{ 
                    const r=new FileReader(); 
                    r.onload=(ev)=>{{e.i=ev.target.result; DATA.journal.unshift(e); app.addXP(20); app.saveData(); app.renderJournal();}}; 
                    r.readAsDataURL(f.files[0]); 
                }} else {{ DATA.journal.unshift(e); app.addXP(20); app.saveData(); app.renderJournal(); }} 
                document.getElementById('journal-text').value=""; 
                document.querySelectorAll('.mood-btn').forEach(b=>b.classList.remove('selected'));
                document.getElementById('selected-mood').value="";
            }},
            renderJournal: () => {{ const c=document.getElementById('journal-feed'); c.innerHTML=""; if(!DATA.journal) DATA.journal=[]; DATA.journal.forEach(e=>{{ c.innerHTML+=`<div class='journal-entry'><div class='d-flex justify-content-between'><span>${{e.d}}</span><span>${{e.m}}</span></div><p class='text-dark'>${{e.t}}</p>${{e.i?`<img src='${{e.i}}' class='journal-img'>`:''}}</div>`}}); }},

            speakText: (text) => {{ window.speechSynthesis.cancel(); const msg = new SpeechSynthesisUtterance(); msg.text = text; msg.lang = 'fr-FR'; window.speechSynthesis.speak(msg); }},
            speakQuestion: () => {{ app.speakText(document.getElementById('game-question').innerText); }},
            startGame: (t) => {{ currentQuiz = QUIZ[t]; qIndex=0; score=0; document.getElementById('game-menu').style.display='none'; document.getElementById('game-interface').style.display='block'; app.renderQuestion(); }},
            renderQuestion: () => {{ if(qIndex>=currentQuiz.length){{ alert("{t['end_score']}"+score); app.addXP(score); app.exitGame(); return;}} const q=currentQuiz[qIndex]; document.getElementById('game-question').innerText=q.q; const o=document.getElementById('game-options'); o.innerHTML=""; q.a.forEach((ans,i)=>{{ o.innerHTML+=`<div class='game-opt' onclick='app.checkAnswer(${{i}})'>${{ans}}</div>`}}); }},
            checkAnswer: (i) => {{ app.speakText(currentQuiz[qIndex].a[i]); if(i===currentQuiz[qIndex].c){{score+=10; confetti();}} setTimeout(()=>{{qIndex++; app.renderQuestion()}}, 1200); }},
            exitGame: () => {{ document.getElementById('game-interface').style.display='none'; document.getElementById('game-menu').style.display='block'; }}
        }};
        
        app.init();
    </script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=True)
