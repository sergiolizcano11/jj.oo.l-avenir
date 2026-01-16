import streamlit as st
import pandas as pd
import os
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import random
from st_audiorec import st_audiorec 
from gtts import gTTS
import time

# --- 1. CONFIGURACIÓN DE PÁGINA (MOBILE FIRST) ---
st.set_page_config(
    page_title="L'Alliance App",
    page_icon="🏅",
    layout="centered", # Importante para simular móvil
    initial_sidebar_state="collapsed" 
)

# --- 2. INYECCIÓN DE CSS "ESTILO APP NATIVA" ---
st.markdown("""
<style>
    /* IMPORTAR FUENTE POPPINS */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');

    /* VARIABLES DE TEMA (NEO-POP) */
    :root {
        --primary: #4D79FF;
        --accent: #FFD93D;
        --success: #6BCB77;
        --bg-app: #F0F2F5;
        --card-bg: #FFFFFF;
        --text-main: #2D3436;
    }

    /* ESTRUCTURA GENERAL */
    .stApp {
        background-color: var(--bg-app);
        font-family: 'Poppins', sans-serif;
    }
    
    /* OCULTAR ELEMENTOS DE STREAMLIT (HEADER, FOOTER) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* TITULOS */
    h1 {
        color: var(--text-main);
        font-weight: 800 !important;
        letter-spacing: -1px;
        text-align: center;
        margin-bottom: 20px;
    }

    /* TARJETAS FLOTANTES (CARDS) */
    .css-1r6slb0, .stDataFrame, .stForm, div[data-testid="stExpander"] {
        background: var(--card-bg);
        border-radius: 25px; /* Bordes muy redondos */
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08); /* Sombra suave */
        border: none;
        margin-bottom: 20px;
    }

    /* INPUTS DE TEXTO ESTILO iOS */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #F8F9FA;
        border: 2px solid #E9ECEF;
        border-radius: 15px;
        padding: 10px;
        color: var(--text-main);
    }
    .stTextInput input:focus {
        border-color: var(--primary);
        box-shadow: none;
    }

    /* BOTONES MODERNOS (PILLS) */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary), #3a60d0);
        color: white;
        border-radius: 50px;
        border: none;
        padding: 15px 25px;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        box-shadow: 0 5px 15px rgba(77, 121, 255, 0.3);
        transition: transform 0.1s, box-shadow 0.1s;
    }
    .stButton > button:active {
        transform: scale(0.96);
        box-shadow: 0 2px 10px rgba(77, 121, 255, 0.2);
    }

    /* BOTONES DE NAVEGACIÓN (ICONOS GRANDES) */
    div.row-widget.stButton {
        text-align: center;
    }
    
    /* AVATAR STYLE */
    .avatar-display {
        font-size: 60px;
        background: white;
        width: 100px;
        height: 100px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        border: 4px solid var(--primary);
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0% { transform: translatey(0px); }
        50% { transform: translatey(-10px); }
        100% { transform: translatey(0px); }
    }
    
    /* ALERTAS (TOASTS) MÁS BONITAS */
    div[data-testid="stToast"] {
        border-radius: 50px;
        background-color: var(--text-main);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. GESTIÓN DE DATOS ---
FILE_ELEVES = 'eleves.csv'
FILE_PROPOSALS = 'propositions.csv'
FILE_VOTES = 'votes_finaux.csv'
FILE_EVAL_PROF = 'evaluation_prof.csv' 
FILE_METEO = 'meteo_eleves.csv'

def init_db():
    cols_eleves = ['Pseudo', 'Avatar', 'Forces', 'Faiblesse', 'Slogan', 'TeamID']
    cols_props = ['Demandeur', 'Partenaire', 'Justification', 'Votes_Pour', 'Votes_Contre', 'Status', 'Nom_Epreuve']
    cols_votes = ['Votante', 'Equite', 'FairPlay', 'Innovation', 'Francophonie']
    cols_eval = ['Equipe', 'Nom_Epreuve', 'Stars_Epreuve', 'Stars_Eleve1', 'Stars_Eleve2', 'Commentaire']
    cols_meteo = ['Pseudo', 'Humeur', 'Besoin_Aide', 'Date']

    for file, cols in [(FILE_ELEVES, cols_eleves), (FILE_PROPOSALS, cols_props), 
                       (FILE_VOTES, cols_votes), (FILE_EVAL_PROF, cols_eval), (FILE_METEO, cols_meteo)]:
        if not os.path.exists(file):
            pd.DataFrame(columns=cols).to_csv(file, index=False)
        else:
            df = pd.read_csv(file)
            if not set(cols).issubset(df.columns):
                for c in cols:
                    if c not in df.columns: df[c] = ""
                df.to_csv(file, index=False)

def load_data(file): return pd.read_csv(file)
def save_data(df, file): df.to_csv(file, index=False)

init_db()
df_eleves = load_data(FILE_ELEVES)
df_proposals = load_data(FILE_PROPOSALS)
df_votes = load_data(FILE_VOTES)
df_eval = load_data(FILE_EVAL_PROF)
df_meteo = load_data(FILE_METEO)

# --- 4. HERRAMIENTAS AUDIO ---
def speak_text(text, key_id):
    try:
        tts = gTTS(text=text, lang='fr')
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        b64 = base64.b64encode(mp3_fp.read()).decode()
        # Reproductor minimalista
        md = f"""
            <audio controls style="width: 100%; border-radius: 20px;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)
    except:
        st.toast("Mode silencieux (Audio hors ligne)")

def create_badge(pseudo, avatar):
    W, H = 400, 600
    img = Image.new('RGB', (W, H), color='white')
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (W, 150)], fill='#4D79FF')
    try: font = ImageFont.truetype("arial.ttf", 40)
    except: font = ImageFont.load_default()
    d.text((20, 50), "JO AVENIR", fill="white", font=font)
    d.text((150, 200), avatar, fill="black", font=font)
    d.text((50, 300), pseudo, fill="black", font=font)
    qr = qrcode.QRCode(box_size=4, border=1)
    qr.add_data(f"ID:{pseudo}")
    qr.make(fit=True)
    img.paste(qr.make_image(fill_color="black", back_color="white"), (100, 420))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

