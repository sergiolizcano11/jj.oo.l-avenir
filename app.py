import streamlit as st
import pandas as pd
import os
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
# --- NUEVO IMPORT PARA AUDIO (DUA) ---
from st_audiorec import st_audiorec 

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

# --- 3. GESTIÓN DE DATOS (DATABASE ACTUALIZADA) ---
FILE_ELEVES = 'eleves.csv'
FILE_PROPOSALS = 'propositions.csv'
FILE_VOTES = 'votes_finaux.csv'
FILE_EVAL_PROF = 'evaluation_prof.csv' 

def init_db():
    cols_eleves = ['Pseudo', 'Avatar', 'Forces', 'Faiblesse', 'Slogan', 'TeamID']
    cols_props = ['Demandeur', 'Partenaire', 'Justification', 'Votes_Pour', 'Votes_Contre', 'Status', 'Nom_Epreuve']
    cols_votes = ['Votante', 'Equite', 'FairPlay', 'Innovation', 'Francophonie']
    cols_eval = ['Equipe', 'Nom_Epreuve', 'Stars_Epreuve', 'Stars_Eleve1', 'Stars_Eleve2', 'Commentaire']

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
        if 'Nom_Epreuve' not in df.columns:
            df['Nom_Epreuve'] = "Non défini"
            df.to_csv(FILE_PROPOSALS, index=False)
        if 'Status' not in df.columns:
            df['Status'] = 'Pending'
            df.to_csv(FILE_PROPOSALS, index=False)
            
    # 3. Votos Finales
    if not os.path.exists(FILE_VOTES):
        pd.DataFrame(columns=cols_votes).to_csv(FILE_VOTES, index=False)

    # 4. Evaluación Profesor
    if not os.path.exists(FILE_EVAL_PROF):
        pd.DataFrame(columns=cols_eval).to_csv(FILE_EVAL_PROF, index=False)

def load_data(file): return pd.read_csv(file)
def save_data(df, file): df.to_csv(file, index=False)

init_db()
df_eleves = load_data(FILE_ELEVES)
df_proposals = load_data(FILE_PROPOSALS)
df_votes = load_data(FILE_VOTES)
df_eval = load_data(FILE_EVAL_PROF)

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
#   ZONA PROFESOR (SIDEBAR + EVALUACIÓN)
# ==========================================
with st.sidebar:
    st.header("👨‍🏫 Zone Prof")
    
    # 1. QR CODE GENERATOR
    with st.expander("📲 QR Code Classe"):
        url_app = st.text_input("URL App", "https://share.streamlit.io/...")
        if url_app:
            qr_img = qrcode.make(url_app)
            buffer = io.BytesIO()
            qr_img.save(buffer, format="PNG")
            st.image(buffer.getvalue(), use_container_width=True)

    st.markdown("---")
    
    # 2. DASHBOARD DE EVALUACIÓN
    st.subheader("📝 Évaluation")
    password = st.text_input("Mot de passe", type="password")
    
    if password == "admin2026": 
        st.success("Mode Prof Actif")
        approved_teams = df_proposals[df_proposals['Status'] == 'Approved']
        
        if approved_teams.empty:
            st.warning("Aucune équipe validée.")
        else:
            team_options = [f"{r['Demandeur']} & {r['Partenaire']}" for i, r in approved_teams.iterrows()]
            selected_team_str = st.selectbox("Choisir Équipe", team_options)
            
            team_row = approved_teams[
                (approved_teams['Demandeur'] + " & " + approved_teams['Partenaire']) == selected_team_str
            ].iloc[0]
            
            p1 = team_row['Demandeur']
            p2 = team_row['Partenaire']
            nom_epreuve = team_row.get('Nom_Epreuve', 'Non défini')
            
            st.info(f"🏅 Épreuve: **{nom_epreuve}**")
            
            with st.form("eval_form"):
                st.markdown("### Notation (Étoiles)")
                st.write(f"⭐ Note de l'Épreuve ({nom_epreuve})")
                stars_epreuve = st.feedback("stars", key="s_epreuve")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"👤 {p1}")
                    stars_p1 = st.feedback("stars", key="s_p1")
                with col2:
                    st.write(f"👤 {p2}")
                    stars_p2 = st.feedback("stars", key="s_p2")
                
                comment = st.text_area("Observations Prof")
                
                if st.form_submit_button("Enregistrer Note"):
                    s_e = (stars_epreuve + 1) if stars_epreuve is not None else 0
                    s_1 = (stars_p1 + 1) if stars_p1 is not None else 0
                    s_2 = (stars_p2 + 1) if stars_p2 is not None else 0
                    
                    new_eval = pd.DataFrame([[selected_team_str, nom_epreuve, s_e, s_1, s_2, comment]], 
                                          columns=['Equipe', 'Nom_Epreuve', 'Stars_Epreuve', 'Stars_Eleve1', 'Stars_Eleve2', 'Commentaire'])
                    df_eval = pd.concat([df_eval, new_eval], ignore_index=True)
                    save_data(df_eval, FILE_EVAL_PROF)
                    st.success("Évaluation enregistrée !")

