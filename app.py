import streamlit as st
import pandas as pd
import os
import random

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="L'Alliance Olympique",
    page_icon="🏅",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- ESTILOS CSS (DISEÑO GEN Z / MÓVIL) ---
# Esto transforma Streamlit en una App visual
st.markdown("""
<style>
    /* VARIABLES DE COLOR */
    :root {
        --blue: #4D79FF;
        --yellow: #FFD93D;
        --green: #6BCB77;
        --red: #FF6B6B;
        --bg: #F4F7F6;
    }
    
    /* FONDO Y TEXTO */
    .stApp {
        background-color: var(--bg);
        font-family: 'Helvetica', sans-serif;
    }

    /* ESCONDER MENU HAMBURGUESA Y FOOTER DEFAULT */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* TARJETAS (CARD STYLE) */
    .css-1r6slb0, .stDataFrame, .stForm {
        background: white;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #eee;
    }

    /* BOTONES PRIMARIOS (AZUL ELÉCTRICO) */
    .stButton > button {
        background-color: var(--blue);
        color: white;
        border-radius: 15px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        width: 100%;
        transition: transform 0.2s;
    }
    .stButton > button:active {
        transform: scale(0.95);
    }

    /* BOTONES DE NAVEGACIÓN (FAKE BOTTOM BAR) */
    /* Nota: En Streamlit puro es difícil fijar abajo, usamos columnas al final */
    
    /* TITULOS CON GRADIENTE */
    h1 {
        background: -webkit-linear-gradient(45deg, var(--blue), var(--green));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
    }

    /* AVATAR CIRCLE */
    .avatar-box {
        font-size: 50px;
        background: #EFF3FF;
        border-radius: 50%;
        width: 100px;
        height: 100px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto;
        border: 3px solid var(--blue);
    }
</style>
""", unsafe_allow_html=True)

# --- GESTIÓN DE DATOS (PERSISTENCIA CSV) ---
FILE_ELEVES = 'eleves.csv'
FILE_PROPOSALS = 'propositions.csv'

def init_db():
    if not os.path.exists(FILE_ELEVES):
        pd.DataFrame(columns=['Pseudo', 'Avatar', 'Forces', 'Faiblesse', 'Slogan']).to_csv(FILE_ELEVES, index=False)
    if not os.path.exists(FILE_PROPOSALS):
        pd.DataFrame(columns=['Demandeur', 'Partenaire', 'Justification', 'Votes_Pour', 'Votes_Contre']).to_csv(FILE_PROPOSALS, index=False)

def load_data(file):
    return pd.read_csv(file)

def save_data(df, file):
    df.to_csv(file, index=False)

init_db()
df_eleves = load_data(FILE_ELEVES)
df_proposals = load_data(FILE_PROPOSALS)

# --- NAVEGACIÓN (SESSION STATE) ---
if 'page' not in st.session_state:
    st.session_state['page'] = 'profile'

def navigate_to(page):
    st.session_state['page'] = page
    st.rerun()

# --- PÁGINAS ---

# 1. PÁGINA PERFIL
if st.session_state['page'] == 'profile':
    st.title("Mon Profil 👤")
    st.markdown("<div style='text-align: center; color: #888; margin-bottom: 20px;'>Crée ton avatar de légende</div>", unsafe_allow_html=True)
    
    with st.form("profile_form"):
        # Selección de Avatar divertido
        avatars = ["🦊", "🦁", "🚀", "🦄", "⚡", "👽", "🤖", "🐯"]
        col_av1, col_av2 = st.columns([1, 3])
        with col_av1:
            avatar = st.selectbox("Avatar", avatars, index=0)
            st.markdown(f"<div class='avatar-box'>{avatar}</div>", unsafe_allow_html=True)
        with col_av2:
            pseudo = st.text_input("Ton Bledger (Pseudo)", placeholder="Ex: Flash_Gordon")
            slogan = st.text_input("Ma Devise", placeholder="Toujours plus loin !")

        st.markdown("### Mes Super-Pouvoirs ⚡")
        # Multiselect actúa como 'Chips'
        forces = st.multiselect(
            "Choisis tes atouts (Max 2)",
            ["Vitesse 🏃‍♂️", "Force 💪", "Stratégie 🧠", "Endurance 🔋", "Mental 🧘", "Organisation 📋"],
            max_selections=2
        )

        st.markdown("### Mon Talon d'Achille 🐢")
        faiblesse = st.text_input("Sois honnête...", placeholder="Ex: Je déteste perdre...")

        submitted = st.form_submit_button("Sauvegarder mon Perso")
        
        if submitted:
            if pseudo and forces:
                # Guardar en CSV
                new_user = pd.DataFrame([[pseudo, avatar, ", ".join(forces), faiblesse, slogan]], 
                                      columns=['Pseudo', 'Avatar', 'Forces', 'Faiblesse', 'Slogan'])
                df_eleves = pd.concat([df_eleves, new_user], ignore_index=True)
                save_data(df_eleves, FILE_ELEVES)
                st.success(f"Bienvenue dans l'arène, {pseudo} ! 🔥")
                st.balloons()
            else:
                st.error("Il manque des infos !")

