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

# --- 2. CSS "COMIC BOOK SPORTS" ---
st.markdown("""
<style>
    /* Fuente estilo cómic para títulos + fuente legible para texto */
    @import url('https://fonts.googleapis.com/css2?family=Bangers&family=Poppins:wght@400;700;900&display=swap');

    :root {
        --primary: #4D79FF;
        --accent: #FFD93D;
        --text: #2D3436;
        --card-bg: #FFFFFF;
    }

    /* --- CAMBIO PRINCIPAL: FONDO DE CÓMIC --- */
    .stApp {
        /* IMPORTANTE: REEMPLAZA ESTA URL POR TU IMAGEN DE CÓMIC DE DEPORTES */
        /* He puesto una de ejemplo estilo pop-art genérico */
        background-image: url('https://img.freepik.com/free-vector/pop-art-comic-background_23-2148566476.jpg?w=1380&t=st=1708125000~exp=1708125600~hmac=example_token');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Poppins', sans-serif; /* Fuente base legible */
    }
    
    /* CAPA BLANCA FUERTE PARA LEGIBILIDAD (CRÍTICO EN FONDOS DE CÓMIC) */
    .stApp::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(255, 255, 255, 0.94); /* 94% opaco para tapar bien el fondo ruidoso */
        z-index: -1;
        backdrop-filter: blur(2px); /* Un poco de desenfoque extra ayuda */
    }

    /* TARJETAS CON BORDE DE VIÑETA GRUESO */
    .css-1r6slb0, .stDataFrame, .stForm, div[data-testid="stExpander"], .news-card, .photo-card, .mood-card, .trophy-case {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 20px;
        /* Borde negro grueso tipo cómic */
        border: 3px solid black;
        /* Sombra sólida desplazada (pop art) */
        box-shadow: 6px 6px 0px rgba(0,0,0,1);
        margin-bottom: 25px;
    }

    /* HERO HEADER ESTILO TÍTULO DE CÓMIC */
    .hero-header {
        background: linear-gradient(45deg, #4D79FF, #00C6FF);
        padding: 30px 20px;
        border-radius: 0 0 20px 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        border-bottom: 5px solid black;
        box-shadow: 0 10px 0 rgba(0,0,0,0.2);
    }
    .hero-header h1 { 
        font-family: 'Bangers', cursive; /* Fuente de cómic */
        font-weight: 400; 
        font-size: 3rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 3px 3px 0px black; /* Sombra dura de texto */
    }
    .hero-header p {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
    }

    /* TEXTOS */
    h1, h2, h3, h4 { color: black !important; font-family: 'Bangers', cursive; letter-spacing: 1px; }
    p, label, .stMarkdown { color: black !important; font-weight: 600; }

    /* BOTONES "POW!" */
    .stButton > button {
        background: #FFD93D;
        color: black;
        border-radius: 8px;
        border: 3px solid black;
        border-bottom: 6px solid black;
        padding: 12px;
        font-family: 'Bangers', cursive;
        font-size: 1.2rem;
        text-transform: uppercase;
        width: 100%;
        transition: all 0.1s;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        background: #FFE066;
        box-shadow: 0 3px 0 black;
    }
    
    .stButton > button:active {
        transform: translateY(4px);
        border-bottom: 3px solid black;
    }
    
    /* Inputs con borde grueso */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background: #FFF;
        border: 3px solid black;
        border-radius: 8px;
        color: black;
        font-weight: 700;
    }

</style>
""", unsafe_allow_html=True)

# --- 3. BASE DE DATOS ---
FILE_ELEVES = 'eleves.csv'
FILE_TEAMS = 'teams.csv'
FILE_GALLERY = 'gallery.csv'
FILE_NEWS = 'news_feed.csv'
FILE_JOURNAL = 'journal.csv'
FILE_SUGGESTIONS = 'suggestions.csv'

