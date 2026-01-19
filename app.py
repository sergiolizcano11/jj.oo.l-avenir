import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURACIÓN DE PÁGINA STREAMLIT ---
st.set_page_config(
    page_title="Gymkhana Gen Z",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🚀"
)

# Ocultamos la interfaz nativa de Streamlit para inmersión total
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding: 0 !important; margin: 0 !important;}
        iframe {height: 100vh !important;} 
    </style>
""", unsafe_allow_html=True)

# --- CÓDIGO FRONTEND (HTML/CSS/JS) ---
# Todo el diseño Glassmorphism y la lógica de animaciones vive aquí
html_code = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Gymkhana Gen Z</title>
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&family=Montserrat:wght@700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>

    <style>
        /* --- VARIABLES GEN Z --- */
        :root {
            --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --glass-bg: rgba(255, 255, 255, 0.1);
            --glass-border: 1px solid rgba(255, 255, 255, 0.2);
            --glass-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            --neon-blue: #00f2fe;
            --neon-pink: #fe00a1;
            --text-color: #fff;
            --font-main: 'Poppins', sans-serif;
            --font-header: 'Montserrat', sans-serif;
        }

        /* --- BASE --- */
        body {
            font-family: var(--font-main);
            color: var(--text-color);
            margin: 0;
            padding: 0;
            height: 100vh;
            width: 100vw;
            overflow: hidden;
            background: #0f0c29; 
        }

        /* Fondo Animado */
        .bg-animation {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
            z-index: -1;
        }

        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* --- GLASSMORPHISM --- */
        .glass-panel {
            background: var(--glass-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: 20px;
            border: var(--glass-border);
            box-shadow: var(--glass-shadow);
            margin-bottom: 15px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .glass-panel:hover {
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.2);
        }

        .glass-input {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 50px;
            padding: 15px;
            color: white;
            text-align: center;
            width: 100%;
            font-family: var(--font-header);
            transition: 0.3s;
        }
        .glass-input:focus {
            outline: none;
            border-color: var(--neon-blue);
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.3);
        }

        /* --- BOTONES --- */
        .btn-neon {
            background: linear-gradient(90deg, var(--neon-blue), #4facfe);
            color: #000;
            border: none;
            padding: 12px;
            border-radius: 50px;
            font-weight: 800;
            text-transform: uppercase;
            width: 100%;
            font-family: var(--font-header);
            box-shadow: 0 0 10px rgba(0, 242, 254, 0.5);
            transition: transform 0.2s;
        }
        .btn-neon:active { transform: scale(0.95); }

        /* --- TRANSICIONES (SPA Logic) --- */
        .view {
            display: none;
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.5s cubic-bezier(0.22, 1, 0.36, 1), transform 0.5s cubic-bezier(0.22, 1, 0.36, 1);
            height: 100%;
            overflow-y: auto;
            padding-bottom: 100px; /* Espacio para el Dock */
        }

        .active-view {
            display: block;
            opacity: 1;
            transform: translateY(0);
        }

        /* --- MISIONES --- */
        .mission-card {
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        .mission-card.locked {
            opacity: 0.6;
            filter: grayscale(1);
            pointer-events: none;
        }
        .mission-card.completed {
            border: 2px solid var(--neon-blue);
            background: rgba(0, 242, 254, 0.1);
        }

        /* --- OSCARS --- */
        .oscar-card {
            text-align: center;
            padding: 20px;
            border: 1px solid rgba(255, 215, 0, 0.3); /* Gold border */
            background: rgba(20, 20, 20, 0.6);
        }
        .text-gold {
            background: linear-gradient(to bottom, #cfc09f 22%,#634f2c 24%, #cfc09f 26%, #cfc09f 27%,#ffecb3 40%,#3a2c0f 78%); 
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            color: #fff;
            font-weight: 800;
        }

        /* --- DOCK MENU (iOS Style) --- */
        .dock-nav {
            position: fixed;
            bottom: 25px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(20, 20, 30, 0.6);
            backdrop-filter: blur(20px);
            padding: 12px 30px;
            border-radius: 50px;
            display: flex;
            gap: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            border: 1px solid rgba(255,255,255,0.1);
            z-index: 1000;
        }

        .dock-item {
            color: rgba(255,255,255,0.5);
            font-size: 1.5rem;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            cursor: pointer;
            position: relative;
        }

        .dock-item:hover, .dock-item.active {
            color: var(--neon-blue);
            transform: translateY(-10px) scale(1.2);
            text-shadow: 0 0 15px var(--neon-blue);
        }
        
        .dock-item.active::after {
            content: '';
            position: absolute;
            bottom: -15px;
            left: 50%;
            transform: translateX(-50%);
            width: 5px;
            height: 5px;
            background: var(--neon-blue);
            border-radius: 50%;
        }

        /* --- MODAL --- */
        .custom-modal {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.8);
            backdrop-filter: blur(5px);
            z-index: 2000;
            display: flex;
            justify-content: center;
            align-items: center;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s;
        }
        .custom-modal.show {
            opacity: 1;
            pointer-events: all;
        }
        .modal-content-glass {
            background: #1a1a2e;
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 20px;
            padding: 30px;
            width: 90%;
            max-width: 400px;
            text-align: center;
            transform: scale(0.8);
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .custom-modal.show .modal-content-glass {
            transform: scale(1);
        }
    </style>
</head>
<body>

    <div class="bg-animation"></div>

    <section id="view-login" class="view active-view d-flex flex-column justify-content-center align-items-center p-4">
        <div class="glass-panel p-5 text-center" style="max-width: 400px; width: 100%;">
            <div class="mb-4">
                <i class="fa-solid fa-rocket fa-4x text-white" style="filter: drop-shadow(0 0 15px var(--neon-pink)); animation: float 3s ease-in-out infinite;"></i>
            </div>
            <h1 class="fw-bold mb-0 text-white" style="font-family: 'Montserrat'; letter-spacing: 2px;">GYMKHANA</h1>
            <p class="text-white-50 small mb-4" style="letter-spacing: 4px;">LYCÉE OLYMPIQUE</p>
            
            <input type="text" id="team-input" class="glass-input mb-4" placeholder="Nom de l'équipe...">
            <button onclick="app.login()" class="btn-neon fw-bold">
                COMMENCER <i class="fa-solid fa-arrow-right ms-2"></i>
            </button>
        </div>
    </section>

    <section id="view-dashboard" class="view p-3">
        <div class="d-flex justify-content-between align-items-center mb-4 pt-2">
            <div>
                <small class="text-uppercase text-white-50 fw-bold" style="font-size: 0.7rem;">Équipe</small>
                <div id="display-team" class="fw-bold h5 mb-0 text-white">...</div>
            </div>
            <div class="glass-panel px-3 py-1 mb-0 d-flex align-items-center">
                <i class="fa-solid fa-star text-warning me-2"></i> 
                <span class="fw-bold"><span id="completed-count">0</span>/4</span>
            </div>
        </div>

        <div class="glass-panel p-3 mb-4 d-flex justify-content-center align-items-center position-relative" style="height: 220px;">
            <canvas id="progressChart"></canvas>
            <div class="position-absolute text-center" style="pointer-events: none;">
                <h2 id="percent-text" class="fw-bold m-0 text-white" style="font-size: 2.5rem; text-shadow: 0 0 10px rgba(0,0,0,0.5);">0%</h2>
                <small class="text-white-50 text-uppercase" style="font-size: 0.6rem;">Progression</small>
            </div>
        </div>

        <h6 class="text-uppercase text-white-50 fw-bold small mb-3 ps-2">Missions Actives</h6>
        <div id="missions-list">
            </div>
    </section>

    <section id="view-oscars" class="view p-3">
        <div class="text-center mb-5 mt-3">
            <i class="fa-solid fa-crown fa-3x text-warning mb-2"></i>
            <h2 class="fw-bold text-white" style="font-family: 'Montserrat';">LES OSCARS</h2>
            <p class="text-white-50">Cérémonie de remise des prix</p>
        </div>

        <div class="row g-3">
            <div class="col-6">
                <div class="glass-panel oscar-card">
                    <i class="fa-solid fa-language fa-2x text-gold mb-2"></i>
                    <h6 class="fw-bold small mb-1 text-white">Francophones d'Or</h6>
                    <small class="text-white-50 d-block" style="font-size: 0.65rem;">Meilleur niveau linguistique</small>
                </div>
            </div>
            <div class="col-6">
                <div class="glass-panel oscar-card">
                    <i class="fa-solid fa-users fa-2x text-gold mb-2"></i>
                    <h6 class="fw-bold small mb-1 text-white">Esprit d'Équipe</h6>
                    <small class="text-white-50 d-block" style="font-size: 0.65rem;">Meilleure coopération</small>
                </div>
            </div>
            <div class="col-6">
                <div class="glass-panel oscar-card">
                    <i class="fa-solid fa-lightbulb fa-2x text-gold mb-2"></i>
                    <h6 class="fw-bold small mb-1 text-white">Les Innovateurs</h6>
                    <small class="text-white-50 d-block" style="font-size: 0.65rem;">Créativité maximale</small>
                </div>
            </div>
            <div class="col-6">
                <div class="glass-panel oscar-card">
                    <i class="fa-solid fa-leaf fa-2x text-gold mb-2"></i>
                    <h6 class="fw-bold small mb-1 text-white">Gardiens Planète</h6>
                    <small class="text-white-50 d-block" style="font-size: 0.65rem;">Écologie & Durable</small>
                </div>
            </div>
        </div>
    </section>

    <div id="bottom-nav" class="dock-nav d-none">
        <div class="dock-item active" onclick="app.nav('dashboard', this)">
            <i class="fa-solid fa-gamepad"></i>
        </div>
        <div class="dock-item" onclick="app.nav('oscars', this)">
            <i class="fa-solid fa-trophy"></i>
        </div>
    </div>

    <div id="customModal" class="custom-modal">
        <div class="modal-content-glass">
            <div class="mb-3">
                <i id="modal-icon" class="fa-solid fa-user-secret fa-3x text-white"></i>
            </div>
            <h4 id="modal-title" class="fw-bold text-white mb-2">...</h4>
            <p id="modal-desc" class="text-white-50 small mb-4">...</p>
            
            <input type="text" id="secret-code" class="glass-input text-uppercase fs-4 mb-4" placeholder="CODE" maxlength="6">
            
            <button onclick="app.validate()" class="btn-neon">Vérifier</button>
            <button onclick="app.closeModal()" class="btn btn-link text-white-50 mt-3 text-decoration-none btn-sm">Annuler</button>
            
            <div id="feedback-msg" class="mt-3 small fw-bold"></div>
        </div>
    </div>

    <script>
        // --- DATA ---
        const GAME_DATA = {
            missions: [
                { id: 1, title: "Économie (ODD 1)", group: "Les Banquiers", code: "JETON", completed: false, icon: "fa-coins" },
                { id: 2, title: "Climat (ODD 13)", group: "Les Écologistes", code: "FUTUR", completed: false, icon: "fa-temperature-low" },
                { id: 3, title: "Santé (ODD 3)", group: "Les Nutritionnistes", code: "SANTE", completed: false, icon: "fa-heart-pulse" },
                { id: 4, title: "Urbanisme (ODD 11)", group: "Les Architectes", code: "VILLE", completed: false, icon: "fa-city" }
            ],
            teamName: "",
            currentMissionId: null
        };
        
        let progressChart = null;

        // --- APP CONTROLLER ---
        const app = {
            login: () => {
                const input = document.getElementById('team-input').value;
                if (!input) return alert("Veuillez entrer un nom d'équipe !");
                
                GAME_DATA.teamName = input;
                document.getElementById('display-team').innerText = input;
                
                // Transición Suave
                app.switchView('view-login', 'view-dashboard');
                document.getElementById('bottom-nav').classList.remove('d-none');
                
                // Inicializar
                app.renderMissions();
                setTimeout(app.initChart, 300);
            },

            nav: (targetView, el) => {
                // Update Dock
                document.querySelectorAll('.dock-item').forEach(i => i.classList.remove('active'));
                el.classList.add('active');

                // Animate Out current view
                const current = document.querySelector('.active-view');
                if(current) {
                    current.style.opacity = 0;
                    current.style.transform = 'translateY(-20px)';
                    setTimeout(() => current.classList.remove('active-view'), 400);
                }

                // Animate In new view
                setTimeout(() => {
                    const next = document.getElementById(`view-${targetView}`);
                    next.classList.add('active-view');
                    next.style.opacity = 0;
                    next.style.transform = 'translateY(20px)';
                    
                    // Force Reflow
                    void next.offsetWidth;
                    
                    next.style.opacity = 1;
                    next.style.transform = 'translateY(0)';
                }, 400);
            },

            switchView: (from, to) => {
                document.getElementById(from).classList.remove('active-view');
                document.getElementById(to).classList.add('active-view');
            },

            renderMissions: () => {
                const container = document.getElementById('missions-list');
                container.innerHTML = "";

                GAME_DATA.missions.forEach((m, i) => {
                    const isLocked = i > 0 && !GAME_DATA.missions[i-1].completed;
                    const statusClass = m.completed ? 'completed' : (isLocked ? 'locked' : '');
                    const iconStatus = m.completed ? 'fa-check text-success' : (isLocked ? 'fa-lock text-white-50' : 'fa-play text-white');
                    
                    container.innerHTML += `
                        <div class="glass-panel p-3 mission-card ${statusClass} d-flex align-items-center" 
                             onclick="app.openModal(${m.id})">
                            <div class="me-3 bg-dark rounded-circle d-flex justify-content-center align-items-center" 
                                 style="width:45px; height:45px; box-shadow: 0 0 10px rgba(0,0,0,0.5);">
                                <i class="fa-solid ${m.icon} text-white"></i>
                            </div>
                            <div class="flex-grow-1">
                                <small class="text-white-50 text-uppercase fw-bold" style="font-size:0.65rem">
                                    Cherchez: ${m.group}
                                </small>
                                <h6 class="mb-0 fw-bold text-white">${m.title}</h6>
                            </div>
                            <div>
                                <i class="fa-solid ${iconStatus}"></i>
                            </div>
                        </div>
                    `;
                });
                
                // Update stats
                const completed = GAME_DATA.missions.filter(m => m.completed).length;
                document.getElementById('completed-count').innerText = completed;
            },

            openModal: (id) => {
                const m = GAME_DATA.missions.find(x => x.id === id);
                if (m.completed) return; // Ya completada

                GAME_DATA.currentMissionId = id;
                document.getElementById('modal-title').innerText = m.title;
                document.getElementById('modal-desc').innerText = `Trouvez le groupe "${m.group}" pour obtenir le code secret.`;
                document.getElementById('secret-code').value = '';
                document.getElementById('feedback-msg').innerText = '';
                document.getElementById('customModal').classList.add('show');
            },

            closeModal: () => {
                document.getElementById('customModal').classList.remove('show');
            },

            validate: () => {
                const input = document.getElementById('secret-code').value.toUpperCase().trim();
                const m = GAME_DATA.missions.find(x => x.id === GAME_DATA.currentMissionId);
                const fb = document.getElementById('feedback-msg');

                if (input === m.code) {
                    m.completed = true;
                    fb.innerHTML = '<span class="text-info"><i class="fa-solid fa-check"></i> Correct !</span>';
                    
                    // Confetti Effect
                    confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } });

                    setTimeout(() => {
                        app.closeModal();
                        app.renderMissions();
                        app.updateChart();
                    }, 1500);
                } else {
                    fb.innerHTML = '<span class="text-danger">Code incorrect.</span>';
                    // Shake animation input
                    const inp = document.getElementById('secret-code');
                    inp.style.borderColor = 'red';
                    setTimeout(() => inp.style.borderColor = 'rgba(255,255,255,0.2)', 500);
                }
            },

            initChart: () => {
                const ctx = document.getElementById('progressChart').getContext('2d');
                progressChart = new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        datasets: [{
                            data: [0, 4],
                            backgroundColor: ['#00f2fe', 'rgba(255,255,255,0.05)'],
                            borderWidth: 0,
                            borderRadius: 20,
                            cutout: '85%'
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        animation: { animateScale: true, animateRotate: true },
                        plugins: { legend: { display: false }, tooltip: { enabled: false } }
                    }
                });
            },

            updateChart: () => {
                const completed = GAME_DATA.missions.filter(m => m.completed).length;
                const total = GAME_DATA.missions.length;
                
                progressChart.data.datasets[0].data = [completed, total - completed];
                progressChart.update();
                
                document.getElementById('percent-text').innerText = Math.round((completed/total)*100) + '%';
            }
        };

        // Animación Flotante CSS
        const styleSheet = document.createElement("style");
        styleSheet.innerText = `
          @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
          }
        `;
        document.head.appendChild(styleSheet);
    </script>
</body>
</html>
"""

# Renderizamos el HTML en Streamlit con altura fija y scroll permitido
components.html(html_code, height=900, scrolling=True)
