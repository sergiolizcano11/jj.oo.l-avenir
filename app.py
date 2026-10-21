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
st.set_page_config(page_title="J.O. De l'Avenir", layout="wide", initial_sidebar_state="collapsed", page_icon="🏅")

if 'lang' not in st.session_state: st.session_state.lang = 'Français'
if 'chapter' not in st.session_state: st.session_state.chapter = 1

translations = {
    'Français': {
        'tools': "Boîte à Outils", 'tts': "🗣️ Lecteur (TTS)", 'mic': "🎙️ Micro",
        'card': "🎒 Carte Élève", 'name': "Ton Nom:", 'trait': "Atout:", 
        'traits': ["Vitesse", "Force", "Stratégie", "Créativité", "Éloquence"], 'download_pdf': "📄 Ma Carte",
        'admin': "🔐 Zone Prof", 'pass': "Mot de passe:", 'chap_control': "Contrôle Chapitres",
        'chap_titles': {1: "Chap. 1: L'Appel", 2: "Chap. 2: L'Équipe", 3: "Chap. 3: L'Action", 4: "Chap. 4: Les Règles", 5: "Chap. 5: L'Énergie", 6: "Chap. 6: La Gloire"},
        'create_athlete': "CRÉEZ VOTRE ATHLÈTE", 'choose_champ': "CHOISISSEZ VOTRE CHAMPION",
        'name_label': "NOM", 'enter_stadium': "ENTRER DANS LE STADE",
        'profil_btn': "MON PROFIL", 'missions_btn': "MISSIONS", 'map_btn': "PLAN", 'journal_btn': "JOURNAL", 'arcade_btn': "ARCADE", 'oscars_btn': "ÉVALUATION",
        'global_impact': "IMPACT GLOBAL", 'secret_codes_title': "CODES SECRETS", 'progression': "ROAD TO PARIS",
        'arcade_title': "ARCADE INTERDISCIPLINAIRE", 'journal_title': "JOURNAL DE BORD", 'campus_map': "PLAN DU CAMPUS", 'oscars_title': "CO-ÉVALUATION",
        'locked_chap': "Chapitre Requis", 'next': "Suivant", 'correct': "Correct!", 'incorrect': "Incorrect",
        'm1_title': "Conférence ODD", 'm1_desc': "Création monnaie solidaire.", 'm2_title': "Équipes Inclusives", 'm2_desc': "Création des équipes.", 
        'm3_title': "Obstacles Avenir", 'm3_desc': "Design d'épreuves.", 'm4_title': "Règlement", 'm4_desc': "Pacte de Fair-play.", 
        'm5_title': "Ravitaillement", 'm5_desc': "Snacks sains.", 'm6_title': "Plan Parcours", 'm6_desc': "Tracé sur le campus."
    },
    'Español': {
        'tools': "Herramientas", 'tts': "🗣️ Lector (TTS)", 'mic': "🎙️ Micrófono",
        'card': "🎒 Carnet Alumno", 'name': "Nombre:", 'trait': "Habilidad:", 
        'traits': ["Velocidad", "Fuerza", "Estrategia", "Creatividad", "Elocuencia"], 'download_pdf': "📄 Mi Carnet",
        'admin': "🔐 Zona Profesor", 'pass': "Contraseña:", 'chap_control': "Control Capítulos",
        'chap_titles': {1: "Cap. 1: La Llamada", 2: "Cap. 2: El Equipo", 3: "Cap. 3: La Acción", 4: "Cap. 4: Las Reglas", 5: "Cap. 5: La Energía", 6: "Cap. 6: La Gloria"},
        'create_athlete': "CREA TU ATLETA", 'choose_champ': "ELIGE TU CAMPEÓN",
        'name_label': "NOMBRE", 'enter_stadium': "ENTRAR AL ESTADIO",
        'profil_btn': "MI PERFIL", 'missions_btn': "MISIONES", 'map_btn': "MAPA", 'journal_btn': "DIARIO", 'arcade_btn': "ARCADE", 'oscars_btn': "EVALUACIÓN",
        'global_impact': "IMPACTO GLOBAL", 'secret_codes_title': "CÓDIGOS SECRETOS", 'progression': "ROAD TO PARIS",
        'arcade_title': "ARCADE INTERDISCIPLINAR", 'journal_title': "DIARIO DE A BORDO", 'campus_map': "MAPA DEL CAMPUS", 'oscars_title': "COEVALUACIÓN",
        'locked_chap': "Capítulo Requerido", 'next': "Siguiente", 'correct': "¡Correcto!", 'incorrect': "Incorrecto",
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
# 2. BACKEND MOCKS Y SIDEBAR (PYTHON)
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
    pdf.cell(210, 15, "ACCRÉDITATION", 0, 1, 'C')
    pdf.cell(210, 30, name.upper(), 0, 1, 'C')
    return pdf.output(dest='S').encode('latin-1')

with st.sidebar:
    st.selectbox("🌐 Langue / Idioma", ["Français", "Español"], key='lang')
    t = translations.get(st.session_state.lang, translations['Français'])
    
    with st.expander(t['tts']):
        text_to_speak = st.text_input("", "Allez!")
        if st.button("🔊"):
            try:
                tts = gTTS(text=text_to_speak, lang=get_tts_lang(st.session_state.lang))
                audio_bytes = io.BytesIO()
                tts.write_to_fp(audio_bytes)
                st.audio(audio_bytes, format='audio/mp3')
            except Exception as e: st.error("Erreur TTS")

    st.markdown(f"### {t['admin']}")
    password = st.text_input(t['pass'], type="password")
    if password == "prof123": 
        col1, col2, col3 = st.columns([1,2,1])
        if col1.button("⏪"): st.session_state.chapter = max(1, st.session_state.chapter - 1)
        col2.markdown(f"<div style='text-align:center;'>{st.session_state.chapter}</div>", unsafe_allow_html=True)
        if col3.button("⏩"): st.session_state.chapter = min(6, st.session_state.chapter + 1)

st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;} .block-container {padding:0;}</style>", unsafe_allow_html=True)

# ==========================================================
# 3. CSS Y HTML FRONTAL (APP NATIVA)
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

    /* RUTAS Y AVATARES (Mantenido) */
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
    
    .avatar-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-bottom: 20px; }
    .avatar-item { background: white; border: 2px solid #ccc; border-radius: 10px; padding: 12px; text-align: center; cursor: pointer; font-size: 1.5rem; }
    .avatar-item.selected { border-color: var(--primary); border-width: 4px; transform: scale(1.1); }
</style>
"""

# ==========================================================
# 4. JAVASCRIPT LOGIC (FEEDBACK ARCADE + NAVEGACIÓN)
# ==========================================================
JS_CODE = f"""
<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
<script>
    const sfx_coin = new Audio('https://actions.google.com/sounds/v1/cartoon/cartoon_boing.ogg');

    window.app = {{
        currentChapter: {st.session_state.chapter},
        data: {{ user: {{ sprite: "", name: "", trait: "", xp: 0, usedCodes: [] }}, missions: [] }},
        
        init: () => {{
            window.app.data.missions = [
                {{ id: 1, title: "{t['m1_title']}", desc: "{t['m1_desc']}", icon: "fa-coins", completed: false }},
                {{ id: 2, title: "{t['m2_title']}", desc: "{t['m2_desc']}", icon: "fa-users", completed: false }},
                {{ id: 3, title: "{t['m3_title']}", desc: "{t['m3_desc']}", icon: "fa-recycle", completed: false }},
                {{ id: 4, title: "{t['m4_title']}", desc: "{t['m4_desc']}", icon: "fa-scale-balanced", completed: false }},
                {{ id: 5, title: "{t['m5_title']}", desc: "{t['m5_desc']}", icon: "fa-apple-whole", completed: false }},
                {{ id: 6, title: "{t['m6_title']}", desc: "{t['m6_desc']}", icon: "fa-map", completed: false }}
            ];

            try {{
                const localData = localStorage.getItem("jo_avenir_2026");
                if (localData) window.app.data = JSON.parse(localData);
            }} catch (error) {{ localStorage.removeItem("jo_avenir_2026"); }}

            window.app.renderAvatars();
            window.app.updateUI();
            
            if (window.app.data.user.name !== "") {{
                document.getElementById('player-name').value = window.app.data.user.name;
                window.app.nav('home');
            }} else {{
                window.app.nav('login');
            }}
        }},

        saveData: () => {{
            try {{ localStorage.setItem("jo_avenir_2026", JSON.stringify(window.app.data)); }} catch(e) {{}}
            window.app.updateUI();
        }},

        addXP: (amount) => {{
            sfx_coin.play().catch(e=>{});
            window.app.data.user.xp += amount;
            window.app.saveData();
        }},

        nav: (view) => {{
            // Gestión de Vistas
            document.querySelectorAll('.view').forEach(v => v.classList.remove('active-view'));
            document.getElementById('view-' + view).classList.add('active-view');
            
            // Gestión de la Barra Superior (Top Bar)
            const header = document.getElementById('app-header');
            const title = document.getElementById('header-title');
            
            if(view === 'login' || view === 'home') {{
                header.classList.remove('visible'); // Ocultar top bar en menús principales
            }} else {{
                header.classList.add('visible'); // Mostrar al entrar a una sección
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
            const SPRITES = ["fa-dragon", "fa-robot", "fa-bolt", "fa-leaf", "fa-meteor"];
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
        }},

        updateUI: () => {{
            const xp = window.app.data.user.xp || 0;
            document.querySelectorAll('.xp-counter').forEach(el => el.innerText = xp);
            if(window.app.data.user.sprite) {{
                document.querySelectorAll('.mini-avatar').forEach(el => el.innerHTML = `<i class="fa-solid ${{window.app.data.user.sprite}}"></i>`);
            }}
        }},

        saveProfile: () => {{
            const name = document.getElementById('player-name').value;
            if(!window.app.data.user.sprite || !name) return alert("{t['alert_profile']}");
            window.app.data.user.name = name;
            window.app.saveData();
            window.app.nav('home');
        }},

        renderPath: () => {{
            const container = document.getElementById('path-container'); container.innerHTML = "";
            window.app.data.missions.forEach((m, idx) => {{
                const isLeft = idx % 2 === 0; const reqChapter = idx + 1;
                let statusClass = m.completed ? 'completed' : ''; let iconClass = m.completed ? 'fa-check' : m.icon;
                
                if (window.app.currentChapter < reqChapter) {{ statusClass = 'locked'; iconClass = 'fa-lock'; }} 
                else if (!m.completed && (idx === 0 || window.app.data.missions[idx-1].completed)) {{ statusClass = 'active'; }}
                
                container.innerHTML += `
                <div class="mission-node ${{isLeft ? 'left' : 'right'}} ${{statusClass}}">
                    <div class="node-icon"><i class="fa-solid ${{iconClass}}"></i></div>
                    <div><h5 class="mb-0 fw-bold">${{m.title}}</h5><small class="text-secondary">${{statusClass==='locked' ? "{t['locked_chap']} "+reqChapter : m.desc}}</small></div>
                </div>`;
            }});
        }},

        // --- SISTEMA ARCADE CON FEEDBACK ---
        startGame: (t) => {{
            // 3 Preguntas por categoría con FEEDBACK (Corrección/Explicación)
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
                bio: [
                    {{ q: "Où jeter une bouteille en plastique ?", a: ["Poubelle Jaune", "Poubelle Verte", "Poubelle Bleue"], c: 0, f: "Le plastique et le carton vont dans le bac de recyclage jaune." }},
                    {{ q: "Quel gaz cause l'effet de serre ?", a: ["Le CO2", "L'Oxygène", "L'Azote"], c: 0, f: "Le dioxyde de carbone (CO2) retient la chaleur dans l'atmosphère." }}
                ]
            }};
            
            // Si la categoría no tiene preguntas extendidas, proveemos un fallback
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
            
            document.getElementById('game-feedback').className = "feedback-box";
            document.getElementById('btn-next-question').style.display = "none";
        }},

        checkAnswer: (selectedIdx, btnElement) => {{
            // Deshabilitar clics en otras opciones
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
                confetti({{ particleCount: 40, spread: 50, origin: {{ y: 0.6 }} }});
            }} else {{
                btnElement.style.border = "3px solid #dc3545";
                // Resaltar la correcta
                document.querySelectorAll('.game-opt')[q.c].style.border = "3px solid #28a745";
                feedbackBox.className = "feedback-box incorrect";
                feedbackText.innerHTML = `<strong>{t['incorrect']}</strong><br><small>${{q.f}}</small>`;
            }}

            btnNext.style.display = "block"; // Mostrar botón continuar
        }},

        nextQuestion: () => {{
            window.app.qIndex++; 
            window.app.renderQuestion();
        }}
    }};

    setTimeout(() => window.app.init(), 200);
