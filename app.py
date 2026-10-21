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
# LA BARRA AHORA ESTÁ OCULTA POR DEFECTO PARA LOS ALUMNOS ("collapsed")
st.set_page_config(page_title="J.O. De l'Avenir", layout="wide", initial_sidebar_state="collapsed", page_icon="🏅")

if 'lang' not in st.session_state: st.session_state.lang = 'Français'
if 'chapter' not in st.session_state: st.session_state.chapter = 1

translations = {
    'Français': {
        'tools': "Boîte à Outils", 'tts': "🗣️ Lecteur (TTS)", 'mic': "🎙️ Micro",
        'card': "🎒 Carte Élève", 'name': "Ton Nom:", 'trait': "Atout:", 
        'traits': ["Vitesse", "Force", "Stratégie", "Créativité", "Éloquence"], 'download_pdf': "📄 Ma Carte", 'download_diploma': "🎓 Diplôme",
        'admin': "🔐 Zone Prof", 'pass': "Mot de passe:", 'chap_control': "Contrôle Chapitres",
        'chap_titles': {1: "Chap. 1: L'Appel", 2: "Chap. 2: L'Équipe", 3: "Chap. 3: L'Action", 4: "Chap. 4: Les Règles", 5: "Chap. 5: L'Énergie", 6: "Chap. 6: La Gloire"},
        'create_athlete': "CRÉEZ VOTRE ATHLÈTE", 'choose_champ': "CHOISISSEZ VOTRE CHAMPION",
        'name_label': "NOM", 'enter_stadium': "ENTRER DANS LE STADE",
        'profil_btn': "MON PROFIL", 'missions_btn': "MISSIONS", 'map_btn': "PLAN", 'journal_btn': "JOURNAL", 'arcade_btn': "ARCADE", 'oscars_btn': "ÉVALUATION",
        'global_impact': "IMPACT GLOBAL", 'personal_impact': "MON IMPACT PERSONNEL", 'class': "CLASSE", 'obj_comm': "Objectif commun (ODD 17)",
        'progression': "ROAD TO PARIS", 'secret_codes_title': "CODES SECRETS", 'secret_codes_desc': "As-tu un code caché ? (ex: MATH-50)",
        'back': "Retour", 'campus_map': "PLAN DU CAMPUS", 'legend': "LÉGENDE", 'arcade_title': "ARCADE INTERDISCIPLINAIRE", 'quit': "Quitter",
        'locked_chap': "Chapitre Requis", 'validate': "VALIDER", 'close': "Fermer", 'post': "POSTER L'ENTRÉE", 'vote_btn': "VOTER",
        'legend_unlocked': "LÉGENDE DÉBLOQUÉE", 'org_top': "🏅 ORGANISATEURS TOP 🏅", 'win_msg': "La classe a atteint 100% d'Impact Global !", 'amazing': "INCROYABLE !",
        'journal_title': "JOURNAL DE BORD", 'mood': "HUMEUR", 'reflection': "Réflexion...", 'photo': "PHOTO", 'oscars_title': "CO-ÉVALUATION GYMKHANA",
        'vote_thanks': "Vote enregistré ! +20 XP", 'already_voted': "Vous avez déjà voté !", 'alert_profile': "Complétez votre profil !", 
        'code_used': "Code déjà utilisé !", 'code_invalid': "Code invalide.", 'validated_xp': "Validé ! +100 XP", 'incorrect': "Incorrect", 
        'end_score': "Fin! Score: ", 'next': "Suivant", 'correct': "Correct!", 'p_start': "Départ", 'p_end': "Arrivée", 'p_food': "Ravito", 
        'p_recyc': "Recyclage", 'p_water': "Eau", 'p_med': "Secours", 'analytics_title': "📊 Learning Analytics",
        'm1_title': "Conférence ODD", 'm1_desc': "Création monnaie solidaire.", 'm2_title': "Équipes Inclusives", 'm2_desc': "Création des équipes.", 
        'm3_title': "Obstacles Avenir", 'm3_desc': "Design d'épreuves.", 'm4_title': "Règlement", 'm4_desc': "Pacte de Fair-play.", 
        'm5_title': "Ravitaillement", 'm5_desc': "Snacks sains.", 'm6_title': "Plan Parcours", 'm6_desc': "Tracé sur le campus."
    },
    'Español': {
        'tools': "Herramientas", 'tts': "🗣️ Lector (TTS)", 'mic': "🎙️ Micrófono",
        'card': "🎒 Carnet Alumno", 'name': "Nombre:", 'trait': "Habilidad:", 
        'traits': ["Velocidad", "Fuerza", "Estrategia", "Creatividad", "Elocuencia"], 'download_pdf': "📄 Mi Carnet", 'download_diploma': "🎓 Diploma",
        'admin': "🔐 Zona Profesor", 'pass': "Contraseña:", 'chap_control': "Control Capítulos",
        'chap_titles': {1: "Cap. 1: La Llamada", 2: "Cap. 2: El Equipo", 3: "Cap. 3: La Acción", 4: "Cap. 4: Las Reglas", 5: "Cap. 5: La Energía", 6: "Cap. 6: La Gloria"},
        'create_athlete': "CREA TU ATLETA", 'choose_champ': "ELIGE TU CAMPEÓN",
        'name_label': "NOMBRE", 'enter_stadium': "ENTRAR AL ESTADIO",
        'profil_btn': "MI PERFIL", 'missions_btn': "MISIONES", 'map_btn': "MAPA", 'journal_btn': "DIARIO", 'arcade_btn': "ARCADE", 'oscars_btn': "EVALUACIÓN",
        'global_impact': "IMPACTO GLOBAL", 'personal_impact': "MI IMPACTO PERSONAL", 'class': "CLASE", 'obj_comm': "Objetivo común (ODS 17)",
        'progression': "ROAD TO PARIS", 'secret_codes_title': "CÓDIGOS SECRETOS", 'secret_codes_desc': "¿Tienes un código oculto? (ej: MATH-50)",
        'back': "Volver", 'campus_map': "MAPA DEL CAMPUS", 'legend': "LEYENDA", 'arcade_title': "ARCADE INTERDISCIPLINAR", 'quit': "Salir",
        'locked_chap': "Capítulo Requerido", 'validate': "VALIDAR", 'close': "Cerrar", 'post': "PUBLICAR ENTRADA", 'vote_btn': "VOTAR",
        'legend_unlocked': "LEYENDA DESBLOQUEADA", 'org_top': "🏅 ORGANIZADORES TOP 🏅", 'win_msg': "¡La clase ha alcanzado el 100% de Impacto Global!", 'amazing': "¡INCREÍBLE!",
        'journal_title': "DIARIO DE A BORDO", 'mood': "ESTADO DE ÁNIMO", 'reflection': "Reflexión...", 'photo': "FOTO", 'oscars_title': "COEVALUACIÓN GYMKHANA",
        'vote_thanks': "¡Voto registrado! +20 XP", 'already_voted': "¡Ya has votado!", 'alert_profile': "¡Completa tu perfil!", 
        'code_used': "¡Código ya usado!", 'code_invalid': "Código inválido.", 'validated_xp': "¡Validado! +100 XP", 'incorrect': "Incorrecto", 
        'end_score': "¡Fin! Puntuación: ", 'next': "Siguiente", 'correct': "¡Correcto!", 'p_start': "Salida", 'p_end': "Meta", 'p_food': "Snacks", 
        'p_recyc': "Reciclaje", 'p_water': "Agua", 'p_med': "Botiquín", 'analytics_title': "📊 Learning Analytics",
        'm1_title': "Conferencia ODS", 'm1_desc': "Creación moneda.", 'm2_title': "Equipos Inclusivos", 'm2_desc': "Formación de equipos.", 
        'm3_title': "Obstáculos Futuro", 'm3_desc': "Diseño de pruebas.", 'm4_title': "Reglamento", 'm4_desc': "Pacto Fair-play.", 
        'm5_title': "Avituallamiento", 'm5_desc': "Snacks saludables.", 'm6_title': "Plano Recorrido", 'm6_desc': "Trazado en campus."
    }
}
t = translations.get(st.session_state.lang, translations['Français'])
dynamic_title = t['chap_titles'][st.session_state.chapter]

