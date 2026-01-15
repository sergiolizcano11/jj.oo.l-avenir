import streamlit as st
import pandas as pd
import os
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

# --- 1. CONFIGURACIÓN VISUAL Y APP ---
st.set_page_config(
    page_title="L'Alliance Olympique",
    page_icon="🏅",
    layout="centered",
    initial_sidebar_state="expanded" 
)

# --- 2. CSS AVANZADO (DISEÑO GEN Z) ---
st.markdown("""
<style>
    :root { --blue: #4D79FF; --yellow: #FFD93D; --green: #6BCB77; --red: #FF6B6B; --bg: #F4F7F6; }
    .stApp { background-color: var(--bg); font-family: 'Segoe UI', sans-serif; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* TARJETAS */
    .css-1r6slb0, .stDataFrame, .stForm, div[data-testid="stExpander"] {
        background: white; border-radius: 24px; padding: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.05); border: none; margin-bottom: 15px;
    }
    /* BOTONES */
    .stButton > button {
        background: linear-gradient(90deg, var(--blue), #3a60d0); color: white;
        border-radius: 50px; border: none; padding: 12px; font-weight: 700; width: 100%;
    }
    /* AVATAR */
    .avatar-circle {
        font-size: 50px; background: #EFF3FF; width: 90px; height: 90px;
        border-radius: 50%; display: flex; align-items: center; justify-content: center;
        margin: 0 auto; border: 3px solid var(--blue);
    }
    /* METRICAS DE PREMIOS */
    div[data-testid="stMetric"] {
        background-color: #FFF9E6; border: 2px solid #FFD93D; border-radius: 15px;
        padding: 10px; text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. GESTIÓN DE DATOS (DATABASE CON REPARACIÓN AUTOMÁTICA) ---
FILE_ELEVES = 'eleves.csv'
FILE_PROPOSALS = 'propositions.csv'
FILE_VOTES = 'votes_finaux.csv' # NUEVO ARCHIVO

def init_db():
    cols_eleves = ['Pseudo', 'Avatar', 'Forces', 'Faiblesse', 'Slogan', 'TeamID']
    cols_props = ['Demandeur', 'Partenaire', 'Justification', 'Votes_Pour', 'Votes_Contre', 'Status']
    cols_votes = ['Votante', 'Equite', 'FairPlay', 'Innovation', 'Francophonie'] # NUEVAS COLUMNAS

    # 1. Alumnos
    if not os.path.exists(FILE_ELEVES):
        pd.DataFrame(columns=cols_eleves).to_csv(FILE_ELEVES, index=False)
    else:
        df = pd.read_csv(FILE_ELEVES)
        if not set(cols_eleves).issubset(df.columns):
            pd.DataFrame(columns=cols_eleves).to_csv(FILE_ELEVES, index=False)

    # 2. Propuestas
    if not os.path.exists(FILE_PROPOSALS):
        pd.DataFrame(columns=cols_props).to_csv(FILE_PROPOSALS, index=False)
    else:
        df = pd.read_csv(FILE_PROPOSALS)
        if 'Status' not in df.columns:
            df['Status'] = 'Pending'
            df.to_csv(FILE_PROPOSALS, index=False)
            
    # 3. Votos Finales (NUEVO)
    if not os.path.exists(FILE_VOTES):
        pd.DataFrame(columns=cols_votes).to_csv(FILE_VOTES, index=False)

def load_data(file): return pd.read_csv(file)
def save_data(df, file): df.to_csv(file, index=False)

init_db()
df_eleves = load_data(FILE_ELEVES)
df_proposals = load_data(FILE_PROPOSALS)
df_votes = load_data(FILE_VOTES) # Cargar votos

# --- 4. FUNCIÓN GENERADOR DE CARNET ---
def create_badge(pseudo, avatar, role="Athlète"):
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
def nav(page_name): st.session_state['page'] = page_name; st.rerun()

# ==========================================
#   ZONA PROFESOR (SIDEBAR)
# ==========================================
with st.sidebar:
    st.header("👨‍🏫 Zone Prof")
    st.info("Utiliza esto para proyectar en la pizarra.")
    url_app = st.text_input("URL de tu App (Copia del navegador)", "https://share.streamlit.io/...")
    
    if url_app:
        qr_img = qrcode.make(url_app)
        buffer = io.BytesIO()
        qr_img.save(buffer, format="PNG")
        img_bytes = buffer.getvalue()
        st.image(img_bytes, caption="Escanea para entrar a la App", use_container_width=True)
    
    st.markdown("---")
    st.caption("✅ Comp. Digital (Uso de App)")
    st.caption("✅ ODD 16 (Instituciones sólidas)")

# ==========================================
#              PÁGINAS DE LA APP
# ==========================================

# --- PÁGINA 1: PERFIL ---
if st.session_state['page'] == 'profile':
    st.markdown("<h1>👤 Mon Profil</h1>", unsafe_allow_html=True)
    
    with st.form("profile_maker"):
        st.markdown("<div class='avatar-circle'>😎</div>", unsafe_allow_html=True)
        c1, c2 = st.columns([1,3])
        with c1: avatar = st.selectbox("Avatar", ["🦊", "🦁", "🦄", "⚡", "👽", "🤖", "🔥"])
        with c2: pseudo = st.text_input("Ton Pseudo", placeholder="Ex: Flash_Gordon")
        
        st.markdown("### ⚡ Mes Super-Pouvoirs")
        forces = st.multiselect("Forces", ["Vitesse 🏃‍♂️", "Force 💪", "Stratégie 🧠", "Endurance 🔋", "Organisation 📋"], label_visibility="collapsed")
        
        st.markdown("### 🐢 Mon Point Faible")
        faiblesse = st.text_input("Weakness", placeholder="Je suis...", label_visibility="collapsed")
        
        if st.form_submit_button("💾 Sauvegarder"):
            if pseudo and forces:
                new_user = pd.DataFrame([[pseudo, avatar, ", ".join(forces), faiblesse, "Ready", "None"]], 
                                      columns=['Pseudo', 'Avatar', 'Forces', 'Faiblesse', 'Slogan', 'TeamID'])
                df_eleves = pd.concat([df_eleves, new_user], ignore_index=True)
                save_data(df_eleves, FILE_ELEVES)
                st.success("Profil Créé ! Va au Marché.")
            else: st.error("Remplis tout !")

# --- PÁGINA 2: MERCADO ---
elif st.session_state['page'] == 'market':
    st.markdown("<h1>🤝 Le Marché</h1>", unsafe_allow_html=True)
    available_students = df_eleves[df_eleves['TeamID'] == 'None']

    if available_students.empty:
        st.warning("Personne de disponible pour le moment.")
    else:
        for i, row in available_students.iterrows():
            with st.container():
                c1, c2 = st.columns([1, 4])
                with c1: st.markdown(f"<div style='font-size:30px;'>{row['Avatar']}</div>", unsafe_allow_html=True)
                with c2: 
                    st.markdown(f"**{row['Pseudo']}**")
                    st.caption(f"⚡ {row['Forces']} | 🐢 {row['Faiblesse']}")
                
                with st.expander(f"💌 Proposer Alliance à {row['Pseudo']}"):
                    with st.form(f"form_{i}"):
                        me = st.text_input("Ton Pseudo", placeholder="Qui es-tu ?")
                        st.markdown("**Pourquoi ce choix ?**")
                        justif = st.text_area("Justification", placeholder="Je te choisis car...")
                        
                        if st.form_submit_button("🚀 Envoyer"):
                            if len(justif) > 10:
                                new_p = pd.DataFrame([[me, row['Pseudo'], justif, 0, 0, "Pending"]],
                                                   columns=['Demandeur', 'Partenaire', 'Justification', 'Votes_Pour', 'Votes_Contre', 'Status'])
                                df_proposals = pd.concat([df_proposals, new_p], ignore_index=True)
                                save_data(df_proposals, FILE_PROPOSALS)
                                st.success("Envoyé au Conseil !")
                            else: st.error("Trop court ! Explique mieux.")

# --- PÁGINA 3: CONSEJO ---
elif st.session_state['page'] == 'council':
    st.markdown("<h1>⚖️ Le Conseil</h1>", unsafe_allow_html=True)
    pending = df_proposals[df_proposals['Status'] == 'Pending']
    
    if pending.empty:
        st.info("Aucun vote en cours.")
    else:
        for i, row in pending.iterrows():
            st.markdown(f"### ⚔️ {row['Demandeur']} + {row['Partenaire']}")
            st.info(f"🗣️ \"{row['Justification']}\"")
            
            c1, c2 = st.columns(2)
            if c1.button(f"🟢 VALIDÉ ({row['Votes_Pour']})", key=f"y{i}"):
                df_proposals.at[i, 'Votes_Pour'] += 1
                if df_proposals.at[i, 'Votes_Pour'] >= 3:
                    df_proposals.at[i, 'Status'] = 'Approved'
                    st.balloons()
                save_data(df_proposals, FILE_PROPOSALS)
                st.rerun()
            if c2.button(f"🔴 REVOIR ({row['Votes_Contre']})", key=f"n{i}"):
                df_proposals.at[i, 'Votes_Contre'] += 1
                save_data(df_proposals, FILE_PROPOSALS)
                st.rerun()
            st.markdown("---")

# --- PÁGINA 4: BADGE ---
elif st.session_state['page'] == 'badge':
    st.markdown("<h1>🆔 Passeport</h1>", unsafe_allow_html=True)
    user = st.text_input("Ton Pseudo:")
    if user:
        udata = df_eleves[df_eleves['Pseudo'] == user]
        if not udata.empty:
            img = create_badge(user, udata.iloc[0]['Avatar'])
            st.image(img, caption="Badge Officiel")
            st.download_button("⬇️ Télécharger", img, file_name="badge.png", mime="image/png")

# --- PÁGINA 5: PREMIOS (AWARDS) --- [NUEVA SECCIÓN]
elif st.session_state['page'] == 'awards':
    st.markdown("<h1>🏆 Les Oscars JO</h1>", unsafe_allow_html=True)
    
    # Pestañas para Votar vs Ver Resultados
    tab1, tab2 = st.tabs(["🗳️ Je Vote", "📊 Résultats"])
    
    # Obtener lista de equipos aprobados
    approved_teams = df_proposals[df_proposals['Status'] == 'Approved']
    
    if approved_teams.empty:
        st.warning("⚠️ Il faut valider des équipes au Conseil d'abord !")
    else:
        # Formatear nombres de equipos para el selectbox
        team_list = [f"{r['Demandeur']} & {r['Partenaire']}" for i, r in approved_teams.iterrows()]
        
        # --- SUB-PESTAÑA 1: VOTACIÓN ---
        with tab1:
            st.markdown("Vote pour les meilleurs duos ! (Honnêtement 😉)")
            with st.form("voting_form"):
                voter = st.selectbox("Qui vote ?", df_eleves['Pseudo'].unique())
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("⚖️ **Prix de l'Équité (ODD 10)**")
                    st.caption("Le duo le plus inclusif.")
                    v_eq = st.selectbox("Choix 1", team_list, key="v1")
                    
                    st.markdown("💡 **Prix de l'Innovation (ODD 9)**")
                    st.caption("Le duo le plus original.")
                    v_in = st.selectbox("Choix 2", team_list, key="v2")

                with col_b:
                    st.markdown("🤝 **Prix du Fair-Play (ODD 16)**")
                    st.caption("Le respect avant tout.")
                    v_fp = st.selectbox("Choix 3", team_list, key="v3")
                    
                    st.markdown("🗣️ **Prix Francophonie**")
                    st.caption("L'effort en français.")
                    v_fr = st.selectbox("Choix 4", team_list, key="v4")
                
                if st.form_submit_button("📩 Envoyer mes Votes"):
                    # Evitar doble voto (simple check)
                    if voter in df_votes['Votante'].values:
                        st.error("Tu as déjà voté ! 🚫")
                    else:
                        new_vote = pd.DataFrame([[voter, v_eq, v_fp, v_in, v_fr]], 
                                              columns=['Votante', 'Equite', 'FairPlay', 'Innovation', 'Francophonie'])
                        df_votes = pd.concat([df_votes, new_vote], ignore_index=True)
                        save_data(df_votes, FILE_VOTES)
                        st.success("Votes enregistrés ! Merci.")
                        st.balloons()

        # --- SUB-PESTAÑA 2: RESULTADOS ---
        with tab2:
            st.markdown("### 🌟 Le Podium en Direct")
            if df_votes.empty:
                st.info("Attente des votes...")
            else:
                # Función auxiliar para mostrar ganador
                def show_winner(category, emoji, title):
                    if category in df_votes.columns:
                        counts = df_votes[category].value_counts()
                        if not counts.empty:
                            winner = counts.idxmax()
                            votes = counts.max()
                            st.metric(label=f"{emoji} {title}", value=winner, delta=f"{votes} votes")
                            # Gráfica simple
                            st.bar_chart(counts)
                
                show_winner('Equite', '⚖️', "Prix Équité")
                st.markdown("---")
                show_winner('FairPlay', '🤝', "Prix Fair-Play")
                st.markdown("---")
                show_winner('Innovation', '💡', "Prix Innovation")
                st.markdown("---")
                show_winner('Francophonie', '🗣️', "Prix Francophonie")

# --- MENÚ INFERIOR (5 COLUMNAS) ---
st.markdown("---")
n1, n2, n3, n4, n5 = st.columns(5)
with n1: 
    if st.button("👤"): nav('profile')
with n2: 
    if st.button("🤝"): nav('market')
with n3: 
    if st.button("⚖️"): nav('council')
with n4: 
    if st.button("🆔"): nav('badge')
with n5: 
    if st.button("🏆"): nav('awards') # NUEVO BOTÓN