# ==========================================
#              PÁGINAS DE LA APP
# ==========================================

# --- PÁGINA 1: PERFIL + GESTIÓN DE PRUEBA ---
if st.session_state['page'] == 'profile':
    st.markdown("<h1>👤 Mon Profil</h1>", unsafe_allow_html=True)
    
    # SECCIÓN 1: CREAR PERFIL
    with st.expander("✨ Créer / Modifier mon Avatar", expanded=True):
        with st.form("profile_maker"):
            st.markdown("<div class='avatar-circle'>😎</div>", unsafe_allow_html=True)
            c1, c2 = st.columns([1,3])
            
            lista_avatares = ["🦊", "🦁", "🐯", "🐼", "🐨", "🦄", "🐲", "⚡", "🔥", "🚀", "🤖", "👽", "🦸", "🥷", "🧙", "🕵️", "👻"]
            with c1: avatar = st.selectbox("Avatar", lista_avatares)
            with c2: pseudo = st.text_input("Ton Pseudo", placeholder="Ex: Flash_Gordon")
            
            st.markdown("### ⚡ Mes Super-Pouvoirs")
            forces = st.multiselect("Forces", ["Vitesse 🏃‍♂️", "Force 💪", "Stratégie 🧠", "Endurance 🔋", "Organisation 📋"], label_visibility="collapsed")
            
            st.markdown("### 🐢 Mon Point Faible")
            faiblesse = st.text_input("Weakness", placeholder="Je suis...", label_visibility="collapsed")
            
            if st.form_submit_button("💾 Sauvegarder Profil"):
                if pseudo and forces:
                    new_user = pd.DataFrame([[pseudo, avatar, ", ".join(forces), faiblesse, "Ready", "None"]], 
                                          columns=['Pseudo', 'Avatar', 'Forces', 'Faiblesse', 'Slogan', 'TeamID'])
                    df_eleves = pd.concat([df_eleves, new_user], ignore_index=True)
                    save_data(df_eleves, FILE_ELEVES)
                    st.success("Profil mis à jour !")
                    st.rerun()

    # SECCIÓN 2: BAUTIZAR PRUEBA
    st.markdown("---")
    st.subheader("🔥 Ma Team & Mon Épreuve")
    user_pseudo = pseudo if 'pseudo' in locals() and pseudo else ""
    if not user_pseudo:
        user_pseudo = st.text_input("Entre ton pseudo pour voir ta team:", key="search_team")

    if user_pseudo:
        my_team = df_proposals[
            ((df_proposals['Demandeur'] == user_pseudo) | (df_proposals['Partenaire'] == user_pseudo)) &
            (df_proposals['Status'] == 'Approved')
        ]
        
        if not my_team.empty:
            row_team = my_team.iloc[0]
            st.success(f"✅ Tu es en duo avec : {row_team['Partenaire'] if row_team['Demandeur'] == user_pseudo else row_team['Demandeur']}")
            
            current_test_name = row_team.get('Nom_Epreuve', 'Non défini')
            st.info(f"Nom actuel de l'épreuve : **{current_test_name}**")
            
            with st.form("name_test_form"):
                new_name = st.text_input("Nommez votre épreuve sportive (Ex: Le Saut Galactique):")
                if st.form_submit_button("🏷️ Baptiser l'Épreuve"):
                    idx = row_team.name
                    df_proposals.at[idx, 'Nom_Epreuve'] = new_name
                    save_data(df_proposals, FILE_PROPOSALS)
                    st.balloons()
                    st.success(f"C'est officiel ! Votre épreuve s'appelle : {new_name}")
                    st.rerun()
        else:
            st.caption("Tu n'as pas encore d'équipe validée par le Conseil.")

