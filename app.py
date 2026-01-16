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

# --- 1. CONFIGURACIÓN (WIDE MODE PARA GALERÍA) ---
st.set_page_config(
    page_title="Le Village Olympique",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="collapsed" 
)

# --- 2. CSS "IMPACTANTE" (FONDO + GLASSMORPHISM) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');

    :root {
        --primary: #4D79FF;
        --accent: #FFD93D;
        --text: #2D3436;
    }

    /* FONDO LLAMATIVO */
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1461896836934-ffe607ba8211?q=80&w=2070&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Poppins', sans-serif;
    }
    
    /* CAPA OSCURA PARA LEER TEXTO */
    .stApp::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(255, 255, 255, 0.85); /* Capa blanca semitransparente */
        z-index: -1;
    }

    /* TARJETAS GLASSMORPHISM */
    .css-1r6slb0, .stDataFrame, .stForm, div[data-testid="stExpander"], .news-card, .photo-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 20px;
    }

    /* HERO HEADER */
    .hero-header {
        background: linear-gradient(135deg, #4D79FF, #00C6FF);
        padding: 30px;
        border-radius: 0 0 40px 40px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        animation: slideDown 0.8s ease-out;
    }
    
    @keyframes slideDown {
        from { transform: translateY(-50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    /* ESTILOS DE NOTICIAS */
    .news-card h3 { margin-top: 0; color: #4D79FF; }
    .news-meta { font-size: 0.8rem; color: #666; display: flex; justify-content: space-between; }
    
    /* SLOGAN */
    .team-slogan {
        font-style: italic;
        color: #FF6B6B;
        font-weight: 600;
        font-size: 0.9rem;
    }

    /* BOTONES */
    .stButton > button {
        background: var(--primary); color: white; border-radius: 50px; 
        padding: 12px; font-weight: 600; border: none; width: 100%;
        box-shadow: 0 4px 15px rgba(77, 121, 255, 0.4);
        transition: transform 0.2s;
    }
    .stButton > button:hover { transform: scale(1.02); }

</style>
""", unsafe_allow_html=True)

# --- 3. BASE DE DATOS REFACTORIZADA (EQUIPOS MULTIPLES) ---
FILE_ELEVES = 'eleves.csv'
FILE_TEAMS = 'teams.csv'     # NUEVO: Gestión de equipos
FILE_GALLERY = 'gallery.csv' # NUEVO: Fotos
FILE_NEWS = 'news_feed.csv'
FILE_METEO = 'meteo.csv'

def init_db():
    # Alumnos: Ahora tienen 'TeamName' en vez de TeamID complejo
    cols_eleves = ['Pseudo', 'Avatar', 'Forces', 'Faiblesse', 'TeamName']
    # Equipos: Nombre, Slogan, Puntos
    cols_teams = ['TeamName', 'Slogan', 'MembersCount', 'Points']
    # Galería: Foto en Base64
    cols_gallery = ['TeamName', 'ImageB64', 'Caption', 'Date']
    cols_news = ['Date', 'Titre', 'Contenu', 'Type']
    cols_meteo = ['Pseudo', 'Mood', 'Date']

    for file, cols in [(FILE_ELEVES, cols_eleves), (FILE_TEAMS, cols_teams), 
                       (FILE_GALLERY, cols_gallery), (FILE_NEWS, cols_news), (FILE_METEO, cols_meteo)]:
        if not os.path.exists(file):
            pd.DataFrame(columns=cols).to_csv(file, index=False)
        else:
            # Reparación simple
            df = pd.read_csv(file)
            for c in cols:
                if c not in df.columns: df[c] = "" if c != 'Points' and c != 'MembersCount' else 0
            df.to_csv(file, index=False)

def load_data(file): return pd.read_csv(file)
def save_data(df, file): df.to_csv(file, index=False)

init_db()
df_eleves = load_data(FILE_ELEVES)
df_teams = load_data(FILE_TEAMS)
df_gallery = load_data(FILE_GALLERY)
df_news = load_data(FILE_NEWS)

# --- 4. FUNCIÓN AUTOMÁTICA: POSTEAR EN EL MURO ---
def auto_post(title, content, type_msg="Info 📢"):
    """Publica automáticamente en el muro sin intervención manual"""
    global df_news
    # Recargar por si acaso
    df_news = load_data(FILE_NEWS)
    new_n = pd.DataFrame([[datetime.now().strftime("%d/%m %H:%M"), title, content, type_msg]],
                       columns=['Date', 'Titre', 'Contenu', 'Type'])
    df_news = pd.concat([new_n, df_news], ignore_index=True)
    save_data(df_news, FILE_NEWS)

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
        <h1>🔥 Le Village Olympique</h1>
        <p>Actualités, Défis et Victoires en direct !</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Météo rápida
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("🤩"): 
        st.toast("Super énergie !")
        # Aquí podrías guardar el mood
    if c4.button("😴"): st.toast("Repos nécessaire...")

    st.markdown("### 📢 Le Mur (En Direct)")
    
    if df_news.empty:
        st.info("Le village est calme... Soyez les premiers à faire du bruit !")
    
    for i, row in df_news.iterrows():
        # Icono según tipo
        icon = "📢"
        if "Équipe" in str(row['Type']): icon = "🛡️"
        if "Photo" in str(row['Type']): icon = "📸"
        
        st.markdown(f"""
        <div class="news-card">
            <div class="news-meta">
                <span>{icon} {row['Type']}</span>
                <span>{row['Date']}</span>
            </div>
            <h3>{row['Titre']}</h3>
            <p>{row['Contenu']}</p>
        </div>
        """, unsafe_allow_html=True)

# --- 2. PERFIL (CREACIÓN) ---
elif st.session_state['page'] == 'profile':
    st.markdown("<h1>👤 Mon Athlète</h1>", unsafe_allow_html=True)
    
    with st.form("my_profile"):
        c1, c2 = st.columns([1,2])
        with c1: 
            av = st.selectbox("Avatar", ["🦊","🦁","🐯","🦄","🐲","⚡","🔥","🚀","🤖","👽","🦸","🥷"])
            st.markdown(f"<div style='font-size:50px;text-align:center'>{av}</div>", unsafe_allow_html=True)
        with c2: 
            ps = st.text_input("Pseudo")
        
        forces = st.multiselect("Forces", ["Vitesse","Force","Stratégie","Endurance","Créativité"])
        if st.form_submit_button("💾 Sauvegarder"):
            if ps and forces:
                # Verificar si ya existe
                if ps not in df_eleves['Pseudo'].values:
                    new = pd.DataFrame([[ps, av, ",".join(forces), "", "None"]], columns=df_eleves.columns)
                    df_eleves = pd.concat([df_eleves, new], ignore_index=True)
                    save_data(df_eleves, FILE_ELEVES)
                    # AUTO POST
                    auto_post(f"Nouvel Athlète !", f"{ps} ({av}) a rejoint le village !", "Bienvenue 👋")
                    st.success("Profil créé !")
                else:
                    st.error("Ce pseudo existe déjà !")

# --- 3. EQUIPOS (SQUADS) ---
elif st.session_state['page'] == 'teams':
    st.markdown("<h1>🛡️ Les Équipes (Squads)</h1>", unsafe_allow_html=True)
    
    tab_create, tab_join = st.tabs(["✨ Créer une Équipe", "🤝 Rejoindre"])
    
    # CREAR EQUIPO
    with tab_create:
        with st.form("create_team"):
            st.write("Fonde ta propre alliance !")
            t_name = st.text_input("Nom de l'Équipe (Ex: Les Titans)")
            t_slogan = st.text_input("Slogan de combat (Ex: Toujours plus haut!)")
            leader_name = st.selectbox("Qui est le chef ?", df_eleves['Pseudo'].unique())
            
            if st.form_submit_button("🔥 Fonder l'Équipe"):
                if t_name and t_slogan:
                    if t_name not in df_teams['TeamName'].values:
                        # Crear Equipo
                        new_t = pd.DataFrame([[t_name, t_slogan, 1, 0]], columns=df_teams.columns)
                        df_teams = pd.concat([df_teams, new_t], ignore_index=True)
                        save_data(df_teams, FILE_TEAMS)
                        
                        # Asignar Líder
                        idx = df_eleves[df_eleves['Pseudo'] == leader_name].index[0]
                        df_eleves.at[idx, 'TeamName'] = t_name
                        save_data(df_eleves, FILE_ELEVES)
                        
                        # AUTO POST
                        auto_post(f"Nouvelle Équipe : {t_name} !", f"Slogan : « {t_slogan} »", "Équipe 🛡️")
                        st.balloons()
                        st.success("Équipe créée !")
                    else:
                        st.error("Ce nom d'équipe existe déjà.")

    # UNIRSE A EQUIPO
    with tab_join:
        if df_teams.empty:
            st.warning("Aucune équipe... Créez-en une !")
        else:
            st.write("Choisis ton destin :")
            for i, row in df_teams.iterrows():
                with st.expander(f"🛡️ {row['TeamName']}"):
                    st.markdown(f"<p class='team-slogan'>« {row['Slogan']} »</p>", unsafe_allow_html=True)
                    
                    # Ver miembros actuales
                    members = df_eleves[df_eleves['TeamName'] == row['TeamName']]['Pseudo'].tolist()
                    st.write(f"👥 Membres ({len(members)}): {', '.join(members)}")
                    
                    # Botón unirse
                    me = st.selectbox(f"Je suis... (pour {row['TeamName']})", df_eleves['Pseudo'].unique(), key=f"join_{i}")
                    if st.button(f"Rejoindre {row['TeamName']}", key=f"btn_{i}"):
                        # Actualizar alumno
                        idx = df_eleves[df_eleves['Pseudo'] == me].index[0]
                        old_team = df_eleves.at[idx, 'TeamName']
                        
                        if old_team != row['TeamName']:
                            df_eleves.at[idx, 'TeamName'] = row['TeamName']
                            save_data(df_eleves, FILE_ELEVES)
                            
                            # AUTO POST
                            auto_post("Transfert !", f"{me} a rejoint l'équipe {row['TeamName']} !", "Recrutement 🤝")
                            st.success(f"Bienvenue chez les {row['TeamName']} !")
                            st.rerun()
                        else:
                            st.warning("Tu y es déjà !")

# --- 4. GALERÍA (SOUVENIRS) ---
elif st.session_state['page'] == 'gallery':
    st.markdown("<h1>📸 Galerie Souvenirs</h1>", unsafe_allow_html=True)
    
    # Subir Foto
    with st.expander("📤 Poster une photo (Préparation)"):
        uploader = st.selectbox("Qui poste ?", df_teams['TeamName'].unique())
        caption = st.text_input("Description")
        uploaded_file = st.file_uploader("Choisis une image", type=['png', 'jpg', 'jpeg'])
        
        if st.button("Publier la photo") and uploaded_file and uploader:
            # Convertir a Base64
            bytes_data = uploaded_file.getvalue()
            b64_str = base64.b64encode(bytes_data).decode()
            
            new_img = pd.DataFrame([[uploader, b64_str, caption, datetime.now().strftime("%d/%m")]], 
                                 columns=df_gallery.columns)
            df_gallery = pd.concat([new_img, df_gallery], ignore_index=True)
            save_data(df_gallery, FILE_GALLERY)
            
            # AUTO POST
            auto_post("Nouvelle Photo 📸", f"L'équipe {uploader} a partagé un souvenir : {caption}", "Photo 📸")
            st.success("Photo publiée !")
            st.rerun()

    # Ver Fotos (Grid)
    st.write("---")
    if df_gallery.empty:
        st.info("La galerie est vide.")
    else:
        cols = st.columns(2) # Grid de 2 columnas
        for i, row in df_gallery.iterrows():
            col = cols[i % 2]
            with col:
                st.markdown(f"""
                <div class="photo-card">
                    <img src="data:image/png;base64,{row['ImageB64']}" style="width:100%; border-radius:10px;">
                    <p><strong>{row['TeamName']}</strong><br>{row['Caption']}</p>
                </div>
                """, unsafe_allow_html=True)

# --- NAVEGACIÓN INFERIOR (DOCK) ---
st.markdown("---")
cols = st.columns(5)
labels = ["🏠 Village", "👤 Profil", "🛡️ Équipes", "📸 Galerie", "🏆 Oscars"]
pages = ['home', 'profile', 'teams', 'gallery', 'awards'] # Awards se mantiene (lógica simple)

for col, label, page in zip(cols, labels, pages):
    with col:
        if st.button(label, key=f"nav_{page}"):
            nav(page)

# Página Awards simplificada para que no de error
if st.session_state['page'] == 'awards':
    st.markdown("<h1>🏆 Oscars</h1>", unsafe_allow_html=True)
    if not df_teams.empty:
        vote = st.selectbox("Meilleur Équipe", df_teams['TeamName'].unique())
        if st.button("Voter"): st.balloons()