# --- 5. NAVEGACIÓN ---
if 'page' not in st.session_state: st.session_state['page'] = 'profile'
def nav(page_name): 
    st.session_state['page'] = page_name
    st.rerun()

# ==========================================
#   SIDEBAR: MÉTÉO + PROF (Oculto en móvil)
# ==========================================
with st.sidebar:
    st.markdown("### 🌦️ Météo Intérieure")
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    mood = None
    if col_m1.button("☀️"): mood = "Super"
    if col_m2.button("⛅"): mood = "Bien"
    if col_m3.button("🌧️"): mood = "Bof"
    if col_m4.button("⛈️"): mood = "Mal"
    
    if mood:
        st.toast(f"Humeur enregistrée: {mood}")
        
    st.markdown("---")
    with st.expander("👨‍🏫 Zone Prof (Admin)"):
        password = st.text_input("Code Secret", type="password")
        if password == "admin2026": 
            st.success("Accès Autorisé")
            st.write("Ici panel d'évaluation...")

# ==========================================
#              CONTENIDO DE LA APP
# ==========================================

# --- PÁGINA 1: PERFIL ---
if st.session_state['page'] == 'profile':
    st.markdown("<h1>👤 Mon Avatar</h1>", unsafe_allow_html=True)
    
    with st.expander("📢 Instructions (Audio)"):
        speak_text("Bienvenue athlète! Crée ton identité pour les Jeux.", "intro")

    # Tarjeta Principal
    st.markdown('<div class="css-1r6slb0">', unsafe_allow_html=True) # Inicio Card Wrapper simulado
    
    c1, c2 = st.columns([1,2])
    
    lista_avatares = ["🦊", "🦁", "🐯", "🐼", "🐨", "🦄", "🐲", "⚡", "🔥", "🚀", "🤖", "👽", "🦸", "🥷", "🧙", "🕵️", "👻"]
    with c1: 
        avatar = st.selectbox("Avatar", lista_avatares, label_visibility="collapsed")
        st.markdown(f"<div class='avatar-display'>{avatar}</div>", unsafe_allow_html=True)
    
    with c2: 
        pseudo = st.text_input("Ton Pseudo", placeholder="Ex: Bolt_Jr")
        st.caption("Choisis un nom de légende !")

    st.markdown("### ⚡ Super-Pouvoirs")
    forces = st.multiselect("Tes Forces", ["Vitesse 🏃‍♂️", "Force 💪", "Stratégie 🧠", "Endurance 🔋", "Charisme ✨"], label_visibility="collapsed")
    
    st.markdown("### 🐢 Point Faible")
    faiblesse = st.text_input("À améliorer", placeholder="Ex: Je suis tête en l'air...", label_visibility="collapsed")
    
    if st.button("💾 Sauvegarder Profil"):
        if pseudo and forces:
            new_user = pd.DataFrame([[pseudo, avatar, ", ".join(forces), faiblesse, "Ready", "None"]], 
                                  columns=['Pseudo', 'Avatar', 'Forces', 'Faiblesse', 'Slogan', 'TeamID'])
            df_eleves = pd.concat([df_eleves, new_user], ignore_index=True)
            save_data(df_eleves, FILE_ELEVES)
            st.toast("Profil Créé avec succès ! 🎉", icon="✅")
            time.sleep(1)
            nav('market')
        else:
            st.toast("Remplis toutes les infos !", icon="⚠️")
    
    st.markdown('</div>', unsafe_allow_html=True) # Fin Card

    # Gestión de Prueba (Solo si tiene equipo)
    st.markdown("### 🔥 Ma Team")
    user_search = st.text_input("Vérifier ma team (Pseudo):")
    if user_search:
        my_team = df_proposals[((df_proposals['Demandeur'] == user_search) | (df_proposals['Partenaire'] == user_search)) & (df_proposals['Status'] == 'Approved')]
        if not my_team.empty:
            row_t = my_team.iloc[0]
            st.success(f"Duo validé avec {row_t['Partenaire'] if row_t['Demandeur'] == user_search else row_t['Demandeur']}")
            
            with st.form("rename_epreuve"):
                st.write(f"Épreuve: **{row_t.get('Nom_Epreuve', 'Non défini')}**")
                new_n = st.text_input("Nouveau nom:")
                if st.form_submit_button("Renommer"):
                    df_proposals.at[row_t.name, 'Nom_Epreuve'] = new_n
                    save_data(df_proposals, FILE_PROPOSALS)
                    st.toast("Nom changé !", icon="✨")
                    st.rerun()

