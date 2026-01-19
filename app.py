import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="J.O. De l'Avenir",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🏅"
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
    <title>J.O. De l'Avenir</title>
    
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
            --accent: #FFD93D; /* Amarillo ODD */
            --success: #28a745;
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
            padding: 25px 15px;
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
        .home-btn i { font-size: 2rem; margin-bottom: 10px; color: var(--primary); }
        .home-btn h3 { font-size: 0.9rem; margin: 0; font-weight: 700; text-transform: uppercase; }

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

        /* --- FASES DEL PROYECTO (MISIONES) --- */
        .phase-card { cursor: pointer; position: relative; border-left: 5px solid #555; }
        
        /* Fases bloqueadas (Futuro) */
        .phase-card.locked { opacity: 0.5; pointer-events: none; background-color: #1a1a1a; }
        
        /* Fases completadas */
        .phase-card.completed { border-left: 5px solid var(--success); background-color: #222; }
        .phase-card.completed h6 { color: #888; }
        
        .odd-badge {
            font-size: 0.65rem; background: #333; padding: 2px 6px; 
            border-radius: 4px; color: var(--accent); font-weight: bold;
            margin-bottom: 4px; display: inline-block;
        }

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
            background: rgba(0,0,0,0.95); z-index: 2000;
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
            <h1 style="font-family: var(--font-head); font-size: 2.2rem; line-height: 1.1;">J.O. DE L'AVENIR</h1>
            <p class="text-secondary small mt-2">INNOVATION & DURABILITÉ</p>
            <div id="team-badge" class="badge bg-secondary mb-2 px-3 py-2" style="font-size: 0.9rem;">Équipe non enregistrée</div>
        </div>

        <div class="row g-3">
            <div class="col-6">
                <div class="home-btn" onclick="app.nav('dashboard', 'nav-dash')">
                    <i class="fa-solid fa-list-check"></i>
                    <h3>PHASES DU PROJET</h3>
                </div>
            </div>
            <div class="col-6">
                <div class="home-btn" onclick="app.nav('oscars', 'nav-oscars')">
                    <i class="fa-solid fa-award text-warning"></i>
                    <h3>ÉVALUATION</h3>
                </div>
            </div>
            <div class="col-12">
                <div class="home-btn flex-row gap-3" style="opacity: 0.6;" onclick="alert('Disponible en Juin pour la Grande Gymkhana!')">
                    <i class="fa-solid fa-flag-checkered text-danger mb-0"></i>
                    <h3 class="mb-0">LA GRANDE GYMKHANA (JUIN)</h3>
                </div>
            </div>
        </div>
    </section>

    <section id="view-dashboard" class="view">
        <h4 class="fw-bold mb-3" style="font-family: var(--font-head);">PROGRESSION DU PROJET</h4>
        
        <div class="solid-panel d-flex justify-content-center position-relative mb-4" style="height: 160px;">
            <canvas id="progressChart"></canvas>
            <div class="position-absolute top-50 start-50 translate-middle text-center">
                <h2 id="percent-text" class="m-0 fw-bold">0%</h2>
            </div>
        </div>

        <div id="missions-list">
            </div>
    </section>

    <section id="view-oscars" class="view">
        <h2 class="text-center fw-bold mb-4 mt-2" style="font-family: var(--font-head);">CRITÈRES D'ÉVALUATION</h2>
        <p class="text-center text-secondary small mb-4">Basé sur les compétences et ODD</p>
        
        <div class="row g-3">
            <div class="col-6">
                <div class="solid-panel text-center h-100">
                    <i class="fa-solid fa-comments fa-2x text-warning mb-2"></i>
                    <h6 class="fw-bold small mb-1">LINGUISTIQUE</h6>
                    <small class="text-secondary" style="font-size: 0.6rem;">Futur, Impératif, Comparatifs</small>
                </div>
            </div>
            <div class="col-6">
                <div class="solid-panel text-center h-100">
                    <i class="fa-solid fa-people-group fa-2x text-warning mb-2"></i>
                    <h6 class="fw-bold small mb-1">SOCIAL</h6>
                    <small class="text-secondary" style="font-size: 0.6rem;">Travail d'équipe & Fair-play</small>
                </div>
            </div>
            <div class="col-6">
                <div class="solid-panel text-center h-100">
                    <i class="fa-solid fa-leaf fa-2x text-warning mb-2"></i>
                    <h6 class="fw-bold small mb-1">ENGAGEMENT ODD</h6>
                    <small class="text-secondary" style="font-size: 0.6rem;">Solutions durables réelles</small>
                </div>
            </div>
            <div class="col-6">
                <div class="solid-panel text-center h-100">
                    <i class="fa-solid fa-lightbulb fa-2x text-warning mb-2"></i>
                    <h6 class="fw-bold small mb-1">INNOVATION</h6>
                    <small class="text-secondary" style="font-size: 0.6rem;">Créativité du matériel</small>
                </div>
            </div>
        </div>
    </section>

    <div class="dock-nav">
        <div id="nav-home" class="dock-item active" onclick="app.nav('home', this)"><i class="fa-solid fa-house"></i></div>
        <div id="nav-dash" class="dock-item" onclick="app.nav('dashboard', this)"><i class="fa-solid fa-list-check"></i></div>
        <div id="nav-oscars" class="dock-item" onclick="app.nav('oscars', this)"><i class="fa-solid fa-award"></i></div>
    </div>

    <div id="customModal" class="custom-modal">
        <div class="modal-content-solid">
            <div class="mb-3">
                <i id="modal-icon" class="fa-solid fa-folder-open fa-3x text-primary"></i>
            </div>
            <div class="badge bg-warning text-dark mb-2" id="modal-odd">ODD</div>
            <h4 id="modal-title" class="fw-bold mb-2">...</h4>
            
            <div class="solid-panel p-2 mb-3 bg-black">
                <p id="modal-desc" class="text-white small mb-0">...</p>
            </div>
            
            <label class="small text-secondary mb-2">VALIDATION DU PROFESSEUR</label>
            <input type="text" id="user-input" class="solid-input text-uppercase" placeholder="...">
            
            <button onclick="app.validate()" class="btn-solid mb-2">VALIDER L'ÉTAPE</button>
            <button onclick="app.closeModal()" class="btn btn-link text-secondary text-decoration-none btn-sm">Fermer</button>
            
            <div id="feedback-msg" class="mt-3 small fw-bold"></div>
        </div>
    </div>

    <script>
        // --- DATOS DEL PROYECTO "J.O. DE L'AVENIR" ---
        const GAME_DATA = {
            teamName: null,
            // Las fases corresponden al cronograma del proyecto
            missions: [
                { 
                    id: 1, type: "name", title: "Constitution Équipes", odd: "ODD 5 & 10",
                    icon: "fa-users", desc: "Création des 'Équipes Inclusives' et critères de mixité.", 
                    completed: false 
                },
                { 
                    id: 2, type: "code", code: "MONNAIE", title: "L'Argent Solidaire", odd: "ODD 1 & 12",
                    icon: "fa-coins", desc: "Sept-Oct: Conception de la monnaie officielle (billets/jetons).", 
                    completed: false 
                },
                { 
                    id: 3, type: "code", code: "ECO", title: "Obstacles de l'Avenir", odd: "ODD 13",
                    icon: "fa-recycle", desc: "Jan-Fév: Design des épreuves avec matériaux recyclés.", 
                    completed: false 
                },
                { 
                    id: 4, type: "code", code: "RULES", title: "Règlement du Jeu", odd: "ODD 16",
                    icon: "fa-scale-balanced", desc: "Fév-Mars: Rédaction des normes de fair-play.", 
                    completed: false 
                },
                { 
                    id: 5, type: "code", code: "FOOD", title: "Ravitaillement", odd: "ODD 3",
                    icon: "fa-apple-whole", desc: "Avril-Mai: Planification des snacks sains.", 
                    completed: false 
                },
                { 
                    id: 6, type: "code", code: "MAP", title: "Plan du Parcours", odd: "ODD 11",
                    icon: "fa-map-location-dot", desc: "Mai-Juin: Tracé du plan dans la cour.", 
                    completed: false 
                }
            ],
            currentId: null
        };
        let chart = null;

        const app = {
            nav: (viewName, el) => {
                document.querySelectorAll('.dock-item').forEach(i => i.classList.remove('active'));
                
                if (typeof el === 'string') {
                    document.getElementById(el).classList.add('active');
                } else if (el) {
                    el.classList.add('active');
                } else {
                    document.getElementById('nav-' + (viewName === 'dashboard' ? 'dash' : viewName)).classList.add('active');
                }

                document.querySelectorAll('.view').forEach(v => v.classList.remove('active-view'));
                document.getElementById('view-' + viewName).classList.add('active-view');

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
                    // Bloquear fases futuras secuencialmente
                    const isLocked = (!m.completed && m.id > 1 && !GAME_DATA.missions[m.id-2].completed);
                    const lockClass = isLocked ? 'locked' : '';
                    const iconStatus = m.completed ? 'fa-check text-success' : (isLocked ? 'fa-lock text-secondary' : 'fa-play text-white');

                    list.innerHTML += `
                    <div class="solid-panel phase-card d-flex align-items-center ${statusClass} ${lockClass}" onclick="app.openModal(${m.id})">
                        <div class="me-3 text-center" style="width: 40px;">
                            <i class="fa-solid ${m.icon} fa-xl text-secondary"></i>
                        </div>
                        <div class="flex-grow-1">
                            <span class="odd-badge">${m.odd}</span>
                            <h6 class="mb-0 fw-bold">${m.title}</h6>
                        </div>
                        <i class="fa-solid ${iconStatus}"></i>
                    </div>`;
                });
                
                if(GAME_DATA.teamName) {
                    document.getElementById('team-badge').innerText = GAME_DATA.teamName;
                    document.getElementById('team-badge').classList.replace('bg-secondary', 'bg-success');
                }
            },

            openModal: (id) => {
                GAME_DATA.currentId = id;
                const m = GAME_DATA.missions.find(x => x.id === id);
                if(m.completed) return;

                document.getElementById('modal-title').innerText = m.title;
                document.getElementById('modal-desc').innerText = m.desc;
                document.getElementById('modal-odd').innerText = m.odd;
                document.getElementById('feedback-msg').innerText = "";
                
                const inp = document.getElementById('user-input');
                inp.value = "";
                
                if(m.type === 'name') {
                    inp.placeholder = "Nom de l'équipe...";
                } else {
                    inp.placeholder = "CODE PROFESSEUR";
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
                    GAME_DATA.teamName = inp;
                    m.completed = true;
                    fb.innerText = "Équipe Enregistrée !";
                    fb.style.color = "#28a745";
                    confetti();
                    setTimeout(() => {
                        app.closeModal();
                        app.renderList();
                        app.updateChart();
                    }, 1000);
                } else {
                    if(inp.toUpperCase() === m.code) {
                        m.completed = true;
                        fb.innerText = "Phase Validée !";
                        fb.style.color = "#28a745";
                        confetti();
                        setTimeout(() => {
                            app.closeModal();
                            app.renderList();
                            app.updateChart();
                        }, 1000);
                    } else {
                        fb.innerText = "Code Incorrect";
                        fb.style.color = "#dc3545";
                    }
                }
            },

            initChart: () => {
                if(chart) chart.destroy();
                const ctx = document.getElementById('progressChart').getContext('2d');
                chart = new Chart(ctx, {
                    type: 'doughnut',
                    data: { datasets: [{ data: [0, 6], backgroundColor: ['#4D79FF', '#333'], borderWidth: 0 }] },
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
    </script>
</body>
</html>
"""

# Renderizar en Streamlit
components.html(html_code, height=900, scrolling=True)
