import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURACIÓN DE PÁGINA STREAMLIT ---
st.set_page_config(
    page_title="Gymkhana Gen Z",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ocultamos elementos propios de Streamlit para que parezca una App nativa
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
# Todo el diseño moderno está encapsulado aquí para mantener el rendimiento del lado del cliente.
html_code = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Gymkhana Gen Z</title>
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        /* --- VARIABLES & TEMA GEN Z --- */
        :root {
            --bg-gradient: linear-gradient(-45deg, #1a1a2e, #4a1c40, #0f3460, #e94560);
            --glass-bg: rgba(255, 255, 255, 0.08);
            --glass-border: 1px solid rgba(255, 255, 255, 0.1);
            --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            --neon-blue: #00f2fe;
            --neon-pink: #fe00a1;
            --gold-gradient: linear-gradient(135deg, #fce38a 0%, #f38181 100%);
            --text-color: #fff;
            --font-main: 'Poppins', sans-serif;
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
            background: #1a1a2e;
        }

        /* Fondo Animado */
        .bg-animation {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: var(--bg-gradient);
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
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 20px;
            border: var(--glass-border);
            box-shadow: var(--glass-shadow);
            margin-bottom: 15px;
            transition: transform 0.2s;
        }

        .glass-input {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 50px;
            padding: 15px;
            color: white;
            text-align: center;
            width: 100%;
            font-family: var(--font-main);
            transition: 0.3s;
        }
        .glass-input:focus {
            outline: none;
            border-color: var(--neon-blue);
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.3);
        }

        /* --- BOTONES & UI --- */
        .btn-neon {
            background: linear-gradient(90deg, var(--neon-blue), #4facfe);
            color: #000;
            border: none;
            padding: 12px;
            border-radius: 50px;
            font-weight: 800;
            text-transform: uppercase;
            width: 100%;
            box-shadow: 0 0 10px rgba(0, 242, 254, 0.5);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .btn-neon:active {
            transform: scale(0.95);
            box-shadow: 0 0 5px rgba(0, 242, 254, 0.5);
        }

        /* --- TRANSICIONES (SPA FEEL) --- */
        .view {
            display: none;
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.4s ease, transform 0.4s ease;
            height: 100%;
            overflow-y: auto;
            padding-bottom: 100px; /* Espacio para el menú */
        }

        .active-view {
            display: block;
            opacity: 1;
            transform: translateY(0);
        }

        /* --- MISIONES --- */
        .mission-item {
            cursor: pointer;
        }
        .mission-item:active { transform: scale(0.98); }
        .mission-item.locked {
            opacity: 0.5;
            filter: grayscale(1);
            pointer-events: none;
        }
        .mission-item.completed {
            border-left: 4px solid var(--neon-blue);
            background: rgba(0, 242, 254, 0.05);
        }

        /* --- OSCARS --- */
        .oscar-card {
            border: 1px solid rgba(252, 227, 138, 0.2);
            text-align: center;
            height: 100%;
            padding: 15px;
            transition: transform 0.3s;
        }
        .oscar-card:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.12);
        }
        .text-gold {
            background: var(--gold-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 20px rgba(252, 227, 138, 0.3);
        }

        /* --- DOCK NAV (MENU) --- */
        .dock-nav {
            position: fixed;
            bottom: 25px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(20, 20, 30, 0.85);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            padding: 10px 30px;
            border-radius: 50px;
            display: flex;
            gap: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            border: 1px solid rgba(255,255,255,0.1);
            z-index: 1000;
        }

        .dock-item {
            color: rgba(255,255,255,0.4);
            font-size: 1.6rem;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            cursor: pointer;
        }

        .dock-item.active {
            color: var(--neon-blue);
            transform: translateY(-8px) scale(1.2);
            text-shadow: 0 0 15px var(--neon-blue);
        }
        
        /* Modal Glass */
        .glass-modal {
            background: rgba(26, 26, 46, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.2);
            color: white;
            border-radius: 20px;
        }
    </style>
</head>
<body>

    <div class="bg-animation"></div>

    <section id="view-login" class="view active-view d-flex flex-column justify-content-center align-items-center p-4">
        <div class="glass-panel p-5 text-center" style="max-width: 400px; width: 100%;">
            <div class="mb-4">
                <i class="fa-solid fa-rocket fa-4x text-white" style="filter: drop-shadow(0 0 10px var(--neon-pink));"></i>
            </div>
            <h1 class="fw-bold mb-0" style="letter-spacing: 2px;">GYMKHANA</h1>
            <p class="text-white-50 small mb-4" style="letter-spacing: 3px;">INNOVATION & ODD</p>
            
            <input type="text" id="team-input" class="glass-input mb-3" placeholder="Nom de l'équipe">
            <button onclick="app.login()" class="btn-neon fw-bold">
                START <i class="fa-solid fa-play ms-2"></i>
            </button>
        </div>
    </section>

    <section id="view-dashboard" class="view p-3">
        <div class="d-flex justify-content-between align-items-center mb-4 pt-2">
            <div>
                <small class="text-uppercase text-white-50 fw-bold" style="font-size: 0.65rem;">Team</small>
                <div id="display-team" class="fw-bold h5 mb-0 text-white text-truncate" style="max-width: 150px;">...</div>
            </div>
            <div class="glass-panel px-3 py-1 mb-0 d-flex align-items-center">
                <i class="fa-solid fa-bolt text-warning me-2"></i> 
                <span class="fw-bold"><span id="medal-count">0</span>/4</span>
            </div>
        </div>

        <div class="glass-panel p-3 mb-4 d-flex justify-content-center align-items-center position-relative" style="height: 200px;">
            <canvas id="progressChart"></canvas>
            <div class="position-absolute text-center" style="pointer-events: none;">
                <h2 id="percent-text" class="fw-bold m-0 text-white" style="font-size: 2rem;">0%</h2>
                <small class="text-white-50 text-uppercase" style="font-size: 0.6rem;">Complété</small>
            </div>
        </div>

        <h6 class="text-uppercase text-white-50 fw-bold small mb-3 ps-2">Missions Actives</h6>
        <div id="missions-list">
            </div>
    </section>

    <section id="view-oscars" class="view p-3">
        <div class="text-center mb-4 pt-3">
            <h2 class="fw-bold mb-1">Les Oscars</h2>
            <p class="text-white-50 small">Cérémonie de l'Innovation</p>
        </div>

        <div class="row g-3">
            <div class="col-6">
                <div class="glass-panel oscar-card">
                    <i class="fa-solid fa-microphone-lines fa-2x text-gold mb-2"></i>
                    <h6 class="fw-bold small mb-1">Francophones d'Or</h6>
                    <small class="text-white-50 lh-1 d-block" style="font-size: 0.65rem;">Meilleur Linguistique</small>
                </div>
            </div>
            <div class="col-6">
                <div class="glass-panel oscar-card">
                    <i class="fa-solid fa-users fa-2x text-gold mb-2"></i>
                    <h6 class="fw-bold small mb-1">Esprit d'Équipe</h6>
                    <small class="text-white-50 lh-1 d-block" style="font-size: 0.65rem;">Coopération (ODD 17)</small>
                </div>
            </div>
            <div class="col-6">
                <div class="glass-panel oscar-card">
                    <i class="fa-solid fa-lightbulb fa-2x text-gold mb-2"></i>
                    <h6 class="fw-bold small mb-1">Les Innovateurs</h6>
                    <small class="text-white-50 lh-1 d-block" style="font-size: 0.65rem;">Créativité</small>
                </div>
            </div>
            <div class="col-6">
                <div class="glass-panel oscar-card">
                    <i class="fa-solid fa-earth-europe fa-2x text-gold mb-2"></i>
                    <h6 class="fw-bold small mb-1">Gardiens Planète</h6>
                    <small class="text-white-50 lh-1 d-block" style="font-size: 0.65rem;">Écologie (ODD 13)</small>
                </div>
            </div>
        </div>

        <div class="glass-panel mt-4 p-3 border-0" style="background: linear-gradient(135deg, #fce38a 0%, #f38181 100%);">
            <div class="d-flex align-items-center text-dark">
                <div class="me-3 bg-white rounded-circle d-flex justify-content-center align-items-center" style="width: 45px; height: 45px;">
                    <i class="fa-solid fa-crown text-warning"></i>
                </div>
                <div>
                    <h6 class="fw-bold mb-0">Grande Finale</h6>
                    <small class="fw-bold opacity-75">Semaine du 16 Juin</small>
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

    <div class="modal fade" id="missionModal" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content glass-modal">
                <div class="modal-body text-center p-4">
                    <div class="mb-3">
                        <i id="modal-icon" class="fa-solid fa-user-group fa-3x text-white"></i>
                    </div>
                    <h4 id="modal-title" class="fw-bold mb-2">...</h4>
                    
                    <div class="glass-panel p-3 mb-4 bg-transparent border border-secondary">
                        <p id="modal-desc" class="text-white small mb-0 fw-bold">...</p>
                    </div>
                    
                    <label class="small text-white-50 text-uppercase mb-2">Code Secret des Experts</label>
                    <input type="text" id="secret-code" class="glass-input text-uppercase fs-4 mb-3" placeholder="CODE" maxlength="8">
                    
                    <button onclick="app.validate()" class="btn-neon">Vérifier</button>
                    <div id="feedback-msg" class="mt-3 small fw-bold"></div>
                </div>
                <div class="modal-footer border-0 justify-content-center">
                    <button type="button" class="btn btn-sm text-white-50" data-bs-dismiss="modal">Fermer</button>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // --- DATOS DEL JUEGO ---
        const GAME_DATA = {
            missions: [
                { id: 1, title: "Économie (ODD 1)", group: "Les Banquiers", code: "JETON", completed: false },
                { id: 2, title: "Climat (ODD 13)", group: "Les Écologistes", code: "FUTUR", completed: false },
                { id: 3, title: "Santé (ODD 3)", group: "Les Nutritionnistes", code: "SANTE", completed: false },
                { id: 4, title: "Urbanisme (ODD 11)", group: "Les Architectes", code: "VILLE", completed: false }
            ],
            teamName: "",
            currentMissionId: null
        };
        let progressChart = null;

        // --- LÓGICA DE LA APP ---
        const app = {
            login: () => {
                const input = document.getElementById('team-input').value;
                if (!input) return alert("Nom requis!");
                GAME_DATA.teamName = input;
                document.getElementById('display-team').innerText = input;
                
                // Transición al Dashboard
                app.switchView('view-login', 'view-dashboard');
                document.getElementById('bottom-nav').classList.remove('d-none');
                
                // Renderizar
                app.renderMissions();
                setTimeout(app.initChart, 200); // Pequeño delay para asegurar que el canvas existe
            },

            nav: (targetView, el) => {
                // Actualizar menú activo
                document.querySelectorAll('.dock-item').forEach(i => i.classList.remove('active'));
                el.classList.add('active');

                // Ocultar vistas con animación
                document.querySelectorAll('.view').forEach(v => {
                    if(v.classList.contains('active-view')) {
                        v.style.opacity = 0;
                        v.style.transform = 'translateY(-20px)';
                        setTimeout(() => v.classList.remove('active-view'), 300);
                    }
                });

                // Mostrar nueva vista
                setTimeout(() => {
                    const next = document.getElementById(`view-${targetView}`);
                    next.classList.add('active-view');
                    // Forzar reflow para reiniciar animación
                    next.style.opacity = 0;
                    next.style.transform = 'translateY(20px)';
                    void next.offsetWidth; 
                    
                    next.style.opacity = 1;
                    next.style.transform = 'translateY(0)';
                }, 300);
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
                    const icon = m.completed ? 'fa-check text-info' : (isLocked ? 'fa-lock text-white-50' : 'fa-play text-white');
                    
                    container.innerHTML += `
                        <div class="glass-panel p-3 mb-3 mission-item d-flex align-items-center ${statusClass}" 
                             onclick="app.openMission(${m.id})">
                            <div class="me-3 bg-dark rounded-circle d-flex justify-content-center align-items-center" 
                                 style="width:40px; height:40px; box-shadow: 0 0 10px rgba(0,0,0,0.3);">
                                <i class="fa-solid ${icon}"></i>
                            </div>
                            <div class="flex-grow-1">
                                <small class="text-white-50 text-uppercase fw-bold" style="font-size:0.6rem">
                                    Cherchez: ${m.group}
                                </small>
                                <h6 class="mb-0 fw-bold text-white">${m.title}</h6>
                            </div>
                        </div>
                    `;
                });
                app.updateStats();
            },

            openMission: (id) => {
                const m = GAME_DATA.missions.find(x => x.id === id);
                if (m.completed) return;

                GAME_DATA.currentMissionId = id;
                document.getElementById('modal-title').innerText = m.title;
                document.getElementById('modal-desc').innerText = `Trouvez le groupe "${m.group}" pour obtenir le code.`;
                document.getElementById('secret-code').value = '';
                document.getElementById('feedback-msg').innerText = '';
                
                new bootstrap.Modal(document.getElementById('missionModal')).show();
            },

            validate: () => {
                const input = document.getElementById('secret-code').value.toUpperCase().trim();
                const m = GAME_DATA.missions.find(x => x.id === GAME_DATA.currentMissionId);
                const fb = document.getElementById('feedback-msg');

                if (input === m.code) {
                    m.completed = true;
                    fb.innerHTML = '<span class="text-info"><i class="fa-solid fa-star"></i> Bravo! Code Correct.</span>';
                    
                    setTimeout(() => {
                        bootstrap.Modal.getInstance(document.getElementById('missionModal')).hide();
                        app.renderMissions();
                        app.updateChart();
                    }, 1000);
                } else {
                    fb.innerHTML = '<span class="text-danger">Code incorrect. Réessayez.</span>';
                }
            },

            updateStats: () => {
                const completed = GAME_DATA.missions.filter(m => m.completed).length;
                document.getElementById('medal-count').innerText = completed;
            },

            initChart: () => {
                if(progressChart) progressChart.destroy();
                const ctx = document.getElementById('progressChart').getContext('2d');
                progressChart = new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Complété', 'Restant'],
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
    </script>
</body>
</html>
"""

# RENDERIZADO EN STREAMLIT
# Usamos scrolling=True para asegurar que se puede navegar en móviles pequeños
components.html(html_code, height=900, scrolling=True)