# --- PÁGINA 2: MERCADO ---
elif st.session_state['page'] == 'market':
    st.markdown("<h1>🤝 Le Marché</h1>", unsafe_allow_html=True)
    
    with st.expander("🎧 Écouter la mission"):
        speak_text("Trouve un partenaire qui complète tes forces. Utilise le micro pour expliquer ton choix.", "mkt")

    available = df_eleves[df_eleves['TeamID'] == 'None']

    if available.empty:
        st.info("Tout le monde est en équipe ! 👏")
    else:
        for i, row in available.iterrows():
            with st.container():
                c1, c2 = st.columns([1, 4])
                with c1: st.markdown(f"<div style='font-size:40px; text-align:center;'>{row['Avatar']}</div>", unsafe_allow_html=True)
                with c2: 
                    st.markdown(f"**{row['Pseudo']}**")
                    st.caption(f"⚡ {row['Forces']}")
                
                with st.expander(f"💌 Choisir {row['Pseudo']}"):
                    me = st.text_input(f"Ton Pseudo", key=f"m_{i}")
                    
                    tab_txt, tab_mic = st.tabs(["✍️ Écrire", "🎙️ Parler (Micro d'Or)"])
                    with tab_txt:
                        justif_txt = st.text_area("Pourquoi ?", key=f"t_{i}")
                    with tab_mic:
                        audio_val = st_audiorec(key=f"a_{i}")

                    if st.button(f"Envoyer l'offre 🚀", key=f"b_{i}"):
                        if len(justif_txt) > 2 or audio_val is not None:
                            final_j = justif_txt + (" [🎤 AUDIO]" if audio_val else "")
                            new_p = pd.DataFrame([[me, row['Pseudo'], final_j, 0, 0, "Pending", "Non défini"]],
                                               columns=['Demandeur', 'Partenaire', 'Justification', 'Votes_Pour', 'Votes_Contre', 'Status', 'Nom_Epreuve'])
                            df_proposals = pd.concat([df_proposals, new_p], ignore_index=True)
                            save_data(df_proposals, FILE_PROPOSALS)
                            st.toast("Offre envoyée !", icon="📨")
                        else:
                            st.toast("Dis quelque chose !", icon="❌")

