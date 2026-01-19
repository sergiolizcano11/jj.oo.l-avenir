import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="J.O. De l'Avenir",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🏅"
)

# Ocultar UI nativa
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
    <title>J.O. App</title>
    
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
            padding-bottom: 90px;
        }

        /* --- PANELES GENÉRICOS --- */
        .solid-panel {
            background-color: var(--card-bg);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            border: 1px solid #333;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }

        /* --- GRID DE AVATARES --- */
        .avatar-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin-bottom: 20px;
        }
        .avatar-item {
            background: #2C2C2C;
            border: 2px solid #444;
            border-radius: 10px;
            padding: 10px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
        }
        .avatar-item:hover { transform: scale(1.05); border-color: var(--primary); }
        .avatar-item.selected {
            background: rgba(77, 121, 255, 0.2);
            border-color: var(--primary);
            box-shadow: 0 0 10px var(--primary);
        }
        .avatar-item i { font-size: 1.5rem; color: #fff; }

        /* --- BOTONES --- */
        .btn-solid {
            background-color: var(--primary);
            color: white; border: none; border-radius: 8px;
            padding: 12px; width: 100%; font-weight: 700;
            text-transform: uppercase; font-family: var(--font-head);
            margin-top: 10px;
        }
        .btn-solid:active { background-color: #3a5bbf; transform: scale(0.98); }
        
        .btn-outline {
            background: transparent; border: 2px solid #555;
            color: #aaa; border-radius: 8px; padding: 10px; width: 100%;
            font-weight: 700; margin-top: 5px;
        }
        .btn-outline.active {
            border-color: var(--success); color: var(--success);
            background: rgba(40, 167, 69, 0.1);
        }

        /* --- INPUTS --- */
        .solid-input {
            background-color: #2C2C2C; border: 1px solid #444;
            color: white; padding: 12px; border-radius: 8px;
            width: 100%; text-align: center; font-size: 1.1rem;
            margin-bottom: 10px;
        }
        .trait-selector {
            display: flex; gap: 5px; overflow-x: auto; padding-bottom: 10px;
        }
        .trait-tag {
            background: #333; padding: 5px 15px; border-radius: 20px;
            white-space: nowrap; cursor: pointer; border: 1px solid #444;
            font-size: 0.85rem;
        }
        .trait-tag.selected {
            background: var(--accent); color: black; border-color: var(--accent); font-weight: bold;
        }

        /* --- VISTAS --- */
        .view { display: none; padding: 20px; min-height: 100vh; }
        .active-view { display: block; animation: fadeIn 0.4s; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        /* --- UI PRINCIPAL --- */
        .home-btn {
            background-color: var(--card-bg); border: 1px solid #444;
            border-radius: 15px; padding: 25px 15px; text-align: center;
            cursor: pointer; height: 100%; display: flex; flex-direction: column;
            justify-content: center; align-items: center;
        }
        .dock-nav {
            position: fixed; bottom: 0; left: 0; width: 100%;
            background-color: #1E1E1E; border-top: 1px solid #333;
            display: flex; justify-content: space-around;
            padding: 15px 0; z-index: 1000;
        }
        .dock-item { font-size: 1.5rem; color: #666; cursor: pointer; }
        .dock-item.active { color: var(--primary); transform: translateY(-5px); }
        
        .phase-card { cursor: pointer; border-left: 4px solid #555; background: #252525; padding: 15px; margin-bottom: 10px; border-radius: 8px;}
        .phase-card.completed { border-left-color: var(--success); }
        .odd-badge { font-size: 0.65rem; background: #333; padding: 2px 6px; border-radius: 4px; color: var(--accent); font-weight: bold; margin-bottom: 4px; display: inline-block; }

        /* Modal */
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

    <section id="view-avatar" class="view active-view">
        <div class="text-center mt-4 mb-4">
            <h2 style="font-family: var(--font-head);">CRÉEZ VOTRE PROFIL</h2>
            <p class="text-secondary small">CHOISISSEZ VOTRE CHAMPION</p>
        </div>

        <div class="avatar-grid" id="sprite-container"></div>

        <div class="solid-panel mt-4">
            <label class="small text-secondary mb-2 d-block text-start">VOTRE NOM</label>
            <input type="text" id="player-name" class="solid-input" placeholder="Pseudo...">
            
            <label class="small text-secondary mb-2 d-block text-start mt-3">VOTRE SUPER-POUVOIR (ADJECTIF)</label>
            <div class="trait-selector" id="trait-container"></div>
            <input type="hidden" id="selected-trait">
        </div>

        <button onclick="app.saveProfile()" class="btn-solid mt-2">ENTRER DANS L'APP <i class="fa-solid fa-arrow-right"></i></button>
    </section>

    <section id="view-home" class="view">
        <div class="d-flex align-items-center justify-content-between mb-4 mt-3">
            <div>
                <h1 style="font-family: var(--font-head); font-size: 1.8rem; line-height: 1;">J.O. AVENIR</h1>
                <small class="text-secondary">LYCÉE OLYMPIQUE</small>
            </div>
            <div class="text-center" onclick="app.showView('view-avatar')" style="cursor:pointer">
                <div id="mini-avatar" style="font-size: 1.5rem; color: var(--accent);"></div>
            </div>
        </div>
        
        <div id="home-team-badge" class="badge bg-secondary mb-4 px-3 py-2 w-100" style="font-size: 0.9rem;">
            <i class="fa-solid fa-users-slash me-2"></i> Pas d'équipe (Voir Phase 2)
        </div>

        <div class="row g-3">
            <div class="col-6">
                <div class="home-btn" onclick="app.nav('dashboard', 'nav-dash')">
                    <i class="fa-solid fa-list-check"></i>
                    <h3>PHASES</h3>
                </div>
            </div>
            <div class="col-6">
                <div class="home-btn" onclick="app.nav('oscars', 'nav-oscars')">
                    <i class="fa-solid fa-award text-warning"></i>
                    <h3>ÉVALUATION</h3>
                </div>
            </div>
             <div class="col-12">
                <div class="home-btn flex-row gap-3" style="opacity: 0.6;" onclick="alert('Bientôt!')">
                    <i class="fa-solid fa-flag-checkered text-danger mb-0"></i>
                    <h3 class="mb-0">GRANDE GYMKHANA</h3>
                </div>
            </div>
        </div>
    </section>

    <section id="view-dashboard" class="view">
        <h4 class="fw-bold mb-3" style="font-family: var(--font-head);">PROGRESSION</h4>
        <div class="solid-panel d-flex justify-content-center position-relative mb-4" style="height: 150px;">
            <canvas id="progressChart"></canvas>
            <div class="position-absolute top-50 start-50 translate-middle text-center">
                <h2 id="percent-text" class="m-0 fw-bold">0%</h2>
            </div>
        </div>
        <div id="missions-list"></div>
    </section>

    <section id="view-debate" class="view">
        <div class="text-center mt-4 mb-4">
            <h2 style="font-family: var(--font-head);">ZONE DE DÉBAT</h2>
            <p class="text-secondary small">PHASE 2: CRÉATION D'ÉQUIPE</p>
        </div>

        <div class="solid-panel d-flex align-items-center bg-black border-primary">
            <div id="debate-avatar" class="me-3 text-center" style="font-size: 2rem; width: 50px;"></div>
            <div>
                <h5 id="debate-name" class="mb-0 fw-bold text-white">Nom</h5>
                <small id="debate-trait" class="badge bg-warning text-dark">Trait</small>
            </div>
        </div>

        <div class="solid-panel">
            <h6 class="fw-bold mb-3"><i class="fa-solid fa-users text-info"></i> L'ÉQUIPE</h6>
            <p class="small text-secondary">Négociez avec la classe. L'équipe est-elle équilibrée ?</p>
            
            <input type="text" id="team-name-create" class="solid-input mb-3" placeholder="NOM DE L'ÉQUIPE">
            
            <div class="p-3 border rounded mb-3" style="border-color: #444 !important;">
                <label class="small text-secondary mb-2">AUTO-VALIDATION (CUA/ODD 5)</label>
                <button id="check-mixed" class="btn-outline" onclick="this.classList.toggle('active')">
                    <i class="fa-regular fa-square"></i> Équipe Mixte
                </button>
                <button id="check-skills" class="btn-outline" onclick="this.classList.toggle('active')">
                    <i class="fa-regular fa-square"></i> Compétences Variées
                </button>
                <button id="check-class" class="btn-outline" onclick="this.classList.toggle('active')">
                    <i class="fa-regular fa-square"></i> Validé par la classe
                </button>
            </div>

            <button onclick="app.finalizeTeam()" class="btn-solid">CONFIRMER L'ÉQUIPE</button>
        </div>
        <button onclick="app.nav('dashboard')" class="btn btn-link text-secondary text-decoration-none w-100">Retour</button>
    </section>

    <section id="view-oscars" class="view">
        <h2 class="text-center fw-bold mb-4">CRITÈRES</h2>
        <div class="row g-3">
            <div class="col-6"><div class="solid-panel text-center"><i class="fa-solid fa-comments text-warning fa-2x"></i><h6>Linguistique</h6></div></div>
            <div class="col-6"><div class="solid-panel text-center"><i class="fa-solid fa-users text-warning fa-2x"></i><h6>Social</h6></div></div>
            <div class="col-6"><div class="solid-panel text-center"><i class="fa-solid fa-leaf text-warning fa-2x"></i><h6>ODD</h6></div></div>
            <div class="col-6"><div class="solid-panel text-center"><i class="fa-solid fa-lightbulb text-warning fa-2x"></i><h6>Innovation</h6></div></div>
        </div>
    </section>

    <div id="app-dock" class="dock-nav" style="display:none;">
        <div id="nav-home" class="dock-item active" onclick="app.nav('home', this)"><i class="fa-solid fa-house"></i></div>
        <div id="nav-dash" class="dock-item" onclick="app.nav('dashboard', this)"><i class="fa-solid fa-list-check"></i></div>
        <div id="nav-oscars" class="dock-item" onclick="app.nav('oscars', this)"><i class="fa-solid fa-award"></i></div>
    </div>

    <div id="customModal" class="custom-modal">
        <div class="modal-content-solid">
            <h4 id="modal-title" class="fw-bold mb-2">...</h4>
            <div class="badge bg-warning text-dark mb-2" id="modal-odd">ODD</div>
            <p id="modal-desc" class="text-secondary small mb-4">...</p>
            
            <input type="text" id="user-input" class="solid-input text-uppercase" placeholder="CODE PROFESSEUR">
            <button onclick="app.validate()" class="btn-solid mb-2">VALIDER</button>
            <button onclick="app.closeModal()" class="btn btn-link text-secondary text-decoration-none">Fermer</button>
            <div id="feedback-msg" class="mt-3 small fw-bold"></div>
        </div>
    </div>

    <script>
        // --- DATOS ---
        const SPRITES = [
            "fa-dragon", "fa-ghost", "fa-robot", "fa-cat", 
            "fa-dog", "fa-crow", "fa-spider", "fa-fish",
            "fa-bolt", "fa-fire", "fa-snowflake", "fa-leaf",
            "fa-user-astronaut", "fa-user-ninja", "fa-user-secret", "fa-child-reaching"
        ];
        const TRAITS = ["Fort", "Rapide", "Intelligent", "Sociable", "Créatif", "Organisé", "Drôle", "Calme"];

        // FASES SEGÚN CRONOGRAMA
        const DATA = {
            user: { sprite: "", name: "", trait: "" },
            teamName: "",
            missions: [
                { id: 1, type: "code", code: "MONNAIE", title: "L'Argent Solidaire", odd: "ODD 1 & 12",
                  icon: "fa-coins", desc: "Sept-Oct: Création de la monnaie.", completed: false },
                  
                { id: 2, type: "team", title: "Équipes Inclusives", odd: "ODD 5 & 10",
                  icon: "fa-users", desc: "Nov-Dec: Création et débat des équipes.", completed: false },
                  
                { id: 3, type: "code", code: "ECO", title: "Obstacles Avenir", odd: "ODD 13",
                  icon: "fa-recycle", desc: "Jan-Fév: Design épreuves recyclées.", completed: false },
                  
                { id: 4, type: "code", code: "RULES", title: "Règlement", odd: "ODD 16",
                  icon: "fa-scale-balanced", desc: "Fév-Mars: Normes de fair-play.", completed: false },
                  
                { id: 5, type: "code", code: "FOOD", title: "Ravitaillement", odd: "ODD 3",
                  icon: "fa-apple-whole", desc: "Avril-Mai: Snacks sains.", completed: false },
                  
                { id: 6, type: "code", code: "MAP", title: "Plan Parcours", odd: "ODD 11",
                  icon: "fa-map", desc: "Mai-Juin: Tracé du plan.", completed: false }
            ],
            currentId: null
        };
        let chart = null;

        const app = {
            init: () => {
                const grid = document.getElementById('sprite-container');
                SPRITES.forEach(icon => {
                    const div = document.createElement('div');
                    div.className = "avatar-item";
                    div.innerHTML = `<i class="fa-solid ${icon}"></i>`;
                    div.onclick = () => {
                        document.querySelectorAll('.avatar-item').forEach(el => el.classList.remove('selected'));
                        div.classList.add('selected');
                        DATA.user.sprite = icon;
                    };
                    grid.appendChild(div);
                });

                const tCont = document.getElementById('trait-container');
                TRAITS.forEach(t => {
                    const span = document.createElement('span');
                    span.className = "trait-tag";
                    span.innerText = t;
                    span.onclick = () => {
                        document.querySelectorAll('.trait-tag').forEach(el => el.classList.remove('selected'));
                        span.classList.add('selected');
                        DATA.user.trait = t;
                        document.getElementById('selected-trait').value = t;
                    };
                    tCont.appendChild(span);
                });
            },

            // --- PERFIL INDIVIDUAL (INICIO) ---
            saveProfile: () => {
                const name = document.getElementById('player-name').value;
                if(!DATA.user.sprite || !name || !DATA.user.trait) {
                    return alert("Complétez votre profil !");
                }
                DATA.user.name = name;
                
                // Mostrar en la app
                document.getElementById('mini-avatar').innerHTML = `<i class="fa-solid ${DATA.user.sprite}"></i>`;
                
                // Ir al Home
                app.showView('view-home');
                document.getElementById('app-dock').style.display = 'flex';
            },

            // --- NAVEGACIÓN ---
            nav: (viewName, el) => {
                document.querySelectorAll('.dock-item').forEach(i => i.classList.remove('active'));
                if(el) {
                    if(typeof el === 'string') document.getElementById(el).classList.add('active');
                    else el.classList.add('active');
                }
                app.showView('view-' + viewName);
                if(viewName === 'dashboard') {
                    app.renderList();
                    setTimeout(app.initChart, 100);
                }
            },

            showView: (id) => {
                document.querySelectorAll('.view').forEach(v => v.classList.remove('active-view'));
                document.getElementById(id).classList.add('active-view');
            },

            // --- RENDERIZADO DE FASES ---
            renderList: () => {
                const list = document.getElementById('missions-list');
                list.innerHTML = "";
                DATA.missions.forEach(m => {
                    const status = m.completed ? 'completed' : '';
                    const locked = (!m.completed && m.id > 1 && !DATA.missions[m.id-2].completed) ? 'locked' : '';
                    const iconCheck = m.completed ? 'fa-check text-success' : (locked ? 'fa-lock text-secondary' : 'fa-play text-white');
                    
                    // Si es Fase 2 (Equipo), usamos una función especial para abrir el Debate
                    const onClickAction = (m.id === 2 && !locked) ? `app.goToDebate()` : `app.openModal(${m.id})`;

                    list.innerHTML += `
                    <div class="solid-panel phase-card d-flex align-items-center ${status} ${locked}" onclick="${onClickAction}">
                        <div class="me-3 text-center" style="width: 40px;">
                            <i class="fa-solid ${m.icon} fa-xl text-secondary"></i>
                        </div>
                        <div class="flex-grow-1">
                            <span class="odd-badge">${m.odd}</span>
                            <h6 class="mb-0 fw-bold text-white">${m.title}</h6>
                        </div>
                        <i class="fa-solid ${iconCheck}"></i>
                    </div>`;
                });
            },

            // --- FASE 2: DEBATE EQUIPOS ---
            goToDebate: () => {
                // Verificar si ya está completada
                if(DATA.missions[1].completed) return;

                // Llenar datos de la ficha de debate con el perfil del usuario
                document.getElementById('debate-avatar').innerHTML = `<i class="fa-solid ${DATA.user.sprite} text-white"></i>`;
                document.getElementById('debate-name').innerText = DATA.user.name;
                document.getElementById('debate-trait').innerText = DATA.user.trait;
                
                app.showView('view-debate');
            },

            finalizeTeam: () => {
                const team = document.getElementById('team-name-create').value;
                const c1 = document.getElementById('check-mixed').classList.contains('active');
                const c2 = document.getElementById('check-skills').classList.contains('active');
                const c3 = document.getElementById('check-class').classList.contains('active');

                if(!team) return alert("Nom de l'équipe ?");
                if(!c1 || !c2 || !c3) return alert("Validez les critères !");

                DATA.teamName = team;
                DATA.missions[1].completed = true; // Fase 2 Completada

                // Actualizar UI
                const badge = document.getElementById('home-team-badge');
                badge.className = "badge bg-success mb-4 px-3 py-2 w-100";
                badge.innerHTML = `<i class="fa-solid fa-users me-2"></i> ${team}`;

                confetti();
                app.nav('dashboard');
            },

            // --- MODAL GENÉRICO (FASES CÓDIGO) ---
            openModal: (id) => {
                DATA.currentId = id;
                const m = DATA.missions.find(x => x.id === id);
                if(m.completed) return;
                
                document.getElementById('modal-title').innerText = m.title;
                document.getElementById('modal-desc').innerText = m.desc;
                document.getElementById('modal-odd').innerText = m.odd;
                document.getElementById('user-input').value = "";
                document.getElementById('feedback-msg').innerText = "";
                document.getElementById('customModal').classList.add('show');
            },
            closeModal: () => document.getElementById('customModal').classList.remove('show'),

            validate: () => {
                const inp = document.getElementById('user-input').value.trim().toUpperCase();
                const m = DATA.missions.find(x => x.id === DATA.currentId);
                const fb = document.getElementById('feedback-msg');

                if(inp === m.code) {
                    m.completed = true;
                    fb.innerText = "Validé !"; fb.style.color = "#28a745";
                    confetti();
                    setTimeout(() => { app.closeModal(); app.renderList(); app.initChart(); }, 1000);
                } else {
                    fb.innerText = "Code Incorrect"; fb.style.color = "#dc3545";
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
                const c = DATA.missions.filter(m => m.completed).length;
                const t = DATA.missions.length;
                chart.data.datasets[0].data = [c, t-c];
                chart.update();
                document.getElementById('percent-text').innerText = Math.round((c/t)*100) + "%";
            }
        };

        app.init();
    </script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=True)
