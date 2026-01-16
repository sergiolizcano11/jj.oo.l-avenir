import streamlit as st
import pandas as pd
import os
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import random
import time
from datetime import datetime
from st_audiorec import st_audiorec 
from gtts import gTTS

# --- 1. CONFIGURACIÓN ---
st.set_page_config(
    page_title="Le Lycée Olympique",
    page_icon="🏟️",
    layout="centered",
    initial_sidebar_state="collapsed" 
)

# --- 2. CSS "TROPHY ROOM" ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700;900&display=swap');

    :root {
        --primary: #4D79FF;
        --card-bg: rgba(255, 255, 255, 0.96);
        --text: #1A1A1A;
    }

    /* FONDO */
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?q=80&w=2069&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Poppins', sans-serif;
    }
    .stApp::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.2); z-index: -1;
    }

    /* TARJETAS */
    .css-1r6slb0, .stDataFrame, .stForm, div[data-testid="stExpander"], .news-card, .photo-card, .mood-card, .trophy-case {
        background: var(--card-bg);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        margin-bottom: 25px;
        border: none;
    }

    /* HERO HEADER */
    .hero-header {
        background: linear-gradient(180deg, #4D79FF 0%, #00C6FF 100%);
        padding: 40px 20px;
        border-radius: 0 0 40px 40px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 15px 30px rgba(0,0,0,0.3);
        border-bottom: 6px solid #0099cc;
    }
    .hero-header h1 { font-size: 2.2rem; font-weight: 900; margin: 0; color: white !important; }

    /* TEXTOS */
    h1, h2, h3, p, label, .stMarkdown { color: var(--text) !important; }

    /* MEDALLAS */
    .medal-unlocked { font-size: 40px; filter: drop-shadow(0 5px 5px rgba(0,0,0,0.2)); cursor: help; }
    .medal-locked { font-size: 40px; filter: grayscale(100%) opacity(0.3); cursor: not-allowed; }
    .medal-container { text-align: center; display: inline-block; width: 18%; }
    .medal-label { font-size: 0.7rem; font-weight: bold; color: #666; display: block; }

    /* BOTONES */
    .stButton > button {
        background: linear-gradient(to bottom, #4D79FF, #3a60d0);
        color: white; border-radius: 15px; border: none;
        border-bottom: 6px solid #2a50c4; padding: 15px; font-weight: 800; width: 100%;
    }
    .stButton > button:active { transform: translateY(4px); border-bottom: 2px solid #2a50c4; }
    
</style>
""", unsafe_allow_html=True)

# --- 3. BASE DE DATOS ---
FILE_ELEVES = 'eleves.csv'
FILE_TEAMS = 'teams.csv'
FILE_GALLERY = 'gallery.csv'
FILE_NEWS = 'news_feed.csv'
FILE_JOURNAL = 'journal.csv' 

def init_db():
    cols_eleves = ['Pseudo', 'Avatar', 'Forces', 'Faiblesse', 'TeamName']
    cols_teams = ['TeamName', 'Slogan', 'MembersCount', 'Points']
    cols_gallery = ['TeamName', 'Uploader', 'ImageB64', 'Caption', 'Date'] # Added Uploader for medal check
    cols_news = ['Date', 'Titre', 'Contenu', 'Type']
    cols_journal = ['Pseudo', 'Date', 'Reflexion', 'Humeur']

    for file, cols in [(FILE_ELEVES, cols_eleves), (FILE_TEAMS, cols_teams), 
                       (FILE_GALLERY, cols_gallery), (FILE_NEWS, cols_news), (FILE_JOURNAL, cols_journal)]:
        if not os.path.exists(file):
            pd.DataFrame(columns=cols).to_csv(file, index=False)
        else:
            df = pd.read_csv(file)
            for c in cols:
                if c not in df.columns: df[c] = ""
            df.to_csv(file, index=False)

def load_data(file): return pd.read_csv(file)
def save_data(df, file): df.to_csv(file, index=False)

init_db()
df_eleves = load_data(FILE_ELEVES)
df_teams = load_data(FILE_TEAMS)
df_gallery = load_data(FILE_GALLERY)
df_news = load_data(FILE_NEWS)
df_journal = load_data(FILE_JOURNAL)

def auto_post(title, content, type_msg="Info 📢"):
    global df_news
    df_news = load_data(FILE_NEWS)
    new_n = pd.DataFrame([[datetime.now().strftime("%d/%m %H:%M"), title, content, type_msg]],
                       columns=['Date', 'Titre', 'Contenu', 'Type'])
    df_news = pd.concat([new_n, df_news], ignore_index=True)
    save_data(df_news, FILE_NEWS)

# --- 4. FUNCIÓN GAMIFICACIÓN (CÁLCULO DE MEDALLAS) ---
def get_medals(pseudo):
    """Calcula las medallas basadas en acciones reales en la DB"""
    medals = []
    
    # 1. Medalla BIENVENIDA (Siempre True si tiene perfil)
    medals.append({"icon": "🥇", "name": "Début", "desc": "Profil créé", "unlocked": True})
    
    # 2. Medalla EQUIPO (Si tiene TeamName != None)
    user_data = df_eleves[df_eleves['Pseudo'] == pseudo]
    has_team = False
    if not user_data.empty:
        team = user_data.iloc[0]['TeamName']
        if team and team != "None" and str(team) != "nan":
            has_team = True
    medals.append({"icon": "🛡️", "name": "Squad", "desc": "Rejoint une équipe", "unlocked": has_team})
    
    # 3. Medalla REPORTERO (Si ha subido foto a la galería)
    # Nota: Chequeamos si su pseudo aparece como Uploader (hemos añadido esa columna)
    has_photo = pseudo in df_gallery['Uploader'].values if 'Uploader' in df_gallery.columns else False
    medals.append({"icon": "📸", "name": "Reporter", "desc": "Photo postée", "unlocked": has_photo})
    
    # 4. Medalla FILÓSOFO (Si ha escrito en el diario)
    has_journal = pseudo in df_journal['Pseudo'].values
    medals.append({"icon": "✍️", "name": "Pensée", "desc": "Journal écrit", "unlocked": has_journal})
    
    return medals

# --- 5. NAVEGACIÓN ---
if 'page' not in st.session_state: st.session_state['page'] = 'home'
def nav(page_name): 
    st.session_state['page'] = page_name
    st.rerun()

# --- SIDEBAR PROFESOR ---
with st.sidebar:
    st.header("👨‍🏫 Zone Prof")
    if st.text_input("Code", type="password") == "admin":
        st.success("Admin")
        st.markdown("---")
        st.subheader("📖 Lecture Journaux")
        if df_journal.empty:
            st.info("Aucun journal.")
        else:
            student_filter = st.selectbox("Filtrer par élève", ["Tous"] + list(df_journal['Pseudo'].unique()))
            view_df = df_journal if student_filter == "Tous" else df_journal[df_journal['Pseudo'] == student_filter]
            for i, row in view_df.iterrows():
                with st.expander(f"{row['Date']} - {row['Pseudo']} ({row['Humeur']})"):
                    st.write(row['Reflexion'])
        st.markdown("---")
        if st.button("Reset News"):
            pd.DataFrame(columns=['Date','Titre','Contenu','Type']).to_csv(FILE_NEWS, index=False)
            st.rerun()

# ==========================================
#              PÁGINAS DE LA APP
# ==========================================

# --- 1. EL PATIO (HOME) ---
if st.session_state['page'] == 'home':
    st.markdown("""
    <div class="hero-header">
        <h1>🏟️ Le Lycée Olympique</h1>
        <p>Bienvenue sur le campus numérique !</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="mood-card">', unsafe_allow_html=True)
    st.markdown("##### 👋 Comment ça va ?")
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("🤩"): st.toast("Super énergie !"); 
    if c2.button("🙂"): st.toast("Ça va bien"); 
    if c3.button("😐"): st.toast("Moyen..."); 
    if c4.button("😴"): st.toast("Fatigué..."); 
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 📢 Actualités")
    if df_news.empty: st.info("Le campus est calme...")
    for i, row in df_news.iterrows():
        icon = "📢"
        if "Équipe" in str(row['Type']): icon = "🛡️"
        if "Photo" in str(row['Type']): icon = "📸"
        st.markdown(f"""
        <div class="news-card">
            <div class="news-meta"><span>{icon} {row['Type']}</span><span>{row['Date']}</span></div>
            <h3 style="color:#4D79FF;">{row['Titre']}</h3>
            <p style="color:black;">{row['Contenu']}</p>
        </div>""", unsafe_allow_html=True)

# --- 2. PERFIL (CON MEDALLAS) ---
elif st.session_state['page'] == 'profile':
    st.markdown("<h1>👤 Mon Profil</h1>", unsafe_allow_html=True)
    
    # 1. FORMULARIO DE PERFIL
    st.markdown('<div class="css-1r6slb0">', unsafe_allow_html=True)
    with st.form("my_profile"):
        c1, c2 = st.columns([1,2])
        with c1: 
            av = st.selectbox("Avatar", ["🦊","🦁","🐯","🦄","🐲","⚡","🔥","🚀","🤖","👽","🦸","🥷"])
            st.markdown(f"<div style='font-size:50px;text-align:center'>{av}</div>", unsafe_allow_html=True)
        with c2: 
            ps = st.text_input("Pseudo (Pour charger ton profil)")
        
        forces = st.multiselect("Forces", ["Vitesse","Force","Stratégie","Endurance","Créativité"])
        if st.form_submit_button("💾 Sauvegarder / Charger"):
            if ps and forces:
                # Si no existe, lo creamos
                if ps not in df_eleves['Pseudo'].values:
                    new = pd.DataFrame([[ps, av, ",".join(forces), "", "None"]], columns=df_eleves.columns)
                    df_eleves = pd.concat([df_eleves, new], ignore_index=True)
                    save_data(df_eleves, FILE_ELEVES)
                    auto_post(f"Nouvel Élève !", f"{ps} ({av}) a rejoint le lycée !", "Bienvenue 👋")
                    st.success("Profil créé !")
                else:
                    st.success("Profil chargé !")
                    # Aquí podríamos cargar los datos existentes en los inputs si streamlit lo permitiera fácil
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. SALA DE TROFEOS (GAMIFICACIÓN)
    if ps: # Solo si ha puesto un nombre
        st.markdown("### 🏆 Mes Succès")
        st.markdown('<div class="trophy-case">', unsafe_allow_html=True)
        
        my_medals = get_medals(ps)
        unlocked_count = sum(1 for m in my_medals if m['unlocked'])
        total_medals = len(my_medals)
        
        # Barra de progreso
        st.progress(unlocked_count / total_medals)
        st.caption(f"Niveau: {unlocked_count}/{total_medals} Médailles")
        
        # Grid de medallas
        cols = st.columns(total_medals)
        for idx, medal in enumerate(my_medals):
            with cols[idx]:
                css_class = "medal-unlocked" if medal['unlocked'] else "medal-locked"
                st.markdown(f"""
                <div class="medal-container">
                    <div class="{css_class}" title="{medal['desc']}">{medal['icon']}</div>
                    <span class="medal-label">{medal['name']}</span>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 3. EQUIPOS ---
elif st.session_state['page'] == 'teams':
    st.markdown("<h1>🛡️ Les Équipes</h1>", unsafe_allow_html=True)
    tab_create, tab_join = st.tabs(["✨ Créer", "🤝 Rejoindre"])
    
    with tab_create:
        with st.form("create_team"):
            st.write("Fonde ton équipe !")
            t_name = st.text_input("Nom de l'Équipe")
            t_slogan = st.text_input("Slogan")
            leader_name = st.selectbox("Qui est le chef ?", df_eleves['Pseudo'].unique())
            
            if st.form_submit_button("🔥 Fonder"):
                if t_name and t_slogan:
                    if t_name not in df_teams['TeamName'].values:
                        new_t = pd.DataFrame([[t_name, t_slogan, 1, 0]], columns=df_teams.columns)
                        df_teams = pd.concat([df_teams, new_t], ignore_index=True)
                        save_data(df_teams, FILE_TEAMS)
                        idx = df_eleves[df_eleves['Pseudo'] == leader_name].index[0]
                        df_eleves.at[idx, 'TeamName'] = t_name
                        save_data(df_eleves, FILE_ELEVES)
                        auto_post(f"Nouvelle Équipe : {t_name} !", f"Slogan : « {t_slogan} »", "Équipe 🛡️")
                        st.balloons(); st.success("Équipe créée !")
                    else: st.error("Déjà pris.")

    with tab_join:
        if df_teams.empty:
            st.warning("Aucune équipe.")
        else:
            for i, row in df_teams.iterrows():
                with st.expander(f"🛡️ {row['TeamName']}"):
                    st.markdown(f"**« {row['Slogan']} »**")
                    members = df_eleves[df_eleves['TeamName'] == row['TeamName']]['Pseudo'].tolist()
                    st.write(f"👥 Membres: {', '.join(members)}")
                    me = st.selectbox(f"Je suis...", df_eleves['Pseudo'].unique(), key=f"j_{i}")
                    if st.button(f"Rejoindre {row['TeamName']}", key=f"btn_{i}"):
                        idx = df_eleves[df_eleves['Pseudo'] == me].index[0]
                        df_eleves.at[idx, 'TeamName'] = row['TeamName']
                        save_data(df_eleves, FILE_ELEVES)
                        auto_post("Recrutement !", f"{me} a rejoint {row['TeamName']} !", "Info 🤝")
                        st.rerun()

# --- 4. GALERÍA ---
elif st.session_state['page'] == 'gallery':
    st.markdown("<h1>📸 Galerie</h1>", unsafe_allow_html=True)
    with st.expander("📤 Poster une photo"):
        # Importante: Pedimos quién sube la foto para la medalla
        uploader = st.selectbox("Qui poste ?", df_eleves['Pseudo'].unique()) 
        team_aff = st.selectbox("Pour quelle équipe ?", df_teams['TeamName'].unique())
        caption = st.text_input("Description")
        uploaded_file = st.file_uploader("Image", type=['png', 'jpg'])
        if st.button("Publier") and uploaded_file and uploader:
            bytes_data = uploaded_file.getvalue()
            b64_str = base64.b64encode(bytes_data).decode()
            new_img = pd.DataFrame([[team_aff, uploader, b64_str, caption, datetime.now().strftime("%d/%m")]], columns=df_gallery.columns)
            df_gallery = pd.concat([new_img, df_gallery], ignore_index=True)
            save_data(df_gallery, FILE_GALLERY)
            auto_post("Nouvelle Photo 📸", f"{uploader} ({team_aff}) a partagé un souvenir.", "Photo 📸")
            st.balloons()
            st.rerun()

    st.write("---")
    if not df_gallery.empty:
        cols = st.columns(2)
        for i, row in df_gallery.iterrows():
            with cols[i % 2]:
                st.markdown(f"""
                <div class="photo-card">
                    <img src="data:image/png;base64,{row['ImageB64']}" style="width:100%; border-radius:10px;">
                    <p style="color:black;"><strong>{row['TeamName']}</strong><br>{row['Caption']}</p>
                    <small>Par: {row['Uploader']}</small>
                </div>""", unsafe_allow_html=True)

# --- 5. JOURNAL ---
elif st.session_state['page'] == 'journal':
    st.markdown("<h1>📖 Mon Journal</h1>", unsafe_allow_html=True)
    st.caption("Espace privé. Seul le prof peut lire ceci.")
    
    with st.form("journal_entry"):
        author = st.selectbox("C'est qui ?", df_eleves['Pseudo'].unique())
        mood_day = st.selectbox("Ressenti global", ["Super", "Bien", "Fatigué", "Triste"])
        reflexion = st.text_area("Qu'as-tu fait aujourd'hui ?", height=150)
        
        if st.form_submit_button("🔒 Enregistrer"):
            if author and reflexion:
                new_entry = pd.DataFrame([[author, datetime.now().strftime("%d/%m %H:%M"), reflexion, mood_day]], 
                                       columns=['Pseudo', 'Date', 'Reflexion', 'Humeur'])
                df_journal = pd.concat([new_entry, df_journal], ignore_index=True)
                save_data(df_journal, FILE_JOURNAL)
                st.success("Enregistré !")
            else: st.error("Écris quelque chose !")

# --- NAVEGACIÓN INFERIOR ---
st.markdown("---")
cols = st.columns(6)
labels = ["🏠", "👤", "🛡️", "📸", "📖", "🏆"]
pages = ['home', 'profile', 'teams', 'gallery', 'journal', 'awards']
for col, label, page in zip(cols, labels, pages):
    with col:
        if st.button(label, key=f"nav_{page}"): nav(page)

if st.session_state['page'] == 'awards':
    st.markdown("<h1>🏆 Oscars</h1>", unsafe_allow_html=True)
    st.info("Vote final bientôt !")