# --- PÁGINA 3: CONSEJO ---
elif st.session_state['page'] == 'council':
    st.markdown("<h1>⚖️ Le Conseil</h1>", unsafe_allow_html=True)
    pending = df_proposals[df_proposals['Status'] == 'Pending']
    
    if pending.empty:
        st.image("https://media.giphy.com/media/26tOZ42MgW6mU/giphy.gif", caption="En attente de duos...")
    else:
        for i, row in pending.iterrows():
            st.markdown(f"### ⚔️ {row['Demandeur']} & {row['Partenaire']}")
            st.info(f"💬 \"{row['Justification']}\"")
            
            c1, c2 = st.columns(2)
            if c1.button("✅ VALIDER", key=f"y{i}"):
                df_proposals.at[i, 'Votes_Pour'] += 1
                if df_proposals.at[i, 'Votes_Pour'] >= 3:
                    df_proposals.at[i, 'Status'] = 'Approved'
                    st.balloons()
                save_data(df_proposals, FILE_PROPOSALS)
                st.rerun()
                
            if c2.button("❌ REFUSER", key=f"n{i}"):
                df_proposals.at[i, 'Votes_Contre'] += 1
                save_data(df_proposals, FILE_PROPOSALS)
                st.rerun()

# --- PÁGINA 4: RECURSOS ---
elif st.session_state['page'] == 'resources':
    st.markdown("<h1>🧠 Zone Savoir</h1>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["📚 Dico", "🌍 Culture"])
    
    with t1:
        c1, c2 = st.columns(2)
        with c1:
            st.image("https://img.icons8.com/color/96/running.png", width=60)
            if st.button("🔊 Courir"): speak_text("Courir. Je cours vite.", "r")
        with c2:
            st.image("https://img.icons8.com/color/96/medal.png", width=60)
            if st.button("🔊 Médaille"): speak_text("La médaille d'or.", "m")
            
    with t2:
        fact = random.choice(["Les premiers JO: Grèce, 776 av. JC.", "La flamme ne s'éteint jamais."])
        st.info(f"💡 {fact}")
        if st.button("🔊 Lire l'info"): speak_text(fact, "f")

# --- PÁGINA 5: BADGE ---
elif st.session_state['page'] == 'badge':
    st.markdown("<h1>🆔 Passeport</h1>", unsafe_allow_html=True)
    user = st.text_input("Ton Pseudo pour le badge:")
    if user:
        u = df_eleves[df_eleves['Pseudo'] == user]
        if not u.empty:
            img = create_badge(user, u.iloc[0]['Avatar'])
            st.image(img)
            st.download_button("Télécharger PNG", img, "badge.png", "image/png")

# --- PÁGINA 6: PREMIOS ---
elif st.session_state['page'] == 'awards':
    st.markdown("<h1>🏆 Les Oscars</h1>", unsafe_allow_html=True)
    st.caption("Vote pour le meilleur duo !")
    # (Lógica resumida)
    approved = df_proposals[df_proposals['Status'] == 'Approved']
    if not approved.empty:
        opts = [f"{r['Demandeur']} & {r['Partenaire']}" for i,r in approved.iterrows()]
        vote = st.selectbox("Meilleur Esprit d'Équipe", opts)
        if st.button("Voter"): st.balloons()

# --- NAVEGACIÓN INFERIOR (ESTILO DOCK/APP) ---
st.markdown("---")
# Usamos columnas vacías a los lados para centrar si es escritorio, o llenar en móvil
cols = st.columns(6)
labels = ["👤", "🤝", "⚖️", "🧠", "🆔", "🏆"]
pages = ['profile', 'market', 'council', 'resources', 'badge', 'awards']

for col, label, page in zip(cols, labels, pages):
    with col:
        # Si la página es la actual, usamos un estilo diferente (simulado)
        if st.button(label, key=f"nav_{page}"):
            nav(page)