# 2. PÁGINA MERCADO (MATCHING)
elif st.session_state['page'] == 'market':
    st.title("Le Hub 🤝")
    st.markdown("<p style='text-align:center'>Trouve ton duo parfait.</p>", unsafe_allow_html=True)

    if df_eleves.empty:
        st.info("Personne n'est encore inscrit... Sois le premier !")
    else:
        # Mostrar tarjetas de alumnos
        for index, row in df_eleves.iterrows():
            with st.container():
                c1, c2 = st.columns([1, 3])
                with c1:
                    st.markdown(f"<div style='font-size:40px; text-align:center;'>{row['Avatar']}</div>", unsafe_allow_html=True)
                with c2:
                    st.subheader(row['Pseudo'])
                    st.caption(f"📢 {row['Slogan']}")
                    # Mostrar etiquetas coloreadas
                    st.markdown(f"**⚡ Atouts:** {row['Forces']}")
                    st.markdown(f"**🐢 Faiblesse:** {row['Faiblesse']}")
                
                # Botón para proponer alianza (simulado con expander para ahorrar espacio)
                with st.expander(f"🔥 Faire équipe avec {row['Pseudo']}"):
                    with st.form(f"prop_form_{index}"):
                        me = st.text_input("Ton Pseudo", placeholder="Qui es-tu ?")
                        justif = st.text_area("Pourquoi ça va marcher ?", placeholder="Vends ton équipe ! On se complète car...")
                        send = st.form_submit_button("Envoyer la proposition 🚀")
                        
                        if send:
                            if len(justif) > 10:
                                new_prop = pd.DataFrame([[me, row['Pseudo'], justif, 0, 0]], 
                                                      columns=['Demandeur', 'Partenaire', 'Justification', 'Votes_Pour', 'Votes_Contre'])
                                df_proposals = pd.concat([df_proposals, new_prop], ignore_index=True)
                                save_data(df_proposals, FILE_PROPOSALS)
                                st.success("Proposition envoyée au Conseil ! ⚖️")
                            else:
                                st.warning("Ton argumentation est trop courte ! ✍️")

# 3. PÁGINA CONSEJO (VOTACIÓN)
elif st.session_state['page'] == 'council':
    st.title("Le Conseil ⚖️")
    st.markdown("<p style='text-align:center'>Vote pour valider les duos.</p>", unsafe_allow_html=True)

    if df_proposals.empty:
        st.info("Aucune alliance en attente. Le calme avant la tempête...")
    else:
        for index, row in df_proposals.iterrows():
            st.markdown("---")
            c1, c2, c3 = st.columns([1, 4, 1])
            with c2:
                st.markdown(f"### ⚔️ {row['Demandeur']} + {row['Partenaire']}")
                st.info(f"🗣️ \"{row['Justification']}\"")
            
            # Botones de Voto
            col_yes, col_no = st.columns(2)
            with col_yes:
                if st.button(f"👍 Validé ({row['Votes_Pour']})", key=f"yes_{index}"):
                    df_proposals.at[index, 'Votes_Pour'] += 1
                    save_data(df_proposals, FILE_PROPOSALS)
                    st.rerun()
            with col_no:
                if st.button(f"👎 Cringe ({row['Votes_Contre']})", key=f"no_{index}"):
                    df_proposals.at[index, 'Votes_Contre'] += 1
                    save_data(df_proposals, FILE_PROPOSALS)
                    st.rerun()

# 4. PÁGINA RANKING
elif st.session_state['page'] == 'ranking':
    st.title("Classement 🏆")
    st.markdown("### En Direct de la Gymkhana")
    
    # Datos simulados para el efecto visual
    ranking_data = pd.DataFrame({
        'Équipe': ['Les Tigres', 'Flash Duo', 'Rocket Team'],
        'Points': [120, 115, 98],
        'Badge': ['🥇', '🥈', '🥉']
    })
    
    st.dataframe(ranking_data, hide_index=True, use_container_width=True)
    st.image("https://media.giphy.com/media/l41lZAxS9lOBrxPfq/giphy.gif", caption="Ambiance !")


# --- MENÚ DE NAVEGACIÓN INFERIOR (FAKE BOTTOM BAR) ---
st.markdown("---")
col_nav1, col_nav2, col_nav3, col_nav4 = st.columns(4)

with col_nav1:
    if st.button("👤\nProfil"):
        navigate_to('profile')
with col_nav2:
    if st.button("🤝\nMarché"):
        navigate_to('market')
with col_nav3:
    if st.button("⚖️\nConseil"):
        navigate_to('council')
with col_nav4:
    if st.button("🏆\nTop"):
        navigate_to('ranking')

# Hack CSS para pegar estos botones abajo en móviles (Opcional, a veces inestable)
# Por ahora los dejamos al final del scroll para asegurar funcionalidad.