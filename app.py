import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Gymkhana Escolar",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🏫"
)

# Ocultar elementos de la interfaz de Streamlit
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding: 0 !important; margin: 0 !important;}
        iframe {height: 100vh !important;} 
    </style>
""", unsafe_allow_html=True)

# --- CÓDIGO FRONTEND COMPLETO ---
html_code = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Gymkhana App</title>
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Montserrat:wght@800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>

    <style>
        :root {
            --bg-color: #121212;
            --card-bg: #1E1E1E;
            --primary: #4D79FF;
            --accent: #FFD93D;
            --text-main: #FFFFFF;
            --font-body: 'Poppins', sans-serif;
            --font-head: 'Montserrat', sans-serif;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: var(--font-body);
            margin: 0; padding: 0;
            overflow-x: hidden;
            padding-bottom: 90px; /* Espacio para el menú inferior */
        }

        /* --- ESTILOS DE PANELES SÓLIDOS --- */
        .solid-panel {
            background-color: var(--card-bg);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            border: 1px solid #333;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }

        /* --- BOTONES GRANDES (HOME) --- */
        .home-btn {
            background-color: var(--card-bg);
            border: 1px solid #444;
            border-radius: 15px;
            padding: 30px 20px;
            text-align: center;
            cursor: pointer;
            transition: transform 0.1s;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .home-btn:active { transform: scale(0.95); background-color: #252525; }
        .home-btn i { font-size: 2.5rem; margin-bottom: 10px; color: var(--primary); }
        .home-btn h3 { font-size: 1.1rem; margin: 0; font-weight: 700; }

        /* --- BOTONES DE ACCIÓN --- */
        .btn-solid {
            background-color: var(--primary);
            color: white; border: none; border-radius: 8px;
            padding: 12px; width: 100%; font-weight: 700;
            text-transform: uppercase; font-family: var(--font-head);
        }
        .btn-solid:active { background-color: #3a5bbf; }

        /* --- INPUTS --- */
        .solid-input {
            background-color: #2C2C2C; border: 1px solid #444;
            color: white; padding: 12px; border-radius: 8px;
            width: 100%; text-align: center; font-size: 1.2rem;
            margin-bottom: 15px;
        }

        /* --- VISTAS --- */
        .view { display: none; padding: 20px; }
        .active-view { display: block; animation: fadeIn 0.3s; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

        /* --- MISIONES --- */
        .mission-card { cursor: pointer; position: relative; }
        .mission-card.locked { opacity: 0.5; pointer-events: none; background-color: #1a1a1a; }
        .mission-card.completed { border-left: 5px solid #28a745; background-color: #222; }
        .mission-card.completed h6 { text-decoration: line-through; color: #888; }

        /* --- MENÚ INFERIOR (DOCK) --- */
        .dock-nav {
            position: fixed; bottom: 0; left: 0; width: 100%;
            background-color: #1E1E1E; border-top: 1px solid #333;
            display: flex; justify-content: space-around;
            padding: 15px 0; z-index: 1000;
        }
        .dock-item { font-size: 1.5rem; color: #666; cursor: pointer; transition: 0.2s; }
        .dock-item.active { color: var(--primary); transform: translateY(-5px); }
        
        /* --- MODAL --- */
        .custom-modal {
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.9); z-index: 2000;
            justify-content: center; align-items: center;
        }
        .custom-modal.show { display: flex; }
        .modal-content-solid {
            background: var(--card-bg); border: 1px solid #444;
            border-radius: 12px; padding: 30px; width: 90%; max-width: 400px; text-align: center;
        }
    </style>
</head>
<body>

    <section id="view-home" class="view active-view">
        <div class="text-center mb-5 mt-4">
            <h1 style="font-family: var(--font-head); font-size: 2.5rem;">GYMKHANA</h1>
            <p class="text-secondary small">LYCÉE OLYMPIQUE</p>
            <div id="team-badge" class="badge bg-secondary mb-2" style="font-size: 0.8rem;">Équipe: Inconnue</div>
        </div>

        <div class="row g-3">
            <div class="col-6">
                <div class="home-btn" onclick="app.nav('dashboard', 'nav-dash')">
                    <i class="fa-solid fa-map-location-dot"></i>
                    <h3>MISSIONS</h3>
                </div>
            </div>
            <div class="col-6">
                <div class="home-btn" onclick="app.nav('oscars', 'nav-oscars')">
                    <i class="fa-solid fa-trophy text-warning"></i>
                    <h3>OSCARS</h3>
                </div>
            </div>
            <div class="col-6">
                <div class="home-btn" onclick="alert('Map en construction!')">
                    <i class="fa-solid fa-map text-info"></i>
                    <h3>PLAN</h3>
                </div>
            </div>
            <div class="col-6">
                <div class="home-btn" onclick="alert('Ranking disponible à la fin!')">
                    <i class="fa-solid fa-chart-simple text-danger"></i>
                    <h3>RANKING</h3>
                </div>
            </div>
        </div>
    </section>

    <section id="view-dashboard" class="view">
        <h4 class="fw-bold mb-3" style="font-family: var(--font-head);">TABLERO DE MISIONES</h4>
        
        <div class="solid-panel d-flex justify-content-center position-relative mb-4" style="height: 180px;">
            <canvas id="progressChart"></canvas>
            <div class="position-absolute top-50 start-50 translate-middle text-center">
                <h2 id="percent-text" class="m-0 fw-bold">0%</h2>
            </div>
        </div>

        <div id="missions-list">
            </div>
    </section>

    <section id="view-oscars" class="view">
        <h2 class="text-center fw-bold mb-4 mt-2" style="font-family: var(--font-head);">PREMIOS</h2>
        <div class="row g-3">
            <div class="col-6"><div class="solid-panel text-center"><i class="fa-solid fa-language fa-2x text-warning mb-2"></i><h6 class="small mb-0">Francophones</h6></div></div>
            <div class="col-6"><div class="solid-panel text-center"><i class="fa-solid fa-users fa-2x text-warning mb-2"></i><h6 class="small mb-0">Équipe</h6></div></div>
            <div class="col-6"><div class="solid-panel text-center"><i class="fa-solid fa-lightbulb fa-2x text-warning mb-2"></i><h6 class="small mb-0">Innovation</h6></div></div>
            <div class="col-6"><div class="solid-panel text-center"><i class="fa-solid fa-leaf fa-2x text-warning mb-2"></i><h6 class="small mb-0">Écologie</h6></div></div>
        </div>
    </section>

    <div class="dock-nav">
        <div id="nav-home" class="dock-item active" onclick="app.nav('home', this)"><i class="fa-solid fa-house"></i></div>
        <div id="nav-dash" class="dock-item" onclick="app.nav('dashboard', this)"><i class="fa-solid fa-gamepad"></i></div>
        <div id="nav-oscars" class="dock-item" onclick="app.nav('oscars', this)"><i class="fa-solid fa-trophy"></i></div>
    </div>

    <div id="customModal" class="custom-modal">
        <div class="modal-content-solid">
            <div class="mb-3">
                <i id="modal-icon" class="fa-solid fa-circle-question fa-3x text-primary"></i>
            </div>
            <h4 id="modal-title" class="fw-bold mb-2">...</h4>
            <p id="modal-desc" class="text-secondary small mb-4">...</p>
            
            <input type="text" id="user-input" class="solid-input text-uppercase" placeholder="...">
            
            <button onclick="app.validate()" class="btn-solid mb-2">VALIDAR</button>
            <button onclick="app.closeModal()" class="btn btn-link text-secondary text-decoration-none btn-sm">Cerrar</button>
            
            <div id="feedback-msg" class="mt-3 small fw-bold"></div>
        </div>
    </div>

    <script>
        const GAME_DATA = {
            teamName: null,
            missions: [
                { id: 1, title: "Identidad", type: "name", completed: false, icon: "fa-id-card", desc: "Elige un nombre para tu equipo." },
                { id: 2, title: "Economía", type: "code", code: "JETON", completed: false, icon: "fa-coins", desc: "Busca a 'Les Banquiers' y consigue el código." },
                { id: 3, title: "Clima", type: "code", code: "FUTUR", completed: false, icon: "fa-temperature-low", desc: "Busca a 'Les Écologistes' y consigue el código." },
                { id: 4, title: "Salud", type: "code", code: "SANTE", completed: false, icon: "fa-heart-pulse", desc: "Busca a 'Les Nutritionnistes' y consigue el código." },
                { id: 5, title: "Urbanismo", type: "code", code: "VILLE", completed: false, icon: "fa-city", desc: "Busca a 'Les Architectes' y consigue el código." }
            ],
            currentId: null
        };
        let chart = null;

        const app = {
            nav: (viewName, el) => {
                // Manejar clases de navegación
                document.querySelectorAll('.dock-item').forEach(i => i.classList.remove('active'));
                
                // Si el elemento se pasa como string (desde los botones home), buscarlo por ID
                if (typeof el === 'string') {
                    document.getElementById(el).classList.add('active');
                } else if (el) {
                    el.classList.add('active');
                } else {
                    // Fallback si venimos de home sin elemento
                    document.getElementById('nav-' + (viewName === 'dashboard' ? 'dash' : viewName)).classList.add('active');
                }

                // Cambiar vista
                document.querySelectorAll('.view').forEach(v => v.classList.remove('active-view'));
                document.getElementById('view-' + viewName).classList.add('active-view');

                // Si vamos al dashboard, asegurar que se renderiza
                if(viewName === 'dashboard') {
                    app.renderList();
                    setTimeout(app.initChart, 100);
                }
            },

            renderList: () => {
                const list = document.getElementById('missions-list');
                list.innerHTML = "";
                GAME_DATA.missions.forEach(m => {
                    const statusClass = m.completed ? 'completed' : '';
                    // Bloquear si la anterior no está hecha (excepto la 1)
                    const isLocked = (!m.completed && m.id > 1 && !GAME_DATA.missions[m.id-2].completed);
                    const lockClass = isLocked ? 'locked' : '';
                    const iconStatus = m.completed ? 'fa-check text-success' : (isLocked ? 'fa-lock text-secondary' : 'fa-play text-white');

                    list.innerHTML += `
                    <div class="solid-panel mission-card d-flex align-items-center ${statusClass} ${lockClass}" onclick="app.openModal(${m.id})">
                        <i class="fa-solid ${m.icon} me-3 fa-xl text-secondary"></i>
                        <div class="flex-grow-1">
                            <h6 class="mb-0 fw-bold">${m.title}</h6>
                        </div>
                        <i class="fa-solid ${iconStatus}"></i>
                    </div>`;
                });
                
                // Actualizar contador del Home
                const count = GAME_DATA.missions.filter(m => m.completed).length;
                if(GAME_DATA.teamName) {
                    document.getElementById('team-badge').innerText = "Équipe: " + GAME_DATA.teamName;
                    document.getElementById('team-badge').classList.replace('bg-secondary', 'bg-success');
                }
            },

            openModal: (id) => {
                GAME_DATA.currentId = id;
                const m = GAME_DATA.missions.find(x => x.id === id);
                if(m.completed) return;

                document.getElementById('modal-title').innerText = m.title;
                document.getElementById('modal-desc').innerText = m.desc;
                document.getElementById('feedback-msg').innerText = "";
                
                const inp = document.getElementById('user-input');
                inp.value = "";
                
                if(m.type === 'name') {
                    inp.placeholder = "Nombre del equipo...";
                } else {
                    inp.placeholder = "CÓDIGO SECRETO";
                }
                
                document.getElementById('customModal').classList.add('show');
            },

            closeModal: () => document.getElementById('customModal').classList.remove('show'),

            validate: () => {
                const inp = document.getElementById('user-input').value.trim();
                if(!inp) return;

                const m = GAME_DATA.missions.find(x => x.id === GAME_DATA.currentId);
                const fb = document.getElementById('feedback-msg');

                if (m.type === 'name') {
                    // Misión 1: Guardar nombre
                    GAME_DATA.teamName = inp;
                    m.completed = true;
                    fb.innerText = "¡Equipo registrado!";
                    fb.style.color = "#28a745";
                    confetti();
                    setTimeout(() => {
                        app.closeModal();
                        app.renderList();
                        app.updateChart();
                    }, 1000);
                } else {
                    // Misiones de Código
                    if(inp.toUpperCase() === m.code) {
                        m.completed = true;
                        fb.innerText = "¡Código Correcto!";
                        fb.style.color = "#28a745";
                        confetti();
                        setTimeout(() => {
                            app.closeModal();
                            app.renderList();
                            app.updateChart();
                        }, 1000);
                    } else {
                        fb.innerText = "Código Incorrecto";
                        fb.style.color = "#dc3545";
                    }
                }
            },

            initChart: () => {
                // Destruir si existe para evitar duplicados
                if(chart) chart.destroy();
                const ctx = document.getElementById('progressChart').getContext('2d');
                chart = new Chart(ctx, {
                    type: 'doughnut',
                    data: { datasets: [{ data: [0, 5], backgroundColor: ['#4D79FF', '#333'], borderWidth: 0 }] },
                    options: { responsive: true, maintainAspectRatio: false, cutout: '80%', events: [] }
                });
                app.updateChart();
            },

            updateChart: () => {
                if(!chart) return;
                const c = GAME_DATA.missions.filter(m => m.completed).length;
                const total = GAME_DATA.missions.length;
                chart.data.datasets[0].data = [c, total-c];
                chart.update();
                document.getElementById('percent-text').innerText = Math.round((c/total)*100) + "%";
            }
        };

        // Iniciar en Home
        // No llamamos a nada automático, el HTML ya muestra la home por defecto.
    </script>
</body>
</html>
"""

# Renderizar en Streamlit
components.html(html_code, height=900, scrolling=True)