</script>
"""

# ==========================================================
# 5. HTML FINAL (VISTAS)
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
    <!-- HEADER NATIVO (Aparece y desaparece) -->
    <div id="app-header" class="app-header">
        <button class="back-btn" onclick="window.app.nav('home')"><i class="fa-solid fa-chevron-left"></i></button>
        <div id="header-title" class="header-title">TITRE</div>
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
        <div class="glass-panel">
            <h6 class="fw-bold"><i class="fa-solid fa-earth-americas text-primary"></i> {t['global_impact']}</h6>
            <div class="progress" style="height: 15px; border-radius: 10px; background:#fff;">
                <div id="global-xp" class="progress-bar bg-success progress-bar-striped progress-bar-animated" style="width: 15%"></div>
            </div>
            <small class="text-secondary">{t['obj_comm']}</small>
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

    <!-- SECCIÓN RUTA DE MISIONES (DUOLINGO PATH) -->
    <section id="view-missions" class="view">
        <div id="path-container" class="path-container"></div>
    </section>

    <!-- SECCIÓN ARCADE (CON FEEDBACK) -->
    <section id="view-games" class="view">
        <div id="game-menu" class="row g-2">
            <div class="col-6"><div class="glass-panel p-3 mb-2 text-center" onclick="window.app.startGame('num')"><i class="fa-solid fa-calculator fa-2x text-primary mb-2"></i><br><h6 class="mb-0 fw-bold small">NOMBRES</h6></div></div>
            <div class="col-6"><div class="glass-panel p-3 mb-2 text-center" onclick="window.app.startGame('fut')"><i class="fa-solid fa-rocket fa-2x text-warning mb-2"></i><br><h6 class="mb-0 fw-bold small">FUTUR</h6></div></div>
            <div class="col-6"><div class="glass-panel p-3 mb-2 text-center" onclick="window.app.startGame('bio')"><i class="fa-solid fa-leaf fa-2x text-success mb-2"></i><br><h6 class="mb-0 fw-bold small">SVT</h6></div></div>
        </div>
        
        <div id="game-interface" style="display:none;">
            <div class="glass-panel">
                <h5 id="game-question" class="fw-bold mb-3 text-center">...</h5>
                <div id="game-options"></div>
                
                <!-- CAJA DE FEEDBACK (CORRECCIÓN) -->
                <div id="game-feedback" class="feedback-box">
                    <span id="feedback-text"></span>
                </div>
                
                <button id="btn-next-question" class="btn-glass mt-3" style="display:none;" onclick="window.app.nextQuestion()">{t['next']}</button>
            </div>
        </div>
    </section>

    <!-- VISTAS VACÍAS PARA QUE NO FALLE LA NAVEGACIÓN -->
    <section id="view-map" class="view"><div class="glass-panel text-center"><h4>En cours de développement...</h4></div></section>
    <section id="view-journal" class="view"><div class="glass-panel text-center"><h4>En cours de développement...</h4></div></section>
    <section id="view-oscars" class="view"><div class="glass-panel text-center"><h4>En cours de développement...</h4></div></section>

    {JS_CODE}
</body>
</html>
"""

components.html(HTML_CODE, height=900, scrolling=True)