def get_tts_lang(lang_choice):
    return 'es' if lang_choice == 'Español' else 'fr'

# ==========================================================
# 2. BACKEND Y GENERADORES DE PDF (PYTHON)
# ==========================================================
FIREBASE_CONFIG = "/* Omitido en demo local */"

def get_mock_data():
    return pd.DataFrame({'Équipe': ['Les Titans', 'Eco-Warriors'], 'Missions Validées': [5, 4], 'XP Moyen': [850, 620]})

def generate_excel(df):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Suivi')
    return buffer.getvalue()

def create_player_card(name, trait):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 28)
    pdf.cell(210, 15, "ACCRÉDITATION OFFICIELLE", 0, 1, 'C')
    pdf.set_font("Arial", 'B', 35)
    pdf.cell(210, 30, name.upper(), 0, 1, 'C')
    pdf.set_font("Arial", 'I', 18)
    pdf.cell(210, 15, f"Atout: {trait}", 0, 1, 'C')
    return pdf.output(dest='S').encode('latin-1')

def generate_diploma(name):
    # Generador de Diploma Apaisado (Landscape)
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_line_width(5)
    pdf.set_draw_color(255, 215, 0) # Borde Dorado
    pdf.rect(10, 10, 277, 190)
    pdf.set_font("Arial", 'B', 45)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(277, 40, "DIPLÔME D'EXCELLENCE", 0, 1, 'C')
    pdf.set_font("Arial", 'I', 20)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(277, 20, "Décerné avec honneur à :", 0, 1, 'C')
    pdf.set_font("Arial", 'B', 55)
    pdf.set_text_color(220, 20, 60)
    pdf.cell(277, 30, name.upper(), 0, 1, 'C')
    pdf.set_font("Arial", '', 16)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(277, 20, "Pour sa participation exceptionnelle, son engagement envers les ODD et le Fair-Play.", 0, 1, 'C')
    pdf.set_font("Arial", 'I', 14)
    pdf.cell(277, 20, "Projet : J.O. De l'Avenir", 0, 1, 'C')
    return pdf.output(dest='S').encode('latin-1')

def generate_analytics_report():
    # PDF Analítico para demostrar Evaluación Formativa en la Oposición
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(200, 15, "RAPPORT: LEARNING ANALYTICS (LOMLOE)", 0, 1, 'C')
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, "Taux d'erreur par categorie (Interdisciplinaire):", 0, 1, 'L')
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 8, "- Futur Simple: 68% (Action requise: Revoir les terminaisons)", 0, 1, 'L')
    pdf.cell(200, 8, "- Partitifs: 45% (Action requise: Exercices pratiques)", 0, 1, 'L')
    pdf.cell(200, 8, "- Mathematiques: 30%", 0, 1, 'L')
    pdf.cell(200, 8, "- SVT (ODD): 15%", 0, 1, 'L')
    pdf.cell(200, 8, "- Geographie: 10%", 0, 1, 'L')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(220, 20, 60)
    pdf.cell(200, 10, "Conclusion Formative : Le systeme a detecte une lacune en grammaire.", 0, 1, 'L')
    return pdf.output(dest='S').encode('latin-1')

