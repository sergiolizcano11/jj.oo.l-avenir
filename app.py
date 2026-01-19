import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Gymkhana Solid",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="⚡"
)

# Ocultar elementos de Streamlit
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding: 0 !important; margin: 0 !important;}
        iframe {height: 100vh !important;} 
    </style>
""", unsafe_allow_html=True)

# --- CÓDIGO FRONTEND (SIN CRISTAL / SIN ANIMACIONES) ---
html_code = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Gymkhana Solid</title>
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Montserrat:wght@800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>

    <style>
        :root {
            --bg-color: #121212;         /* Fondo Negro Sólido */
            --card-bg: #1E1E1E;          /* Fondo Tarjeta Gris Oscuro */
            --primary: #4D79FF;          /* Azul */
            --accent: #FFD93D;           /* Amarillo */
            --text-main: #FFFFFF;
            --font-body: 'Poppins', sans-serif;
            --font-head: 'Montserrat', sans-serif;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: var(--font-body);
            margin: 0;
            padding: 0;
            overflow-x: hidden;
            padding-bottom: 80px; /* Espacio para menú */
        }

        /* --- TARJETAS SÓLIDAS (NO GLASS) --- */
        .solid-panel {
            background-color: var(--card-bg);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            border: 1px solid #333; /* Borde sutil */
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }

        /* --- BOTONES SÓLIDOS --- */
        .btn-solid {
            background-color: var(--primary);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px;
            width: 100%;
            font-weight: 700;
            text-transform: uppercase;
            font-family: var(--font-head);
            cursor: pointer;
        }
        .btn-solid:active {
            background-color: #3a5bbf;
        }

        /* --- INPUTS SÓLIDOS --- */
        .solid-input {
            background-color: #2C2C2C;
            border: 1px solid #444;
            color: white;
            padding: 12px;
            border-radius: 8px;
            width: 100%;
            text-align: center;
            font-size: 1.1rem;
            margin-bottom: 15px;
        }
        .solid-input:focus {
            outline: none;
            border-color: var(--primary);
        }

        /* --- VISTAS (SIN TRANSICIÓN) --- */
        .view {
            display: none; /* Se oculta/muestra instantáneamente */
            padding: 20px;
        }
        .active-view {
            display: block;
        }

        /* --- MISIONES --- */
        .mission-card {
            cursor: pointer;
        }
        .mission-card.locked {
            opacity: 0.5;
            pointer-events: none;
            background-color: #1a1a1a;
        }
        .mission-card.completed {
            border-left: 5px solid #28a745; /* Verde éxito */
            background-color: #222;
        }

        /* --- OSCARS --- */
        .oscar-card {
            text-align: center;
            background: #252525;
            border: 1px solid #FFD93D;
        }
        .text-gold { color: #FFD93D; }

        /* --- MENÚ INFERIOR (SÓLIDO) --- */
        .dock-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #1E1E1E;
            border-top: 1px solid #333;
            display: flex;
            justify-content: space-around;
            padding: 15px 0;
            z-index: 1000;
        }
        .dock-item {
            font-size: 1.5rem;
            color: #666;
            cursor: pointer;
        }
        .dock-item.active {
            color: var(--primary);
        }

        /* --- MODAL --- */
        .custom-modal {
            display: none;
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.9);
            z-index: 2000;
            justify-content: center; align-items: center;
        }
        .custom-modal.show { display: flex; }
        .modal-content-solid {
            background: var(--card-bg);
            border: 1px solid #444;
            border-radius: 12px;
            padding: 30px;
            width: 90%;
            max-width: 400px;
            text-align: center;
        }

        /* Helpers */
        .text-accent { color: var(--accent); }
    </style>
</head>
<body>

    <section id="view-login" class="view active-view" style="height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center;">
        <div class="solid-panel text-center" style="width: 100%; max-width: 400px;">
            <i class="fa-solid fa-rocket fa-4x text-accent mb-3"></i>
            <h1 class="mb-0" style="font-family: var(--font-head);">GYMKHANA</h1>
            <p class="text-secondary small mb-4">EDICIÓN ESCOLAR</p>
            
            <input type="text" id="team-input" class="solid-input" placeholder="Nombre del Equipo...">
            <button onclick="app.login()" class="btn-solid">ENTRAR</button>
        </div>
    </section>

    <section id="view-dashboard" class="view">
        <div class="d-flex justify-content-between align-items-center mb-3">
            <div>
                <small class="text-uppercase text-secondary fw-bold">Equipo</small>
                <div id="display-team" class="h5 fw-bold mb-0">...</div>
            </div>
            <div class="solid-panel py-1 px-3 mb-0">
                <i class="fa-solid fa-star text-accent"></i> <span id="completed-count">0</span>/4
            </div>
        </div>

        <div class="solid-panel d-flex justify-content-center position-relative mb-4" style="height: 200px;">
            <canvas id="progressChart"></canvas>
            <div class="position-absolute top-50 start-50 translate-middle text-center">
                <h2 id="percent-text" class="m-0 fw-bold">0%</h2>
            </div>
        </div>

        <h6 class="text-secondary text-uppercase fw-bold small mb-3">Misiones</h6>
        <div id="missions-list"></div>
    </section>

    <section id="view-oscars" class="view">
        <h2 class="text-center fw-bold mb-4 mt-2" style="font-family: var(--font-head);">PREMIOS</h2>
        <div class="row g-3">
            <div class="col-6"><div class="solid-panel oscar-card"><i class="fa-solid fa-language fa-2x text-gold mb-2"></i><h6 class="small mb-0">Francophones</h6></div></div>
            <div class="col-6"><div class="solid-panel oscar-card"><i class="fa-solid fa-users fa-2x text-gold mb-2"></i><h6 class="small mb-0">Equipo</h6></div></div>
            <div class="col-6"><div class="solid-panel oscar-card"><i class="fa-solid fa-lightbulb fa-2x text-gold mb-2"></i><h6 class="small mb-0">Innovación</h6></div></div>
            <div class="col-6"><div class="solid-panel oscar-card"><i class="fa-solid fa-leaf fa-2x text-gold mb-2"></i><h6 class="small mb-0">Ecología</h6></div></div>
        </div>
    </section>

    <div id="bottom-nav" class="dock-nav" style="display: none;">
        <div class="dock-item active" onclick="app.nav('dashboard', this)"><i class="fa-solid fa-gamepad"></i></div>
        <div class="dock-item" onclick="app.nav('oscars', this)"><i class="fa-solid fa-trophy"></i></div>
    </div>

    <div id="customModal" class="custom-modal">
        <div class="modal-content-solid">
            <h4 id="modal-title" class="fw-bold mb-2">...</h4>
            <p id="modal-desc" class="text-secondary small mb-4">...</p>
            <input type="text" id="secret-code" class="solid-input text-uppercase" placeholder="CÓDIGO">
            <button onclick="app.validate()" class="btn-solid mb-2">VERIFICAR</button>
            <button onclick="app.closeModal()" class="btn btn-link text-secondary text-decoration-none btn-sm">Cancelar</button>
            <div id="feedback-msg" class="mt-3 small fw-bold"></div>
        </div>
    </div>

    <script>
        const GAME_DATA = {
            missions: [
                { id: 1, title: "Economía", code: "JETON", completed: false, icon: "fa-coins" },
                { id: 2, title: "Clima", code: "FUTUR", completed: false, icon: "fa-temperature-low" },
                { id: 3, title: "Salud", code: "SANTE", completed: false, icon: "fa-heart-pulse" },
                { id: 4, title: "Urbanismo", code: "VILLE", completed: false, icon: "fa-city" }
            ],
            teamName: ""
        };
        let chart = null;

        const app = {
            login: () => {
                const val = document.getElementById('team-input').value;
                if(!val) return;
                GAME_DATA.teamName = val;
                document.getElementById('display-team').innerText = val;
                
                // Cambio instantáneo de vista (sin transición)
                document.getElementById('view-login').style.display = 'none'; 
                document.getElementById('view-dashboard').style.display = 'block';
                document.getElementById('bottom-nav').style.display = 'flex';
                
                app.renderList();
                app.initChart();
            },
            nav: (viewName, el) => {
                // Cambio de iconos
                document.querySelectorAll('.dock-item').forEach(i => i.classList.remove('active'));
                el.classList.add('active');
                
                // Cambio instantáneo de vista
                document.querySelectorAll('.view').forEach(v => v.style.display = 'none');
                document.getElementById('view-' + viewName).style.display = 'block';
            },
            renderList: () => {
                const list = document.getElementById('missions-list');
                list.innerHTML = "";
                GAME_DATA.missions.forEach(m => {
                    const statusClass = m.completed ? 'completed' : '';
                    const lockClass = (!m.completed && m.id > 1 && !GAME_DATA.missions[m.id-2].completed) ? 'locked' : '';
                    
                    list.innerHTML += `
                    <div class="solid-panel mission-card d-flex align-items-center ${statusClass} ${lockClass}" onclick="app.openModal(${m.id})">
                        <i class="fa-solid ${m.icon} me-3 fa-xl text-secondary"></i>
                        <div class="flex-grow-1">
                            <h6 class="mb-0 fw-bold">${m.title}</h6>
                        </div>
                        <i class="fa-solid ${m.completed ? 'fa-check text-success' : 'fa-chevron-right text-secondary'}"></i>
                    </div>`;
                });
                document.getElementById('completed-count').innerText = GAME_DATA.missions.filter(m => m.completed).length;
            },
            openModal: (id) => {
                GAME_DATA.currentId = id;
                const m = GAME_DATA.missions.find(x => x.id === id);
                if(m.completed) return;
                document.getElementById('modal-title').innerText = m.title;
                document.getElementById('modal-desc').innerText = "Busca a los expertos para obtener el código.";
                document.getElementById('secret-code').value = "";
                document.getElementById('feedback-msg').innerText = "";
                document.getElementById('customModal').classList.add('show');
            },
            closeModal: () => document.getElementById('customModal').classList.remove('show'),
            validate: () => {
                const inp = document.getElementById('secret-code').value.toUpperCase();
                const m = GAME_DATA.missions.find(x => x.id === GAME_DATA.currentId);
                if(inp === m.code) {
                    m.completed = true;
                    confetti();
                    app.closeModal();
                    app.renderList();
                    app.updateChart();
                } else {
                    document.getElementById('feedback-msg').innerText = "Código Incorrecto";
                    document.getElementById('feedback-msg').style.color = "#dc3545";
                }
            },
            initChart: () => {
                const ctx = document.getElementById('progressChart').getContext('2d');
                chart = new Chart(ctx, {
                    type: 'doughnut',
                    data: { datasets: [{ data: [0, 4], backgroundColor: ['#4D79FF', '#333'], borderWidth: 0 }] },
                    options: { responsive: true, maintainAspectRatio: false, cutout: '80%' }
                });
            },
            updateChart: () => {
                const c = GAME_DATA.missions.filter(m => m.completed).length;
                chart.data.datasets[0].data = [c, 4-c];
                chart.update();
                document.getElementById('percent-text').innerText = Math.round((c/4)*100) + "%";
            }
        };
    </script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=True)
