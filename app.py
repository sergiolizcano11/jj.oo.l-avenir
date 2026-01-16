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

# --- 1. CONFIGURACIÓN (MOBILE FIRST) ---
st.set_page_config(
    page_title="Le Village Olympique",
    page_icon="🏟️",
    layout="centered",
    initial_sidebar_state="collapsed" 
)

# --- 2. CSS "RED SOCIAL" (ESTILO PATIO DIGITAL) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');

    :root {
        --primary: #4D79FF;
        --accent: #FFD93D;
        --success: #00C851;
        --bg-app: #F0F2F5;
        --card-bg: #FFFFFF;
        --text: #2D3436;
    }

    .stApp { background-color: var(--bg-app); font-family: 'Poppins', sans-serif; color: var(--text); }
    #MainMenu, footer, header {visibility: hidden;}

    /* ENCABEZADO TIPO RED SOCIAL */
    .hero-header {
        background: linear-gradient(135deg, var(--primary), #8E2DE2);
        padding: 20px;
        border-radius: 0 0 30px 30px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 10px 20px rgba(77, 121, 255, 0.2);
    }
    
    /* TARJETAS DE NOTICIAS (FEED) */
    .news-card {
        background: white;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-left: 5px solid var(--primary);
    }
    
    .challenge-card {
        background: #FFF9E6;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        border: 2px dashed var(--accent);
        text-align: center;
    }

    /* TARJETAS GENERALES DE LA APP */
    .css-1r6slb0, .stDataFrame, .stForm, div[data-testid="stExpander"] {
        background: var(--card-bg);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        border: none;
    }

    /* BOTONES */
    .stButton > button {
        background: var(--primary); color: white; border-radius: 50px; 
        padding: 12px; font-weight: 600; border: none; width: 100%;
        box-shadow: 0 4px 10px rgba(77, 121, 255, 0.3);
    }
    
    /* MENU DE NAVEGACION INFERIOR */
    .nav-container {
        position: fixed; bottom: 0; left: 0; width: 100%; background: white;
        padding: 10px; display: flex; justify-content: space-around;
        border-top: 1px solid #eee; z-index: 999;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. BASE DE DATOS (INCLUYE NOTICIAS) ---
FILE_ELEVES = 'eleves.csv'
FILE_PROPOSALS = 'propositions.csv'
FILE_VOTES = 'votes_finaux.csv'
FILE_EVAL_PROF = 'evaluation_prof.csv' 
FILE_METEO = 'meteo_eleves.csv'
FILE_NEWS = 'news_feed.csv' # NUEVO: Muro de noticias

def init_db():
    cols_eleves = ['Pseudo', 'Avatar', 'Forces', 'Faiblesse', 'Slogan', 'TeamID']
    cols_props = ['Demandeur', 'Partenaire', 'Justification', 'Votes_Pour', 'Votes_Contre', 'Status', 'Nom_Epreuve']
    cols_votes = ['Votante', 'Equite', 'FairPlay', 'Innovation', 'Francophonie']
    cols_eval = ['Equipe', 'Nom_Epreuve', 'Stars_Epreuve', 'Stars_Eleve1', 'Stars_Eleve2', 'Commentaire']
    cols_meteo = ['Pseudo', 'Humeur', 'Besoin_Aide', 'Date']
    cols_news = ['Date', 'Titre', 'Contenu', 'Type', 'Likes'] # Type: Info, Defi, Bravo

    for file, cols in [(FILE_ELEVES, cols_eleves), (FILE_PROPOSALS, cols_props), 
                       (FILE_VOTES, cols_votes), (FILE_EVAL_PROF, cols_eval), 
                       (FILE_METEO, cols_meteo), (FILE_NEWS, cols_news)]:
        if not os.path.exists(file):
            pd.DataFrame(columns=cols).to_csv(file, index=False)
        else:
            df = pd.read_csv(file)
            if not set(cols).issubset(df.columns):
                for c in cols:
                    if c not in df.columns: df[c] = "" if c != 'Likes' else 0
                df.to_csv(file, index=False)

def load_data(file): return pd.read_csv(file)
def save_data(df, file): df.to_csv(file, index=False)

init_db()
df_eleves = load_data(FILE_ELEVES)
df_proposals = load_data(FILE_PROPOSALS)
df_votes = load_data(FILE_VOTES)
df_eval = load_data(FILE_EVAL_PROF)
df_meteo = load_data(FILE_METEO)
df_news = load_data(FILE_NEWS)

# --- 4. HERRAMIENTAS AUDIO/TTS ---
def speak_text(text, key_id):
    try:
        tts = gTTS(text=text, lang='fr')
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        b64 = base64.b64encode(mp3_fp.read()).decode()
        st.markdown(f"""
            <audio controls style="width: 100%; height: 30px; border-radius: 20px;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """, unsafe_allow_html=True)
    except:
        st.caption("🔇 Audio hors ligne")

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
if 'page' not in st.session_state: st.session_state['page'] = 'home' # AHORA EMPIEZA EN HOME
def nav(page_name): 
    st.session_state['page'] = page_name
    st.rerun()

# ==========================================
#   SIDEBAR: SOLO PROFESOR (ADMIN)
# ==========================================
with st.sidebar:
    st.header("👨‍🏫 Zone Prof")
    password = st.text_input("Code Secret", type="password")
    
    if password == "admin2026": 
        st.success("Mode Admin")
        
        # 1. PUBLICAR NOTICIA EN EL MURO
        with st.expander("📢 Publier sur le Mur"):
            with st.form("new_post"):
                p_title = st.text_input("Titre (Ex: Info, Défi)")
                p_content = st.text_area("Message")
                p_type = st.selectbox("Type", ["Info 📢", "Défi 🚀", "Bravo 🌟"])
                if st.form_submit_button("Publier"):
                    new_n = pd.DataFrame([[datetime.now().strftime("%d/%m"), p_title, p_content, p_type, 0]],
                                       columns=['Date', 'Titre', 'Contenu', 'Type', 'Likes'])
                    df_news = pd.concat([new_n, df_news], ignore_index=True) # Poner al principio
                    save_data(df_news, FILE_NEWS)
                    st.success("Publié !")
        
        # 2. EVALUACIÓN (Tu código anterior)
        with st.expander("📝 Évaluation"):
             approved_teams = df_proposals[df_proposals['Status'] == 'Approved']
             if not approved_teams.empty:
                 st.write("Panel d'évaluation actif.")

# ==========================================
#              CONTENIDO DE LA APP
# ==========================================

# --- PÁGINA 1: EL PATIO DIGITAL (HOME) ---
if st.session_state['page'] == 'home':
    # HERO HEADER
    st.markdown("""
    <div class="hero-header">
        <h1>🏟️ Le Village Olympique</h1>
        <p>Bienvenue sur ton patio numérique !</p>
    </div>
    """, unsafe_allow_html=True)

    # 1. MÉTÉO (MOOD TRACKER) EN EL MURO
    st.markdown("##### 👋 Comment ça va aujourd'hui ?")
    c1, c2, c3, c4 = st.columns(4)
    mood_sel = None
    if c1.button("🤩"): mood_sel = "Top"
    if c2.button("🙂"): mood_sel = "Bien"
    if c3.button("😐"): mood_sel = "Moyen"
    if c4.button("😫"): mood_sel = "Mal"
    
    if mood_sel:
        st.toast(f"Humeur notée: {mood_sel}")
        # Guardaríamos en CSV aquí...

    st.markdown("---")
    
    # 2. MURO DE NOTICIAS (FEED)
    st.subheader("📢 Le Mur du Village")
    
    if df_news.empty:
        # Noticia de ejemplo si está vacío
        st.markdown("""
        <div class="news-card">
            <h4>👋 Bienvenue !</h4>
            <p>Ceci est le début de l'aventure. Crée ton profil pour commencer.</p>
            <small>Prof • Aujourd'hui</small>
        </div>
        """, unsafe_allow_html=True)
    
    for i, row in df_news.iterrows():
        # Estilo diferente si es Reto o Info
        card_class = "challenge-card" if "Défi" in row['Type'] else "news-card"
        
        st.markdown(f"""
        <div class="{card_class}">
            <div style="display:flex; justify-content:space-between;">
                <strong>{row['Type']}</strong>
                <small>{row['Date']}</small>
            </div>
            <h3>{row['Titre']}</h3>
            <p>{row['Contenu']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Interacción DUA (Audio) + Like
        c_like, c_audio = st.columns([1, 4])
        with c_like:
            if st.button("❤️", key=f"l_{i}"):
                df_news.at[i, 'Likes'] += 1
                save_data(df_news, FILE_NEWS)
                st.rerun()
        with c_audio:
            if st.button(f"🔊 Écouter", key=f"s_{i}"):
                speak_text(row['Contenu'], f"tts_{i}")

# --- PÁGINA 2: PERFIL ---
elif st.session_state['page'] == 'profile':
    st.markdown("<h1>👤 Mon Avatar</h1>", unsafe_allow_html=True)
    
    # TARJETA DE PERFIL
    st.markdown('<div class="css-1r6slb0">', unsafe_allow_html=True)
    c1, c2 = st.columns([1,2])
    lista_avatares = ["🦊", "🦁", "🐯", "🐼", "🐨", "🦄", "🐲", "⚡", "🔥", "🚀", "🤖", "👽", "🦸", "🥷", "🧙", "🕵️", "👻"]
    with c1: 
        avatar = st.selectbox("Avatar", lista_avatares, label_visibility="collapsed")
        st.markdown(f"<div style='font-size:60px; text-align:center;'>{avatar}</div>", unsafe_allow_html=True)
    with c2: 
        pseudo = st.text_input("Ton Pseudo", placeholder="Ex: Bolt_Jr")
    
    st.write("**Tes Super-Pouvoirs ⚡**")
    forces = st.multiselect("Forces", ["Vitesse", "Force", "Stratégie", "Endurance", "Charisme"], label_visibility="collapsed")
    faiblesse = st.text_input("Point faible", placeholder="À améliorer...")
    
    if st.button("💾 Mettre à jour"):
        if pseudo:
            # Lógica simplificada de guardado
            new_user = pd.DataFrame([[pseudo, avatar, ", ".join(forces), faiblesse, "Ready", "None"]], columns=df_eleves.columns)
            df_eleves = pd.concat([df_eleves, new_user], ignore_index=True)
            save_data(df_eleves, FILE_ELEVES)
            st.toast("Profil Sauvegardé !")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # GESTIONAR EQUIPO
    st.subheader("🔥 Ma Team")
    user_search = st.text_input("Vérifier ma team (Pseudo):")
    if user_search:
        my_team = df_proposals[((df_proposals['Demandeur'] == user_search) | (df_proposals['Partenaire'] == user_search)) & (df_proposals['Status'] == 'Approved')]
        if not my_team.empty:
            row_t = my_team.iloc[0]
            st.success(f"Duo validé avec {row_t['Partenaire'] if row_t['Demandeur'] == user_search else row_t['Demandeur']}")
            st.info(f"Épreuve: {row_t.get('Nom_Epreuve', 'Non défini')}")
            
            with st.form("rename"):
                nn = st.text_input("Renommer l'épreuve:")
                if st.form_submit_button("Changer"):
                    df_proposals.at[row_t.name, 'Nom_Epreuve'] = nn
                    save_data(df_proposals, FILE_PROPOSALS)
                    st.rerun()

# --- PÁGINA 3: MERCADO (MICRO D'OR) ---
elif st.session_state['page'] == 'market':
    st.markdown("<h1>🤝 Le Marché</h1>", unsafe_allow_html=True)
    st.caption("Trouve ton duo. Écris ou parle !")

    available = df_eleves[df_eleves['TeamID'] == 'None']
    if available.empty: st.info("Tout le monde est casé !")
    
    for i, row in available.iterrows():
        with st.expander(f"{row['Avatar']} {row['Pseudo']}"):
            st.write(f"⚡ {row['Forces']}")
            me = st.text_input("Ton Pseudo", key=f"m_{i}")
            
            t1, t2 = st.tabs(["✍️ Écrire", "🎙️ Micro d'Or"])
            with t1: txt = st.text_area("Pourquoi ?", key=f"t_{i}")
            with t2: aud = st_audiorec(key=f"a_{i}")
            
            if st.button("🚀 Proposer", key=f"b_{i}"):
                if len(txt) > 2 or aud:
                    j = txt + (" [🎤 AUDIO]" if aud else "")
                    new_p = pd.DataFrame([[me, row['Pseudo'], j, 0, 0, "Pending", "Non défini"]], columns=df_proposals.columns)
                    df_proposals = pd.concat([df_proposals, new_p], ignore_index=True)
                    save_data(df_proposals, FILE_PROPOSALS)
                    st.success("Envoyé !")

# --- PÁGINA 4: CONSEJO ---
elif st.session_state['page'] == 'council':
    st.markdown("<h1>⚖️ Le Conseil</h1>", unsafe_allow_html=True)
    pending = df_proposals[df_proposals['Status'] == 'Pending']
    
    if pending.empty: st.info("Rien à voter.")
    for i, row in pending.iterrows():
        st.write(f"⚔️ **{row['Demandeur']} & {row['Partenaire']}**")
        st.info(f"💬 {row['Justification']}")
        c1, c2 = st.columns(2)
        if c1.button("✅ OUI", key=f"y{i}"):
            df_proposals.at[i, 'Votes_Pour'] += 1
            if df_proposals.at[i, 'Votes_Pour'] >= 3:
                df_proposals.at[i, 'Status'] = 'Approved'
                st.balloons()
            save_data(df_proposals, FILE_PROPOSALS); st.rerun()
        if c2.button("❌ NON", key=f"n{i}"):
            df_proposals.at[i, 'Votes_Contre'] += 1
            save_data(df_proposals, FILE_PROPOSALS); st.rerun()
        st.markdown("---")

# --- PÁGINA 5: PREMIOS ---
elif st.session_state['page'] == 'awards':
    st.markdown("<h1>🏆 Oscars JO</h1>", unsafe_allow_html=True)
    # Lógica de votación simplificada
    approved = df_proposals[df_proposals['Status'] == 'Approved']
    if not approved.empty:
        opts = [f"{r['Demandeur']} & {r['Partenaire']}" for i, r in approved.iterrows()]
        st.selectbox("Meilleur Fair-Play", opts)
        if st.button("Voter"): st.balloons()

# --- MENÚ DE NAVEGACIÓN INFERIOR (DOCK) ---
st.markdown("---")
cols = st.columns(6)
# Iconos: Home, Perfil, Mercado, Consejo, Badge, Premios
labels = ["🏠", "👤", "🤝", "⚖️", "🆔", "🏆"]
pages = ['home', 'profile', 'market', 'council', 'badge', 'awards']

for col, label, page in zip(cols, labels, pages):
    with col:
        # Estilo visual si es la página activa
        btn_type = "primary" if st.session_state['page'] == page else "secondary"
        if st.button(label, key=f"nav_{page}"):
            nav(page)

# Página Badge oculta en el loop pero accesible
if st.session_state['page'] == 'badge':
    st.markdown("<h1>🆔 Badge</h1>", unsafe_allow_html=True)
    u = st.text_input("Pseudo:")
    if u:
        dat = df_eleves[df_eleves['Pseudo'] == u]
        if not dat.empty:
            img = create_badge(u, dat.iloc[0]['Avatar'])
            st.image(img)