# ==========================================================
# 3. BARRA LATERAL DEL PROFESOR Y ANALÍTICAS
# ==========================================================
with st.sidebar:
    st.selectbox("🌐 Langue / Idioma", ["Français", "Español"], key='lang')
    t = translations.get(st.session_state.lang, translations['Français'])
    
    st.title(t['tools'])
    
    with st.expander(t.get('tts', "Lecteur")):
        text_to_speak = st.text_input("", "Allez!")
        if st.button("🔊"):
            try:
                tts = gTTS(text=text_to_speak, lang=get_tts_lang(st.session_state.lang))
                audio_bytes = io.BytesIO()
                tts.write_to_fp(audio_bytes)
                st.audio(audio_bytes, format='audio/mp3')
            except Exception as e:
                st.error("Erreur TTS")

    with st.expander(t.get('mic', "Micro")):
        wav_audio_data = st_audiorec()
        if wav_audio_data is not None:
            st.audio(wav_audio_data, format='audio/wav')

    st.divider()
    
    st.markdown(f"### {t.get('card', 'Carte')}")
    player_name = st.text_input(t.get('name', 'Nom'), "Athlète")
    player_trait = st.selectbox(t.get('trait', 'Atout'), t.get('traits', []))
    
    col_pdf1, col_pdf2 = st.columns(2)
    with col_pdf1:
        if st.button("🎒 Card"):
            try:
                pdf_data = create_player_card(player_name, player_trait)
                st.download_button("📥 PDF", pdf_data, file_name="carte.pdf", mime="application/pdf")
            except: st.error("Erreur")
    with col_pdf2:
        if st.button("🎓 Diplôme"):
            try:
                diploma_data = generate_diploma(player_name)
                st.download_button("📥 PDF", diploma_data, file_name="diplome.pdf", mime="application/pdf")
            except: st.error("Erreur")

    st.divider()
    
    st.markdown(f"### {t.get('admin', 'Admin')}")
    password = st.text_input(t.get('pass', 'Mot de passe'), type="password")
    
    if password == "prof123": 
        st.success("Admin Connecté")
        
        # 1. CONTROL DE CAPÍTULOS
        col1, col2, col3 = st.columns([1,2,1])
        if col1.button("⏪"): st.session_state.chapter = max(1, st.session_state.chapter - 1)
        col2.markdown(f"<div style='text-align:center;'>{st.session_state.chapter}</div>", unsafe_allow_html=True)
        if col3.button("⏩"): st.session_state.chapter = min(6, st.session_state.chapter + 1)
        st.download_button("📥 Rapport Excel", data=generate_excel(get_mock_data()), file_name="rapport.xlsx", use_container_width=True)
        
        # 2. LEARNING ANALYTICS (GRÁFICO Y PDF)
        st.markdown("---")
        st.markdown(f"**{t['analytics_title']}**")
        analytics_data = pd.DataFrame({
            'Catégorie': ['Futur', 'Partitifs', 'Maths', 'Bio', 'Géo'],
            'Erreurs (%)': [68, 45, 30, 15, 10]
        }).set_index('Catégorie')
        st.bar_chart(analytics_data)
        
        try:
            analytics_pdf = generate_analytics_report()
            st.download_button("📊 Télécharger Rapport PDF", analytics_pdf, file_name="learning_analytics.pdf", mime="application/pdf", use_container_width=True)
        except: pass

        # 3. RESETEO DE DATOS SEGURO (Try-Catch en JS)
        st.markdown("---")
        if st.button("🗑️ Réinitialiser / Borrar Todo", type="primary", use_container_width=True):
            st.warning("⚠️ Action irréversible. Les profils actuels seront supprimés.")
            components.html("""
                <script>
                    try {
                        window.parent.localStorage.removeItem('jo_avenir_2026');
                        alert('Base de données effacée ! Rechargez la page web (F5) pour un nouveau cours.');
                    } catch(e) { console.error(e); }
                </script>
            """, height=0)

st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;} .block-container {padding:0;}</style>", unsafe_allow_html=True)