# --- PÁGINA 2: MERCADO (AHORA CON AUDIO - DUA) ---
elif st.session_state['page'] == 'market':
    st.markdown("<h1>🤝 Le Marché</h1>", unsafe_allow_html=True)
    available_students = df_eleves[df_eleves['TeamID'] == 'None']

    if available_students.empty:
        st.warning("Personne de disponible.")
    else:
        for i, row in available_students.iterrows():
            with st.container():
                c1, c2 = st.columns([1, 4])
                with c1: st.markdown(f"<div style='font-size:30px;'>{row['Avatar']}</div>", unsafe_allow_html=True)
                with c2: 
                    st.markdown(f"**{row['Pseudo']}**")
                    st.caption(f"⚡ {row['Forces']} | 🐢 {row['Faiblesse']}")
                
                with st.expander(f"💌 Proposer Alliance à {row['Pseudo']}"):
                    st.markdown("#### Pourquoi ce choix ?")
                    st.caption("Option A: Écris ta justification.")
                    
                    # --- FORMULARIO HÍBRIDO ---
                    # Nota: Sacamos los inputs fuera del form estricto para que el audio no recargue mal
                    me = st.text_input(f"Ton Pseudo (pour {row['Pseudo']})", key=f"me_{i}")
                    justif_text = st.text_area("Justification Écrite", placeholder="Je te choisis car...", key=f"txt_{i}")
                    
                    st.caption("Option B: Enregistre ta voix (Micro d'Or 🎙️)")
                    # Componente de Audio DUA
                    wav_audio_data = st_audiorec(key=f"rec_{i}")

                    if st.button(f"🚀 Envoyer Proposition à {row['Pseudo']}", key=f"btn_{i}"):
                        # VALIDACIÓN DUA: Texto O Audio
                        has_text = len(justif_text) > 10
                        has_audio = wav_audio_data is not None
                        
                        if has_text or has_audio:
                            # Preparar el mensaje para guardar
                            final_justification = justif_text
                            if has_audio and not has_text:
                                final_justification = "[🎤 MESSAGE VOCAL REÇU - Validé par DUA]"
                            elif has_audio and has_text:
                                final_justification = justif_text + " (+ 🎤 Audio)"

                            new_p = pd.DataFrame([[me, row['Pseudo'], final_justification, 0, 0, "Pending", "Non défini"]],
                                               columns=['Demandeur', 'Partenaire', 'Justification', 'Votes_Pour', 'Votes_Contre', 'Status', 'Nom_Epreuve'])
                            df_proposals = pd.concat([df_proposals, new_p], ignore_index=True)
                            save_data(df_proposals, FILE_PROPOSALS)
                            st.success("Proposition envoyée au Conseil !")
                        else:
                            st.error("⚠️ Il faut écrire une justification OU enregistrer un audio !")

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

# --- PÁGINA 5: PREMIOS (AWARDS) ---
elif st.session_state['page'] == 'awards':
    st.markdown("<h1>🏆 Les Oscars JO</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🗳️ Je Vote", "📊 Résultats"])
    approved_teams = df_proposals[df_proposals['Status'] == 'Approved']
    
    if approved_teams.empty:
        st.warning("⚠️ Il faut valider des équipes au Conseil d'abord !")
    else:
        team_list = []
        for i, r in approved_teams.iterrows():
            label = f"{r['Demandeur']} & {r['Partenaire']}"
            if r['Nom_Epreuve'] != "Non défini":
                label += f" ({r['Nom_Epreuve']})"
            team_list.append(label)
        
        with tab1:
            st.markdown("Vote pour les meilleurs duos !")
            with st.form("voting_form"):
                voter = st.selectbox("Qui vote ?", df_eleves['Pseudo'].unique())
                c_a, c_b = st.columns(2)
                with c_a:
                    v_eq = st.selectbox("⚖️ Prix Équité", team_list)
                    v_in = st.selectbox("💡 Prix Innovation", team_list)
                with c_b:
                    v_fp = st.selectbox("🤝 Prix Fair-Play", team_list)
                    v_fr = st.selectbox("🗣️ Prix Francophonie", team_list)
                
                if st.form_submit_button("📩 Envoyer"):
                    if voter in df_votes['Votante'].values:
                        st.error("Tu as déjà voté !")
                    else:
                        new_vote = pd.DataFrame([[voter, v_eq, v_fp, v_in, v_fr]], 
                                              columns=['Votante', 'Equite', 'FairPlay', 'Innovation', 'Francophonie'])
                        df_votes = pd.concat([df_votes, new_vote], ignore_index=True)
                        save_data(df_votes, FILE_VOTES)
                        st.success("Votes enregistrés !")
                        st.balloons()
        with tab2:
            if df_votes.empty: st.info("Attente des votes...")
            else:
                def show(cat, emo):
                    if cat in df_votes.columns:
                        c = df_votes[cat].value_counts()
                        if not c.empty: st.metric(f"{emo} Gagnant", c.idxmax(), f"{c.max()} votes")
                show('Equite', '⚖️')
                show('FairPlay', '🤝')
                show('Innovation', '💡')
                show('Francophonie', '🗣️')

# --- MENÚ INFERIOR ---
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
    if st.button("🏆"): nav('awards')