def init_db():
    cols_eleves = ['Pseudo', 'Avatar', 'Forces', 'Faiblesse', 'TeamName']
    cols_teams = ['TeamName', 'Slogan', 'MembersCount', 'Points']
    cols_gallery = ['TeamName', 'Uploader', 'ImageB64', 'Caption', 'Date']
    cols_news = ['Date', 'Titre', 'Contenu', 'Type']
    cols_journal = ['Pseudo', 'Date', 'Reflexion', 'Humeur']
    cols_sugg = ['Date', 'Pseudo', 'Type', 'Message']

    for file, cols in [(FILE_ELEVES, cols_eleves), (FILE_TEAMS, cols_teams), 
                       (FILE_GALLERY, cols_gallery), (FILE_NEWS, cols_news), 
                       (FILE_JOURNAL, cols_journal), (FILE_SUGGESTIONS, cols_sugg)]:
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
df_sugg = load_data(FILE_SUGGESTIONS)

def auto_post(title, content, type_msg="Info 📢"):
    global df_news
    df_news = load_data(FILE_NEWS)
    new_n = pd.DataFrame([[datetime.now().strftime("%d/%m %H:%M"), title, content, type_msg]],
                       columns=['Date', 'Titre', 'Contenu', 'Type'])
    df_news = pd.concat([new_n, df_news], ignore_index=True)
    save_data(df_news, FILE_NEWS)

def get_medals(pseudo):
    medals = []
    medals.append({"icon": "🥇", "name": "Début", "desc": "Profil créé", "unlocked": True})
    user_data = df_eleves[df_eleves['Pseudo'] == pseudo]
    has_team = False
    if not user_data.empty:
        team = user_data.iloc[0]['TeamName']
        if team and team != "None" and str(team) != "nan": has_team = True
    medals.append({"icon": "🛡️", "name": "Squad", "desc": "Rejoint une équipe", "unlocked": has_team})
    has_photo = pseudo in df_gallery['Uploader'].values if 'Uploader' in df_gallery.columns else False
    medals.append({"icon": "📸", "name": "Reporter", "desc": "Photo postée", "unlocked": has_photo})
    has_journal = pseudo in df_journal['Pseudo'].values
    medals.append({"icon": "✍️", "name": "Pensée", "desc": "Journal écrit", "unlocked": has_journal})
    return medals

# --- 4. NAVEGACIÓN ---
if 'page' not in st.session_state: st.session_state['page'] = 'home'
def nav(page_name): 
    st.session_state['page'] = page_name
    st.rerun()

# --- SIDEBAR PROFESOR & BUZÓN ---
with st.sidebar:
    st.markdown("### 📬 Boîte à Idées")
    with st.expander("Une idée ? Un problème ?"):
        with st.form("suggestion_box"):
            s_who = st.selectbox("C'est qui ?", ["Anonyme"] + list(df_eleves['Pseudo'].unique()))
            s_type = st.selectbox("Sujet", ["💡 Idée géniale", "🐛 Problème", "❓ Question"])
            s_msg = st.text_area("Ton message...")
            if st.form_submit_button("Envoyer au Prof"):
                if s_msg:
                    new_s = pd.DataFrame([[datetime.now().strftime("%d/%m"), s_who, s_type, s_msg]], 
                                       columns=['Date', 'Pseudo', 'Type', 'Message'])
                    df_sugg = pd.concat([new_s, df_sugg], ignore_index=True)
                    save_data(df_sugg, FILE_SUGGESTIONS)
                    st.success("Merci ! Message reçu.")
                else: st.error("Écris quelque chose !")

    st.markdown("---")
    st.header("👨‍🏫 Zone Prof")
    if st.text_input("Code", type="password") == "admin":
        st.success("Admin Connecté")
        tab_journ, tab_sugg = st.tabs(["📖 Journaux", "📬 Idées reçues"])
        with tab_journ:
            if df_journal.empty: st.info("Vide.")
            else:
                student_filter = st.selectbox("Filtrer élève", ["Tous"] + list(df_journal['Pseudo'].unique()))
                view_df = df_journal if student_filter == "Tous" else df_journal[df_journal['Pseudo'] == student_filter]
                for i, row in view_df.iterrows():
                    st.caption(f"{row['Date']} - {row['Pseudo']}")
                    st.write(f"📝 {row['Reflexion']}")
                    st.markdown("---")
        with tab_sugg:
            if df_sugg.empty: st.info("Boîte vide.")
            else:
                for i, row in df_sugg.iterrows():
                    st.write(f"**{row['Type']}** par {row['Pseudo']}")
                    st.info(row['Message'])
        if st.button("Reset News"):
            pd.DataFrame(columns=['Date','Titre','Contenu','Type']).to_csv(FILE_NEWS, index=False)
            st.rerun()