# ==========================================================
# 4. CSS (APP NATIVA Y VISTAS)
# ==========================================================
CSS_CODE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Montserrat:wght@800&display=swap');
    :root { --primary: #0066CC; --accent: #FFB100; --font-head: 'Montserrat', sans-serif; --font-body: 'Poppins', sans-serif; }
    body { background-image: url('https://images.unsplash.com/photo-1533107862482-0e6974b06ec4?q=80&w=2574&auto=format&fit=crop'); background-size: cover; background-attachment: fixed; color: #111; font-family: var(--font-body); margin: 0; padding-bottom: 90px; padding-top: 60px; overflow-x: hidden;}
    
    /* MODO ZEN */
    body.mode-zen { background-image: none !important; background-color: #FDF6E3 !important; font-family: 'Comic Sans MS', sans-serif !important; }
    body.mode-zen .glass-panel { box-shadow: none !important; border: 2px solid #ccc !important; background-color: #fff !important; backdrop-filter: none; }
    
    /* APP HEADER NATIVO */
    .app-header { position: fixed; top: 0; left: 0; width: 100%; height: 60px; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); display: flex; align-items: center; padding: 0 15px; z-index: 2000; box-shadow: 0 2px 15px rgba(0,0,0,0.1); transition: transform 0.3s; transform: translateY(-100%); }
    .app-header.visible { transform: translateY(0); }
    .back-btn { font-size: 1.5rem; color: var(--primary); cursor: pointer; border: none; background: transparent; padding: 10px; }
    .header-title { flex-grow: 1; text-align: center; font-weight: 800; font-family: var(--font-head); margin-right: 40px; text-transform: uppercase; color: #222;}

    /* GLASSMORPHISM */
    .glass-panel { background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(12px); border-radius: 20px; padding: 20px; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2); margin-bottom: 20px; }
    
    /* VISTAS Y TRANSICIONES */
    .view { display: none; padding: 20px; min-height: 100vh; animation: slideIn 0.4s ease-out; }
    .active-view { display: block; }
    @keyframes slideIn { from { opacity: 0; transform: translateX(20px); } to { opacity: 1; transform: translateX(0); } }

    /* BOTONES Y INPUTS */
    .btn-glass { background: rgba(0, 102, 204, 0.9); color: white; border: none; border-radius: 12px; padding: 12px 20px; font-weight: bold; width: 100%; transition: 0.2s; box-shadow: 0 4px 0 #004c99; margin-top: 10px;}
    .btn-glass:active { transform: translateY(4px); box-shadow: none; }
    .solid-input, .solid-textarea { background-color: #f8f9fa; border: 2px solid #ddd; padding: 12px; border-radius: 10px; width: 100%; font-family: var(--font-body); text-align: center; margin-bottom:10px;}
    .home-btn { background-color: white; border: none; border-radius: 18px; padding: 15px 5px; text-align: center; cursor: pointer; display: flex; flex-direction: column; align-items: center; box-shadow: 0 4px 10px rgba(0,0,0,0.1); transition: transform 0.2s; }
    .home-btn:hover { transform: scale(1.05); }

    /* FEEDBACK ARCADE */
    .feedback-box { border-radius: 10px; padding: 15px; margin-top: 15px; display: none; animation: fadeIn 0.3s; text-align: center;}
    .feedback-box.correct { background: #d4edda; border: 2px solid #28a745; color: #155724; display: block; }
    .feedback-box.incorrect { background: #f8d7da; border: 2px solid #dc3545; color: #721c24; display: block; }
    .game-opt { background: #f0f0f0; padding: 15px; margin-bottom: 10px; border-radius: 8px; cursor: pointer; text-align: center; font-weight: bold; transition: 0.2s; border: 2px solid transparent;}
    .game-opt:hover { background: #e2e2e2; }
    .game-opt.disabled { pointer-events: none; opacity: 0.6; }

    /* RUTAS DE MISIONES (DUOLINGO) */
    .path-container { display: flex; flex-direction: column; align-items: center; position: relative; padding: 20px 0; }
    .path-container::before { content: ''; position: absolute; width: 6px; background: rgba(255,255,255,0.8); top: 0; bottom: 0; left: 50%; transform: translateX(-50%); z-index: 0; }
    .mission-node { position: relative; z-index: 1; width: 85%; background: white; border-radius: 20px; padding: 15px; display: flex; align-items: center; box-shadow: 0 5px 15px rgba(0,0,0,0.2); margin-bottom: 30px; border: 4px solid transparent; cursor: pointer; }
    .mission-node.left { align-self: flex-start; margin-right: 10%; }
    .mission-node.right { align-self: flex-end; margin-left: 10%; flex-direction: row-reverse; text-align: right; }
    .mission-node.locked { background: rgba(220,220,220,0.9); filter: grayscale(1); opacity: 0.8; pointer-events: none;}
    .mission-node.active { border-color: var(--primary); animation: pulse 2s infinite; }
    .mission-node.completed { border-color: #00b894; background: #f0fff4; }
    .node-icon { width: 60px; height: 60px; background: #eee; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; margin: 0 15px; }
    .completed .node-icon { background: #00b894; color: white; }
    .active .node-icon { background: var(--primary); color: white; }
    @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(0, 102, 204, 0.4); } 70% { box-shadow: 0 0 0 15px rgba(0, 102, 204, 0); } 100% { box-shadow: 0 0 0 0 rgba(0, 102, 204, 0); } }
    
    /* AVATARES */
    .avatar-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-bottom: 20px; }
    .avatar-item { background: white; border: 2px solid #ccc; border-radius: 10px; padding: 12px; text-align: center; cursor: pointer; font-size: 1.5rem; }
    .avatar-item.selected { border-color: var(--primary); border-width: 4px; transform: scale(1.1); }
    .avatar-item.locked { background: #444; border-color: #222; color: #777; }
    .avatar-item.unlocked { background: #FFD700; border-color: #b8860b; color: #222; box-shadow: 0 0 10px rgba(255,215,0,0.5); }

    /* BARRAS DE PROGRESO Y OTROS */
    .progress-bar-bg { background: #e9ecef; height: 20px; border-radius: 10px; overflow: hidden; margin-top: 8px; border: 1px solid #ccc;}
    .fill-global { background: linear-gradient(90deg, #FFD93D, #FF6B6B); height: 100%; width: 0%; transition: width 1s ease-out; }
    .fill-personal { background: linear-gradient(90deg, #00d2ff, #3a7bd5); height: 100%; width: 0%; transition: width 1s ease-out; }
    .xp-badge { background: var(--accent); color: #000; font-weight: 900; padding: 5px 15px; border-radius: 20px; font-size: 0.9rem; border: 2px solid #fff; display: inline-block;}
    
    /* ESTILOS DEL DIARIO Y MAPA FÍSICO */
    .mood-btn { font-size: 2.5rem; background: #fff; border: 2px solid #eee; border-radius: 12px; padding: 5px; cursor: pointer; flex: 1; text-align: center; margin: 0 3px; }
    .mood-btn.selected { background: #e6f0ff; border-color: var(--primary); transform: scale(1.1); }
    .custom-file-input { width: 100%; padding: 10px; background: #222; color: white; border-radius: 8px; cursor: pointer; margin-bottom: 10px; }
    .map-container { position: relative; width: 100%; height: 650px; background: #eee; border-radius: 15px; overflow: hidden; border: 4px solid white; box-shadow: 0 5px 25px rgba(0,0,0,0.3); display: flex; justify-content: center; align-items: center; }
    .map-frame { width: 150%; height: 150%; border: 0; pointer-events: none; transform: rotate(90deg); flex-shrink: 0; filter: contrast(1.1) saturate(1.1); }
    .map-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 5; }
    .map-pin { position: absolute; width: 55px; height: 55px; background: var(--accent); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #000; font-weight: 900; cursor: grab; border: 3px solid #fff; box-shadow: 0 6px 12px rgba(0,0,0,0.5); font-size: 1.8rem; z-index: 10; transform: translate(-50%, -50%); transition: transform 0.1s; }
    
    /* MODALS */
    .custom-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 2000; justify-content: center; align-items: center; }
    .custom-modal.show { display: flex; }
    #golden-star { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 4rem; text-shadow: 0 0 20px #FFD700; cursor: pointer; z-index: 100; display: none; }
    
    .medal-box { display: flex; gap: 10px; margin-top: 10px; }
    .medal { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; background: #eee; color: #aaa; border: 2px solid #ccc; transition: 0.3s; }
    .medal.unlocked.bronze { background: #cd7f32; color: white; border-color: #8c5622; box-shadow: 0 0 10px rgba(205,127,50,0.5); }
    .medal.unlocked.silver { background: #c0c0c0; color: white; border-color: #888; box-shadow: 0 0 10px rgba(192,192,192,0.5); }
    .medal.unlocked.gold { background: #ffd700; color: white; border-color: #b8860b; box-shadow: 0 0 15px rgba(255,215,0,0.8); }
</style>
"""

# ==========================================================
# 4. JAVASCRIPT LOGIC (TODO INCLUIDO Y SEGURO)
# ==========================================================
JS_CODE = f"""
<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
<script type="module">
    import {{ initializeApp }} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
    import {{ getFirestore, doc, setDoc, getDoc, onSnapshot }} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore.js";

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
    const MAX_INDIVIDUAL_XP = 600;

    window.app = {{
        currentChapter: {st.session_state.chapter},
        nominees: ["Les Titans", "Eco-Warriors", "Cyber-Français", "Green Team"],
        data: {{ user: {{ sprite: "", name: "", trait: "", xp: 0, usedCodes: [], unlockedAvatars: [], myVote: "" }}, missions: [], journal: [] }},
        
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

            try {{
                const localData = localStorage.getItem("jo_avenir_2026");
                if (localData) {{
                    const parsedData = JSON.parse(localData);
                    if (parsedData && parsedData.user) window.app.data = parsedData;
                }}
            }} catch (error) {{
                console.error("Erreur critique de LocalStorage:", error);
                localStorage.removeItem("jo_avenir_2026");
            }}

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
                window.app.nav('home');
            }} else {{
                window.app.nav('login');
            }}
        }},

        toggleZen: () => {{
            document.body.classList.toggle('mode-zen');
            localStorage.setItem('jo_avenir_zen', document.body.classList.contains('mode-zen'));
        }},

        saveData: async () => {{
            try {{ localStorage.setItem("jo_avenir_2026", JSON.stringify(window.app.data)); }} catch(e) {{}}
            try {{ if(db && window.app.data.user.name !== "") await setDoc(doc(db, "students", window.app.data.user.name), window.app.data); }} catch(e) {{}}
            window.app.updateUI();
        }},

        addXP: (amount) => {{
            sfx_coin.play().catch(e => console.warn(e));
            window.app.data.user.xp += amount;
            window.app.saveData();
            try {{ confetti({{ particleCount: 100, spread: 70, origin: {{ y: 0.6 }} }}); }} catch(e) {{}}
        }},

        nav: (view) => {{
            document.querySelectorAll('.view').forEach(v => v.classList.remove('active-view'));
            document.getElementById('view-' + view).classList.add('active-view');
            
            const header = document.getElementById('app-header');
            const title = document.getElementById('header-title');
            
            if(view === 'login' || view === 'home') {{
                header.classList.remove('visible');
            }} else {{
                header.classList.add('visible');
                const titles = {{
                    'profil': "{t['profil_btn']}", 'missions': "{t['progression']}",
                    'map': "{t['campus_map']}", 'journal': "{t['journal_title']}",
                    'games': "{t['arcade_title']}", 'oscars': "{t['oscars_title']}"
                }};
                title.innerText = titles[view] || "J.O. AVENIR";
            }}

            if(view === 'missions') window.app.renderPath();
        }},

        renderAvatars: () => {{
            const grid = document.getElementById('sprite-container'); grid.innerHTML = "";
            const SPRITES = ["fa-dragon", "fa-ghost", "fa-robot", "fa-cat", "fa-bolt", "fa-fire", "fa-snowflake", "fa-leaf", "fa-crow", "fa-spider", "fa-fish", "fa-bug", "fa-hippo", "fa-otter", "fa-frog", "fa-horse", "fa-dove", "fa-dog", "fa-kiwi-bird", "fa-worm", "fa-locust", "fa-mosquito", "fa-meteor"];
            const HIDDEN_SPRITES = [
                {{ icon: "fa-crown", code: "NOVA-33" }}, {{ icon: "fa-user-astronaut", code: "TITAN-8X" }}, 
                {{ icon: "fa-jedi", code: "NEXUS-V" }}, {{ icon: "fa-user-ninja", code: "PHOENIX-9" }}, 
                {{ icon: "fa-mask", code: "SPARK-44" }}, {{ icon: "fa-hat-wizard", code: "AURA-77" }}, 
                {{ icon: "fa-gem", code: "ECHO-LUM" }}
            ];
            
            SPRITES.forEach(icon => {{
                const div = document.createElement('div'); div.className = "avatar-item";
                if(window.app.data.user.sprite === icon) div.classList.add('selected');
                div.innerHTML = `<i class="fa-solid ${{icon}}"></i>`;
                div.onclick = function() {{
                    document.querySelectorAll('.avatar-item').forEach(el => el.classList.remove('selected'));
                    this.classList.add('selected'); window.app.data.user.sprite = icon;
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
                        this.classList.add('selected'); window.app.data.user.sprite = h.icon;
                    }};
                }} else {{
                    div.className = "avatar-item locked";
                    div.innerHTML = `<i class="fa-solid fa-lock"></i>`;
                    div.onclick = function() {{
                        const guess = prompt("Code secret:");
                        if (guess && guess.trim().toUpperCase() === h.code) {{
                            window.app.data.user.unlockedAvatars.push(h.icon);
                            window.app.saveData(); window.app.renderAvatars();
                            try{{ confetti(); }}catch(e){{}}
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
            document.querySelectorAll('.xp-counter').forEach(el => el.innerText = xp);
            
            document.querySelectorAll('.mini-avatar').forEach(mini => {{
                if(window.app.data.user.sprite) {{
                    mini.innerHTML = `<i class="fa-solid ${{window.app.data.user.sprite}}"></i>`;
                }}
            }});
            
            if (xp >= 100) document.getElementById('m-bronze').classList.add('unlocked', 'bronze');
            if (xp >= 300) document.getElementById('m-silver').classList.add('unlocked', 'silver');
            if (xp >= 500) document.getElementById('m-gold').classList.add('unlocked', 'gold');
            
            let globalPct = Math.min((xp / 1000) * 100, 100);
            const gb = document.querySelector('.fill-global');
            if(gb) gb.style.width = globalPct + "%";
            
            let personalPct = Math.min((xp / MAX_INDIVIDUAL_XP) * 100, 100);
            const pb = document.getElementById('personal-xp');
            if(pb) pb.style.width = personalPct + "%";
            
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
            try{{ confetti({{ particleCount: 300, spread: 160, origin: {{ y: 0.4 }} }}); }}catch(e){{}}
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
            window.app.nav('home');
        }},

        renderPath: () => {{
            const container = document.getElementById('path-container'); container.innerHTML = "";
            window.app.data.missions.forEach((m, idx) => {{
                const isLeft = idx % 2 === 0; const reqChapter = idx + 1;
                let statusClass = m.completed ? 'completed' : ''; let iconClass = m.completed ? 'fa-check' : m.icon;
                
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

        // === ARCADE (10 CATEGORIES CON FEEDBACK) ===
        startGame: (t) => {{
            const QUIZ = {{
                num: [
                    {{ q: "10 stylos = 20€. 1 stylo = ?", a: ["2€", "5€", "1€"], c: 0, f: "20 divisé par 10 fait 2. Un stylo coûte 2€." }},
                    {{ q: "90 + 9 = ?", a: ["99", "89", "19"], c: 0, f: "Quatre-vingt-dix (90) plus neuf (9) = Quatre-vingt-dix-neuf (99)." }},
                    {{ q: "La moitié de 50 ?", a: ["25", "20", "30"], c: 0, f: "50 divisé par 2 est égal à 25." }}
                ],
                fut: [
                    {{ q: "Demain je ___ (manger)", a: ["mangerai", "mangerais", "mange"], c: 0, f: "Le futur simple avec 'je' se termine toujours par -ai." }},
                    {{ q: "Nous ___ (finir)", a: ["finirons", "finissons", "finiront"], c: 0, f: "Au futur, la terminaison pour 'Nous' est -ons." }},
                    {{ q: "Ils ___ (aller)", a: ["iront", "allent", "allons"], c: 0, f: "Le verbe 'aller' est irrégulier. Son radical au futur est 'ir-'." }}
                ],
                part: [
                    {{ q: "Je veux ___ eau", a: ["de l'", "du", "de la"], c: 0, f: "Devant une voyelle ou un 'h' muet, on utilise 'de l''." }},
                    {{ q: "Il mange ___ pain", a: ["du", "de la", "des"], c: 0, f: "Pain est masculin singulier, on utilise donc 'du'." }},
                    {{ q: "Elle boit ___ limonade", a: ["de la", "du", "des"], c: 0, f: "Limonade est féminin, on utilise 'de la'." }}
                ],
                sport: [
                    {{ q: "Le sport dans l'eau ?", a: ["Natation", "Judo", "Tennis"], c: 0, f: "La natation se pratique dans une piscine ou en eau libre." }},
                    {{ q: "Pour courir il faut des...", a: ["Baskets", "Gants", "Lunettes"], c: 0, f: "Les baskets (chaussures de sport) sont essentielles pour courir." }},
                    {{ q: "Le Tour de France est une course de...", a: ["Cyclisme", "Natation", "Athlétisme"], c: 0, f: "C'est la course cycliste la plus célèbre au monde." }}
                ],
                imp: [
                    {{ q: "(Courir) ___ vite !", a: ["Cours", "Coures", "Courir"], c: 0, f: "À l'impératif, les verbes en -ir (comme courir) prennent un 's' à la 2e personne." }},
                    {{ q: "(Arrêter) ___ de parler ! (vous)", a: ["Arrêtez", "Arrêter", "Arrêtes"], c: 0, f: "Avec 'vous', la terminaison est -ez." }},
                    {{ q: "(Être) ___ gentil !", a: ["Sois", "Es", "Est"], c: 0, f: "Le verbe être est irrégulier : Sois, soyons, soyez." }}
                ],
                odd: [
                    {{ q: "ODD 13 c'est pour...", a: ["Le Climat", "La Faim", "L'Eau"], c: 0, f: "L'ODD 13 concerne les mesures relatives à la lutte contre les changements climatiques." }},
                    {{ q: "ODD 5 c'est...", a: ["Égalité", "Santé", "Villes"], c: 0, f: "L'ODD 5 vise à parvenir à l'égalité des sexes." }},
                    {{ q: "ODD 14 protège...", a: ["Les Océans", "Les Forêts", "Les Villes"], c: 0, f: "La vie aquatique et la protection des océans." }}
                ],
                bio: [
                    {{ q: "Où jeter une bouteille en plastique ?", a: ["Poubelle Jaune", "Poubelle Verte", "Poubelle Bleue"], c: 0, f: "Le bac jaune est destiné aux emballages plastiques et cartons." }},
                    {{ q: "Quel gaz cause l'effet de serre ?", a: ["Le CO2", "L'Oxygène", "L'Azote"], c: 0, f: "Le dioxyde de carbone (CO2) retient la chaleur dans l'atmosphère." }},
                    {{ q: "L'énergie solaire est...", a: ["Renouvelable", "Fossile", "Polluante"], c: 0, f: "Le soleil fournit une énergie propre et inépuisable." }}
                ],
                geo: [
                    {{ q: "Où sont nés les Jeux Olympiques ?", a: ["En Grèce", "En France", "En Italie"], c: 0, f: "Ils ont été créés à Olympie, en Grèce antique." }},
                    {{ q: "Combien d'anneaux sur le drapeau olympique ?", a: ["5", "6", "4"], c: 0, f: "Les 5 anneaux représentent les 5 continents unis par le sport." }},
                    {{ q: "Quelle est la capitale de la France ?", a: ["Paris", "Lyon", "Marseille"], c: 0, f: "Paris accueillera les J.O. en 2024 !" }}
                ],
                math: [
                    {{ q: "Un athlète court 100m en 10s. Vitesse ?", a: ["10 m/s", "100 m/s", "1 m/s"], c: 0, f: "Vitesse = Distance / Temps. 100 / 10 = 10 m/s." }},
                    {{ q: "Aire d'un terrain de 50m x 20m ?", a: ["1000 m²", "100 m²", "500 m²"], c: 0, f: "L'aire d'un rectangle = Longueur x Largeur. 50 x 20 = 1000." }},
                    {{ q: "5 x 5 x 5 = ?", a: ["125", "25", "15"], c: 0, f: "5 au cube (5³) fait 125." }}
                ],
                fra: [
                    {{ q: "Il faut que nous _____ (participer).", a: ["participions", "participons", "participerons"], c: 0, f: "Après 'Il faut que', on utilise le subjonctif présent." }},
                    {{ q: "Synonyme de 'Gagner' ?", a: ["Remporter", "Perdre", "Échouer"], c: 0, f: "Remporter la victoire, c'est gagner." }},
                    {{ q: "Le contraire de 'Rapide' ?", a: ["Lent", "Fort", "Vite"], c: 0, f: "Lent est l'antonyme de rapide." }}
                ]
            }};
            
            window.app.currentQuiz = QUIZ[t] || [
                {{ q: "Question générique ?", a: ["Option A", "Option B"], c: 0, f: "Explication de la réponse." }}
            ];
            
            window.app.qIndex = 0; 
            window.app.score = 0; 
            
            document.getElementById('game-menu').style.display = 'none'; 
            document.getElementById('game-interface').style.display = 'block'; 
            window.app.renderQuestion(); 
        }},

        renderQuestion: () => {{
            if(window.app.qIndex >= window.app.currentQuiz.length) {{
                alert("{t['end_score']}" + window.app.score); 
                window.app.addXP(window.app.score); 
                document.getElementById('game-interface').style.display = 'none'; 
                document.getElementById('game-menu').style.display = 'flex';
                return;
            }} 
            const q = window.app.currentQuiz[window.app.qIndex]; 
            document.getElementById('game-question').innerText = q.q; 
            
            const optionsDiv = document.getElementById('game-options'); 
            optionsDiv.innerHTML = ""; 
            q.a.forEach((ans, i) => {{
                optionsDiv.innerHTML += `<div class='game-opt' onclick='window.app.checkAnswer(${{i}}, this)'>${{ans}}</div>`;
            }});
            
            document.getElementById('game-feedback').style.display = "none";
            document.getElementById('btn-next-question').style.display = "none";
        }},

        checkAnswer: (selectedIdx, btnElement) => {{
            document.querySelectorAll('.game-opt').forEach(el => el.classList.add('disabled'));
            
            const q = window.app.currentQuiz[window.app.qIndex];
            const feedbackBox = document.getElementById('game-feedback');
            const feedbackText = document.getElementById('feedback-text');
            const btnNext = document.getElementById('btn-next-question');

            if(selectedIdx === q.c) {{
                window.app.score += 10; 
                btnElement.style.border = "3px solid #28a745";
                feedbackBox.className = "feedback-box correct";
                feedbackText.innerHTML = `<strong>{t['correct']}</strong><br><small>${{q.f}}</small>`;
                try {{ confetti({{ particleCount: 40, spread: 50, origin: {{ y: 0.6 }} }}); }} catch(e) {{}}
            }} else {{
                btnElement.style.border = "3px solid #dc3545";
                document.querySelectorAll('.game-opt')[q.c].style.border = "3px solid #28a745";
                feedbackBox.className = "feedback-box incorrect";
                feedbackText.innerHTML = `<strong>{t['incorrect']}</strong><br><small>${{q.f}}</small>`;
            }}

            feedbackBox.style.display = "block";
            btnNext.style.display = "block";
        }},

        nextQuestion: () => {{
            window.app.qIndex++; 
            window.app.renderQuestion();
        }},
        
        exitGame: () => {{
            document.getElementById('game-interface').style.display = 'none'; 
            document.getElementById('game-menu').style.display = 'flex'; 
        }},

        // === OTROS (DIARIO, MAPA, TTS, OSCARS) ===
        selectMood: (e,m) => {{
            document.querySelectorAll('.mood-btn').forEach(b => b.classList.remove('selected'));
            e.classList.add('selected'); document.getElementById('selected-mood').value = m;
        }},
        saveJournal: () => {{ 
            const m = document.getElementById('selected-mood').value;
            const t = document.getElementById('journal-text').value;
            if(!m || !t) return; 
            if(!window.app.data.journal) window.app.data.journal = [];
            window.app.data.journal.unshift({{d: new Date().toLocaleDateString(), m: m, t: t}});
            window.app.addXP(20); window.app.saveData(); window.app.renderJournal();
            document.getElementById('journal-text').value = ""; document.getElementById('selected-mood').value = "";
            document.querySelectorAll('.mood-btn').forEach(b => b.classList.remove('selected'));
        }},
        renderJournal: () => {{
            const c = document.getElementById('journal-feed'); c.innerHTML = ""; 
            if(!window.app.data.journal) window.app.data.journal = []; 
            window.app.data.journal.forEach(e => {{ 
                c.innerHTML += `<div class='glass-panel'><div class='d-flex justify-content-between mb-2'><span class="text-secondary small fw-bold">${{e.d}}</span><span style="font-size:1.5rem;">${{e.m}}</span></div><p class='text-dark mb-0'>${{e.t}}</p></div>`;
            }}); 
        }},
        allowDrop: (ev) => {{ ev.preventDefault(); }},
        drag: (ev) => {{ ev.dataTransfer.setData("text", ev.target.id); }},
        drop: (ev) => {{ 
            ev.preventDefault(); 
            const data = ev.dataTransfer.getData("text"); 
            const el = document.getElementById(data); 
            const rect = ev.currentTarget.getBoundingClientRect(); 
            const x = ev.clientX - rect.left; const y = ev.clientY - rect.top; 
            el.style.left = ((x / rect.width) * 100) + "%"; el.style.top = ((y / rect.height) * 100) + "%"; 
        }},
        renderNominees: () => {{
            const list = document.getElementById('nominees-list'); list.innerHTML = "";
            const nominees = ["Les Titans", "Eco-Warriors", "Cyber-Français", "Green Team"];
            nominees.forEach(n => {{
                list.innerHTML += `<div class='glass-panel d-flex justify-content-between align-items-center mb-2'><span class="fw-bold text-dark">${{n}}</span><button class='btn btn-warning fw-bold' style='border-radius:8px;' onclick='window.app.submitVote("${{n}}")'>{t['vote_btn']}</button></div>`;
            }});
        }},
        submitVote: (name) => {{
            if(window.app.data.user.myVote && window.app.data.user.myVote !== "") {{ alert("{t['already_voted']}"); return; }}
            if(confirm("Voter pour " + name + " ?")) {{ window.app.data.user.myVote = name; window.app.addXP(20); window.app.saveData(); window.app.renderNominees(); }}
        }},
        speakText: (text) => {{
            window.speechSynthesis.cancel(); 
            const msg = new SpeechSynthesisUtterance(); msg.text = text; msg.lang = 'fr-FR'; 
            window.speechSynthesis.speak(msg);
        }},
        speakQuestion: () => {{ window.app.speakText(document.getElementById('game-question').innerText); }},
        claimUltimateReward: () => {{
            try{{ confetti({{ particleCount: 300, spread: 160, origin: {{ y: 0.4 }} }}); }}catch(e){{}}
            document.getElementById('golden-star').style.display = 'none'; 
            document.getElementById('ultimateModal').classList.add('show');
        }}
    }};

    setTimeout(() => window.app.init(), 200);
</script>
"""

# ==========================================================
# 6. HTML FINAL (VISTAS COMPLETAS)
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
    <!-- HEADER NATIVO -->
    <div id="app-header" class="app-header">
        <button class="back-btn" onclick="window.app.nav('home')"><i class="fa-solid fa-chevron-left"></i></button>
        <div id="header-title" class="header-title">TITRE</div>
    </div>

    <!-- BOTON ZEN (FIJO) -->
    <div style="position:fixed; top:10px; right:10px; z-index:9999;">
        <button class="btn-zen" onclick="window.app.toggleZen()">🧠 Mode Zen</button>
    </div>

    <!-- PANTALLA LOGIN -->
    <section id="view-login" class="view">
        <div class="glass-panel text-center mt-2">
            <h1 class="fw-bold" style="font-family: var(--font-head); font-size:2.5rem;">J.O. AVENIR</h1>
        </div>
        <div class="glass-panel mt-4">
            <h4 class="fw-bold">{t['create_athlete']}</h4>
            <div class="avatar-grid" id="sprite-container"></div>
            <input type="text" id="player-name" class="solid-input mb-3" placeholder="{t['name_label']}">
            <div class="trait-selector" id="trait-container"></div>
            <button class="btn-glass mt-2" onclick="window.app.saveProfile()">{t['enter_stadium']}</button>
        </div>
    </section>

    <!-- MENÚ PRINCIPAL (HOME) -->
    <section id="view-home" class="view">
        <div class="d-flex align-items-center justify-content-between mb-4 mt-2">
            <div>
                <h1 style="font-family: var(--font-head); font-weight: 900; font-size: 2rem; color: #222; margin:0;">J.O. AVENIR</h1>
                <div class="badge bg-warning text-dark fs-6 mt-1"><i class="fa-solid fa-star"></i> <span class="xp-counter">0</span> XP</div>
            </div>
            <div class="mini-avatar" style="font-size: 2.2rem; color: var(--primary); background: white; padding: 15px; border-radius: 50%; box-shadow: 0 4px 10px rgba(0,0,0,0.1);"></div>
        </div>

        <div class="glass-panel mb-4">
            <h6 class="fw-bold"><i class="fa-solid fa-earth-americas text-primary"></i> {t['global_impact']}</h6>
            <div class="progress" style="height: 15px; border-radius: 10px; background:#fff;">
                <div id="global-xp" class="progress-bar bg-success progress-bar-striped progress-bar-animated" style="width: 15%"></div>
            </div>
            <small class="text-secondary">{t['obj_comm']}</small>
        </div>

        <div class="row g-3 mb-4">
            <div class="col-6"><div class="home-btn" onclick="window.app.nav('profil')"><i class="fa-solid fa-user text-secondary mb-2 fs-1"></i><h6 class="fw-bold mb-0">{t['profil_btn']}</h6></div></div>
            <div class="col-6"><div class="home-btn" style="background:#f0f4ff;" onclick="window.app.nav('missions')"><i class="fa-solid fa-route text-primary mb-2 fs-1"></i><h6 class="fw-bold mb-0">{t['missions_btn']}</h6></div></div>
            <div class="col-6"><div class="home-btn" onclick="window.app.nav('games')"><i class="fa-solid fa-gamepad text-success mb-2 fs-1"></i><h6 class="fw-bold mb-0">{t['arcade_btn']}</h6></div></div>
            <div class="col-6"><div class="home-btn" onclick="window.app.nav('map')"><i class="fa-solid fa-map-location-dot text-danger mb-2 fs-1"></i><h6 class="fw-bold mb-0">{t['map_btn']}</h6></div></div>
            <div class="col-6"><div class="home-btn" onclick="window.app.nav('journal')"><i class="fa-solid fa-book-open text-info mb-2 fs-1"></i><h6 class="fw-bold mb-0">{t['journal_btn']}</h6></div></div>
            <div class="col-6"><div class="home-btn" style="background:#fff3e0;" onclick="window.app.nav('oscars')"><i class="fa-solid fa-award text-warning mb-2 fs-1"></i><h6 class="fw-bold mb-0">{t['oscars_btn']}</h6></div></div>
        </div>
    </section>

    <!-- SECCIÓN PERFIL Y CÓDIGOS -->
    <section id="view-profil" class="view">
        <div class="glass-panel mt-4">
            <h6 class="fw-bold"><i class="fa-solid fa-user text-info"></i> {t['personal_impact']}</h6>
            <div class="progress" style="height: 15px; border-radius: 10px; background:#fff;">
                <div id="personal-xp" class="progress-bar bg-info progress-bar-striped progress-bar-animated" style="width: 0%"></div>
            </div>
            <div class="medal-box mt-2">
                <div id="m-bronze" class="medal"><i class="fa-solid fa-medal"></i></div>
                <div id="m-silver" class="medal"><i class="fa-solid fa-medal"></i></div>
                <div id="m-gold" class="medal"><i class="fa-solid fa-trophy"></i></div>
            </div>
        </div>

        <div class="glass-panel text-center">
            <h6 class="fw-bold text-dark"><i class="fa-solid fa-user-secret text-danger"></i> {t['secret_codes_title']}</h6>
            <p class="small text-secondary mb-2">{t['secret_codes_desc']}</p>
            <div class="d-flex gap-2">
                <input type="text" id="secret-code-input" class="solid-input mb-0" placeholder="CODE...">
                <button class="btn btn-dark" style="border-radius: 8px; font-weight:bold;" onclick="window.app.checkSecretCode()">GO</button>
            </div>
            <div id="secret-msg" class="small mt-2 fw-bold"></div>
        </div>
    </section>

    <!-- SECCIÓN RUTA DE MISIONES -->
    <section id="view-missions" class="view">
        <div id="path-container" class="path-container"></div>
    </section>

    <!-- SECCIÓN ARCADE (CON FEEDBACK) -->
    <section id="view-games" class="view">
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
                
                <!-- CAJA DE FEEDBACK -->
                <div id="game-feedback" class="feedback-box">
                    <span id="feedback-text"></span>
                </div>
                
                <button id="btn-next-question" class="btn-glass mt-3" style="display:none;" onclick="window.app.nextQuestion()">{t['next']}</button>
            </div>
            <button onclick="window.app.exitGame()" class="btn btn-outline w-100">{t['quit']}</button>
        </div>
    </section>

    <!-- SECCIÓN MAPA -->
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
                </div>
            </div>
            <div class="glass-panel mt-3">
                <h6 class="text-dark mb-2 fw-bold" style="font-size: 0.85rem;"><i class="fa-solid fa-hand-pointer text-primary"></i> {t['legend']}</h6>
                <div class="row g-1 small text-dark" style="font-size: 0.7rem; font-weight: bold;">
                    <div class="col-4">🚀 {t['p_start']}</div> <div class="col-4">🏁 {t['p_end']}</div> <div class="col-4">🍎 {t['p_food']}</div>
                    <div class="col-4">♻️ {t['p_recyc']}</div> <div class="col-4">💧 {t['p_water']}</div> <div class="col-4">🏥 {t['p_med']}</div>
                </div>
            </div>
        </div>
    </section>

    <!-- SECCIÓN DIARIO DE A BORDO -->
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

    <!-- SECCIÓN OSCARS (VOTACIONES) -->
    <section id="view-oscars" class="view">
        <h4 class="fw-bold mb-3 text-white" style="text-shadow: 1px 1px 3px rgba(0,0,0,0.5);">{t['oscars_title']}</h4>
        <div id="nominees-list"></div>
    </section>

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