# ==========================================
#              PÁGINAS DE LA APP
# ==========================================

# --- 1. HOME ---
if st.session_state['page'] == 'home':
    st.markdown("""
    <div class="hero-header">
        <h1>🏟️ Le Lycée Olympique</h1>
        <p>Ton espace, tes règles, ton jeu !</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="mood-card">', unsafe_allow_html=True)
    st.markdown("##### 👋 Mood du jour ?")
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("🤩"): st.toast("Top !", icon="🔥")
    if c2.button("🙂"): st.toast("Cool", icon="👍")
    if c3.button("😐"): st.toast("Bof", icon="😐")
    if c4.button("😴"): st.toast("Fatigué", icon="💤")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 📢 Quoi de neuf ?")
    if df_news.empty: st.info("Le lycée est calme...")
    for i, row in df_news.iterrows():
        icon = "📢"
        if "Équipe" in str(row['Type']): icon = "🛡️"
        if "Photo" in str(row['Type']): icon = "📸"
        st.markdown(f"""
        <div class="news-card">
            <div style="display:flex; justify-content:space-between; color:#666; font-size:0.8rem;">
                <span>{icon} {row['Type']}</span><span>{row['Date']}</span>
            </div>
            <h3 style="color:#4D79FF; margin:5px 0;">{row['Titre']}</h3>
            <p>{row['Contenu']}</p>
        </div>""", unsafe_allow_html=True)

# --- 2. PERFIL ---
elif st.session_state['page'] == 'profile':
    st.markdown("<h1>👤 Mon Avatar</h1>", unsafe_allow_html=True)
    st.markdown('<div class="css-1r6slb0">', unsafe_allow_html=True)
    with st.form("my_profile"):
        c1, c2 = st.columns([1,2])
        with c1: 
            av = st.selectbox("Avatar", ["🦊","🦁","🐯","🦄","🐲","⚡","🔥","🚀","🤖","👽","🦸","🥷"])
            st.markdown(f"<div style='font-size:50px;text-align:center'>{av}</div>", unsafe_allow_html=True)
        with c2: ps = st.text_input("Pseudo")
        forces = st.multiselect("Forces", ["Vitesse","Force","Stratégie","Endurance","Créativité"])
        if st.form_submit_button("💾 Sauvegarder"):
            if ps and forces:
                if ps not in df_eleves['Pseudo'].values:
                    new = pd.DataFrame([[ps, av, ",".join(forces), "", "None"]], columns=df_eleves.columns)
                    df_eleves = pd.concat([df_eleves, new], ignore_index=True)
                    save_data(df_eleves, FILE_ELEVES)
                    auto_post(f"Nouvel Élève !", f"{ps} ({av}) a rejoint le lycée !", "Bienvenue 👋")
                    st.success("Profil créé !")
                else: st.success(f"Salut {ps} !")
    st.markdown('</div>', unsafe_allow_html=True)

    if ps: 
        st.markdown("### 🏆 Mes Trophées")
        st.markdown('<div class="trophy-case">', unsafe_allow_html=True)
        my_medals = get_medals(ps)
        cols = st.columns(len(my_medals))
        for idx, medal in enumerate(my_medals):
            with cols[idx]:
                icon = medal['icon'] if medal['unlocked'] else "🔒"
                color = "black" if medal['unlocked'] else "gray"
                st.markdown(f"<div style='text-align:center; color:{color}; font-size:30px; filter:drop-shadow(2px 2px 0px black);'>{icon}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='text-align:center; font-size:10px; font-weight:bold;'>{medal['name']}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 3. EQUIPOS ---
elif st.session_state['page'] == 'teams':
    st.markdown("<h1>🛡️ Les Équipes</h1>", unsafe_allow_html=True)
    tab_create, tab_join = st.tabs(["✨ Créer", "🤝 Rejoindre"])
    with tab_create:
        with st.form("create_team"):
            st.write("Fonde ta squad !")
            t_name = st.text_input("Nom de l'Équipe"); t_slogan = st.text_input("Slogan")
            leader_name = st.selectbox("Chef d'équipe", df_eleves['Pseudo'].unique())
            if st.form_submit_button("🔥 Go !"):
                if t_name and t_slogan:
                    if t_name not in df_teams['TeamName'].values:
                        new_t = pd.DataFrame([[t_name, t_slogan, 1, 0]], columns=df_teams.columns)
                        df_teams = pd.concat([df_teams, new_t], ignore_index=True)
                        save_data(df_teams, FILE_TEAMS)
                        idx = df_eleves[df_eleves['Pseudo'] == leader_name].index[0]
                        df_eleves.at[idx, 'TeamName'] = t_name
                        save_data(df_eleves, FILE_ELEVES)
                        auto_post(f"Nouvelle Équipe : {t_name} !", f"Slogan : « {t_slogan} »", "Équipe 🛡️")
                        st.balloons()
                    else: st.error("Nom pris.")
    with tab_join:
        if df_teams.empty: st.warning("Aucune équipe.")
        for i, row in df_teams.iterrows():
            with st.expander(f"🛡️ {row['TeamName']}"):
                st.markdown(f"**« {row['Slogan']} »**")
                members = df_eleves[df_eleves['TeamName'] == row['TeamName']]['Pseudo'].tolist()
                st.write(f"Membres: {', '.join(members)}")
                me = st.selectbox(f"Moi...", df_eleves['Pseudo'].unique(), key=f"j_{i}")
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
        uploader = st.selectbox("Qui poste ?", df_eleves['Pseudo'].unique()) 
        team_aff = st.selectbox("Pour quelle équipe ?", df_teams['TeamName'].unique())
        caption = st.text_input("Description"); uploaded_file = st.file_uploader("Image", type=['png', 'jpg'])
        if st.button("Publier") and uploaded_file and uploader:
            bytes_data = uploaded_file.getvalue()
            b64_str = base64.b64encode(bytes_data).decode()
            new_img = pd.DataFrame([[team_aff, uploader, b64_str, caption, datetime.now().strftime("%d/%m")]], columns=df_gallery.columns)
            df_gallery = pd.concat([new_img, df_gallery], ignore_index=True)
            save_data(df_gallery, FILE_GALLERY)
            auto_post("Nouvelle Photo 📸", f"{uploader} ({team_aff}) a partagé un souvenir.", "Photo 📸")
            st.balloons(); st.rerun()
    st.write("---")
    if not df_gallery.empty:
        cols = st.columns(2)
        for i, row in df_gallery.iterrows():
            with cols[i % 2]:
                st.markdown(f"""<div class="photo-card">
                    <img src="data:image/png;base64,{row['ImageB64']}" style="width:100%; border-radius:10px; border:2px solid #000;">
                    <p style="color:black; margin-top:5px;"><strong>{row['TeamName']}</strong><br>{row['Caption']}</p></div>""", unsafe_allow_html=True)

# --- 5. JOURNAL ---
elif st.session_state['page'] == 'journal':
    st.markdown("<h1>📖 Mon Journal</h1>", unsafe_allow_html=True)
    st.info("🔒 Espace privé.")
    with st.form("journal_entry"):
        author = st.selectbox("Identité", df_eleves['Pseudo'].unique())
        mood_day = st.selectbox("Ressenti", ["Super", "Bien", "Fatigué", "Triste", "Fier"])
        reflexion = st.text_area("Bilan de la séance :")
        if st.form_submit_button("Enregistrer"):
            if author and reflexion:
                new_entry = pd.DataFrame([[author, datetime.now().strftime("%d/%m %H:%M"), reflexion, mood_day]], columns=['Pseudo', 'Date', 'Reflexion', 'Humeur'])
                df_journal = pd.concat([new_entry, df_journal], ignore_index=True)
                save_data(df_journal, FILE_JOURNAL)
                st.success("Enregistré !")

# --- NAVEGACIÓN ---
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
