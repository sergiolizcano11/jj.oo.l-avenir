import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="J.O. De l'Avenir",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🏅"
)

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding: 0 !important; margin: 0 !important;}
        iframe {height: 100vh !important;} 
    </style>
""", unsafe_allow_html=True)

# --- CÓDIGO FRONTEND ---
html_code = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>J.O. App</title>
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Montserrat:wght@800&family=Reenie+Beanie&display=swap" rel="stylesheet">
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
            --font-hand: 'Reenie Beanie', cursive;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: var(--font-body);
            margin: 0; padding: 0;
            overflow-x: hidden;
            padding-bottom: 90px;
        }

        /* --- UI BASE --- */
        .solid-panel {
            background-color: var(--card-bg);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            border: 1px solid #333;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }

        .btn-solid {
            background-color: var(--primary);
            color: white; border: none; border-radius: 8px;
            padding: 12px; width: 100%; font-weight: 700;
            text-transform: uppercase; font-family: var(--font-head);
            margin-top: 10px; cursor: pointer; transition: 0.2s;
        }
        .btn-solid:active { transform: scale(0.98); background-color: #3a5bbf; }

        .btn-outline {
            background: transparent; border: 2px solid #555;
            color: #aaa; border-radius: 8px; padding: 10px; width: 100%;
            font-weight: 700; margin-top: 5px; cursor: pointer;
        }
        .btn-outline.active {
            border-color: var(--success); color: var(--success);
            background: rgba(40, 167, 69, 0.1);
        }

        .solid-input, .solid-textarea {
            background-color: #2C2C2C; border: 1px solid #444;
            color: white; padding: 12px; border-radius: 8px;
            width: 100%; font-size: 1rem; margin-bottom: 10px;
            font-family: var(--font-body); text-align: center;
        }
        .solid-textarea { text-align: left; }

        /* --- VISTAS --- */
        .view { display: none; padding: 20px; min-height: 100vh; }
        .active-view { display: block; animation: fadeIn 0.4s; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        /* --- RADAR CHART CONTAINER --- */
        .radar-container {
            background: #222; border-radius: 15px; padding: 10px;
            border: 1px solid #444; height: 250px; position: relative;
        }

        /* --- CONTRATO FAIR PLAY --- */
        .parchment {
            background: #fdfbf7; color: #333; padding: 20px; border-radius: 5px;
            box-shadow: 0 0 20px rgba(0,0,0,0.5); font-family: var(--font-body);
            position: relative; border: 10px solid #2C2C2C;
        }
        .parchment h4 { font-family: var(--font-head); color: #000; text-transform: uppercase; border-bottom: 2px solid #000; padding-bottom: 10px; }
        .signature-pad {
            width: 100%; height: 100px; border: 2px dashed #999;
            background: rgba(255,255,255,0.5); margin-top: 20px;
            display: flex; align-items: center; justify-content: center;
            font-family: var(--font-hand); font-size: 2rem; color: #000080;
            cursor: pointer; position: relative;
        }
        .signature-pad::after { content: 'Signez ici (Cliquez)'; font-family: var(--font-body); font-size: 0.8rem; color: #999; position: absolute; bottom: 5px; }
        .signature-pad.signed::after { content: ''; }

        /* --- DOCK --- */
        .dock-nav {
            position: fixed; bottom: 0; left: 0; width: 100%;
            background-color: #1E1E1E; border-top: 1px solid #333;
            display: flex; justify-content: space-around;
            padding: 15px 0; z-index: 1000;
        }
        .dock-item { font-size: 1.4rem; color: #666; cursor: pointer; }
        .dock-item.active { color: var(--primary); transform: translateY(-5px); }

        /* --- UTILIDADES --- */
        .avatar-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 20px; }
        .avatar-item { background: #2C2C2C; border: 2px solid #444; border-radius: 10px; padding: 10px; text-align: center; cursor: pointer; }
        .avatar-item.selected { background: rgba(77, 121, 255, 0.2); border-color: var(--primary); }
        .trait-tag { background: #333; padding: 5px 15px; border-radius: 20px; white-space: nowrap; cursor: pointer; border: 1px solid #444; font-size: 0.85rem; margin-right: 5px;}
        .trait-tag.selected { background: var(--accent); color: black; font-weight: bold; }
        .trait-selector { display: flex; overflow-x: auto; padding-bottom: 10px; }
        .phase-card { cursor: pointer; border-left: 4px solid #555; background: #252525; padding: 15px; margin-bottom: 10px; border-radius: 8px;}
        .phase-card.completed { border-left-color: var(--success); }
        .odd-badge { font-size: 0.65rem; background: #333; padding: 2px 6px; border-radius: 4px; color: var(--accent); font-weight: bold; margin-bottom: 4px; display: inline-block; }
        
        /* Modal */
        .custom-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.95); z-index: 2000; justify-content: center; align-items: center; }
        .custom-modal.show { display: flex; }
        .modal-content-solid { background: var(--card-bg); border: 1px solid #444; border-radius: 12px; padding: 30px; width: 90%; max-width: 400px; text-align: center; }
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
            <label class="small text-secondary mb-2 d-block text-start">NOM</label>
            <input type="text" id="player-name" class="solid-input" placeholder="Pseudo...">
            <label class="small text-secondary mb-2 d-block text-start mt-3">SUPER-POUVOIR (Important pour l'équipe)</label>
            <div class="trait-selector" id="trait-container"></div>
            <input type="hidden" id="selected-trait">
        </div>
        <button onclick="app.saveProfile()" class="btn-solid mt-2">ENTRER <i class="fa-solid fa-arrow-right"></i></button>
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
        
        <div class="solid-panel p-3 mb-4">
            <div class="d-flex justify-content-between align-items-end">
                <h6 class="mb-0 fw-bold text-white"><i class="fa-solid fa-earth-americas text-warning me-2"></i> IMPACT GLOBAL</h6>
                <small class="text-accent fw-bold">CLASSE</small>
            </div>
            <div style="background: #444; height: 15px; border-radius: 10px; overflow: hidden; margin-top: 8px;">
                <div style="background: linear-gradient(90deg, #FFD93D, #FF6B6B); height: 100%; width: 40%;"></div>
            </div>
        </div>

        <div id="home-team-badge" class="badge bg-secondary mb-4 px-3 py-2 w-100" style="font-size: 0.9rem;">
            <i class="fa-solid fa-users-slash me-2"></i> Pas d'équipe
        </div>

        <div class="row g-2">
            <div class="col-6">
                <div class="home-btn" onclick="app.nav('dashboard', 'nav-dash')"><i class="fa-solid fa-list-check text-white"></i><h3>PHASES</h3></div>
            </div>
            <div class="col-6">
                <div class="home-btn" onclick="app.nav('rules', 'nav-dash')"><i class="fa-solid fa-file-contract text-warning"></i><h3>RÈGLES</h3></div>
            </div>
            <div class="col-6">
                <div class="home-btn" onclick="app.nav('games', 'nav-games')"><i class="fa-solid fa-gamepad text-success"></i><h3>ARCADE</h3></div>
            </div>
            <div class="col-6">
                <div class="home-btn" onclick="app.nav('journal', 'nav-journal')"><i class="fa-solid fa-book-open text-info"></i><h3>JOURNAL</h3></div>
            </div>
            <div class="col-12">
                <div class="home-btn flex-row gap-3 py-3" style="min-height: auto;" onclick="app.nav('oscars', 'nav-oscars')">
                    <i class="fa-solid fa-award text-accent mb-0"></i><h3 class="mb-0">VOTE</h3>
                </div>
            </div>
        </div>
    </section>

    <section id="view-dashboard" class="view">
        <h4 class="fw-bold mb-3">PROGRESSION</h4>
        <div class="solid-panel d-flex justify-content-center position-relative mb-4" style="height: 150px;">
            <canvas id="progressChart"></canvas>
            <div class="position-absolute top-50 start-50 translate-middle text-center">
                <h2 id="percent-text" class="m-0 fw-bold">0%</h2>
            </div>
        </div>
        <div id="missions-list"></div>
    </section>

    <section id="view-debate" class="view">
        <div class="text-center mt-4 mb-3">
            <h2 style="font-family: var(--font-head);">ZONE DE DÉBAT</h2>
            <p class="text-secondary small">PHASE 2: ÉQUIPES INCLUSIVES</p>
        </div>
        
        <div class="radar-container mb-3">
            <canvas id="radarChart"></canvas>
        </div>
        <p class="text-center text-white-50 small mb-3">Est-ce que votre équipe couvre tous les points ?</p>

        <div class="solid-panel">
            <h6 class="fw-bold mb-3"><i class="fa-solid fa-users text-info"></i> L'ÉQUIPE</h6>
            <input type="text" id="team-name-create" class="solid-input mb-3" placeholder="NOM DE L'ÉQUIPE">
            
            <div class="p-3 border rounded mb-3" style="border-color: #444 !important;">
                <label class="small text-secondary mb-2">VALIDATION (ODD 5 & 10)</label>
                <button id="check-mixed" class="btn-outline" onclick="this.classList.toggle('active')"><i class="fa-regular fa-square"></i> Équipe Mixte</button>
                <button id="check-skills" class="btn-outline" onclick="this.classList.toggle('active')"><i class="fa-regular fa-square"></i> Compétences Variées</button>
                <button id="check-class" class="btn-outline" onclick="this.classList.toggle('active')"><i class="fa-regular fa-square"></i> Validé par la classe</button>
            </div>
            <button onclick="app.finalizeTeam()" class="btn-solid">CONFIRMER L'ÉQUIPE</button>
        </div>
        <button onclick="app.nav('dashboard')" class="btn btn-link text-secondary w-100">Retour</button>
    </section>

    <section id="view-rules" class="view">
        <h4 class="fw-bold mb-3">RÈGLEMENT DU JEU</h4>
        
        <div class="parchment mb-4">
            <h4 class="text-center">PACTE DE FAIR-PLAY</h4>
            <p class="small">Nous, les élèves du Lycée Olympique, nous engageons à :</p>
            <ul class="small ps-3">
                <li>Respecter les adversaires (ODD 16).</li>
                <li>Accepter la défaite avec dignité.</li>
                <li>Jouer sans tricher.</li>
                <li>Encourager tous les participants.</li>
            </ul>
            <div class="text-center mt-4">
                <strong>Signature :</strong>
                <div class="signature-pad" id="sign-pad" onclick="app.signPact(this)"></div>
            </div>
        </div>
        
        <div id="rules-lock-msg" class="text-center text-secondary small">Signez pour valider la Phase 4</div>
    </section>

    <section id="view-journal" class="view">
        <h4 class="fw-bold mb-3">JOURNAL DE BORD</h4>
        <div class="solid-panel">
            <label class="small text-secondary mb-2">MOOD</label>
            <div class="d-flex justify-content-between mb-3">
                <div class="mood-btn" onclick="app.selectMood(this, '🤩')">🤩</div>
                <div class="mood-btn" onclick="app.selectMood(this, '🙂')">🙂</div>
                <div class="mood-btn" onclick="app.selectMood(this, '😐')">😐</div>
                <div class="mood-btn" onclick="app.selectMood(this, '🥱')">🥱</div>
            </div>
            <input type="hidden" id="selected-mood">
            <textarea id="journal-text" class="solid-textarea mt-2" rows="2" placeholder="Réflexion..."></textarea>
            <label class="small text-secondary mb-2 mt-2">PHOTO</label>
            <input type="file" id="journal-photo" class="form-control bg-dark text-white border-secondary mb-3" accept="image/*">
            <button onclick="app.saveJournal()" class="btn-solid">POSTER</button>
        </div>
        <div id="journal-feed" class="mt-4"></div>
    </section>

    <section id="view-games" class="view">
        <h4 class="fw-bold mb-3">SALLE D'ARCADE</h4>
        <div id="game-menu">
            <div class="solid-panel p-3 mb-2" onclick="app.startGame('num')"><h6 class="mb-0 text-white fw-bold"><i class="fa-solid fa-calculator text-primary me-2"></i> Les Nombres</h6></div>
            <div class="solid-panel p-3 mb-2" onclick="app.startGame('fut')"><h6 class="mb-0 text-white fw-bold"><i class="fa-solid fa-rocket text-warning me-2"></i> Futur Simple</h6></div>
            <div class="solid-panel p-3 mb-2" onclick="app.startGame('part')"><h6 class="mb-0 text-white fw-bold"><i class="fa-solid fa-pizza-slice text-danger me-2"></i> Partitifs</h6></div>
        </div>
        <div id="game-interface" style="display:none;">
            <div class="solid-panel">
                <h5 id="game-question" class="fw-bold mb-4 text-center">...</h5>
                <div id="game-options"></div>
            </div>
            <button onclick="app.exitGame()" class="btn btn-outline text-white w-100">Quitter</button>
        </div>
    </section>

    <section id="view-oscars" class="view">
        <h2 class="text-center fw-bold mb-4">VOTEZ !</h2>
        <div id="oscars-menu">
            <div class="solid-panel text-center mb-3" onclick="app.showNominees('ling')"><h6 class="mb-1 text-white">Francophones d'Or</h6><small id="status-ling" class="text-secondary">Non voté</small></div>
            <div class="solid-panel text-center mb-3" onclick="app.showNominees('soc')"><h6 class="mb-1 text-white">Esprit d'Équipe</h6><small id="status-soc" class="text-secondary">Non voté</small></div>
        </div>
        <div id="oscars-voting" style="display:none;">
            <h5 id="voting-cat-title" class="fw-bold mb-3 text-warning text-center">...</h5>
            <div id="nominees-list"></div>
            <button onclick="app.exitVoting()" class="btn btn-link text-white w-100 mt-3">Retour</button>
        </div>
    </section>

    <div id="app-dock" class="dock-nav" style="display:none;">
        <div id="nav-home" class="dock-item active" onclick="app.nav('home', this)"><i class="fa-solid fa-house"></i></div>
        <div id="nav-dash" class="dock-item" onclick="app.nav('dashboard', this)"><i class="fa-solid fa-list-check"></i></div>
        <div id="nav-games" class="dock-item" onclick="app.nav('games', this)"><i class="fa-solid fa-gamepad"></i></div>
        <div id="nav-journal" class="dock-item" onclick="app.nav('journal', this)"><i class="fa-solid fa-book-open"></i></div>
        <div id="nav-oscars" class="dock-item" onclick="app.nav('oscars', this)"><i class="fa-solid fa-award"></i></div>
    </div>

    <div id="customModal" class="custom-modal">
        <div class="modal-content-solid">
            <h4 id="modal-title" class="fw-bold mb-2">...</h4>
            <div class="badge bg-warning text-dark mb-2" id="modal-odd">ODD</div>
            <p id="modal-desc" class="text-secondary small mb-4">...</p>
            <input type="text" id="user-input" class="solid-input text-uppercase" placeholder="CODE PROF">
            <button onclick="app.validate()" class="btn-solid mb-2">VALIDER</button>
            <button onclick="app.closeModal()" class="btn btn-link text-secondary text-decoration-none">Fermer</button>
            <div id="feedback-msg" class="mt-3 small fw-bold"></div>
        </div>
    </div>

    <script>
        const SPRITES = ["fa-dragon", "fa-ghost", "fa-robot", "fa-cat", "fa-bolt", "fa-fire", "fa-snowflake", "fa-leaf"];
        const TRAITS = ["Fort", "Rapide", "Stratège", "Sociable", "Créatif"];

        const DATA = {
            user: { sprite: "", name: "", trait: "" },
            teamName: "",
            missions: [
                { id: 1, type: "code", code: "MONNAIE", title: "L'Argent Solidaire", odd: "ODD 1 & 12", icon: "fa-coins", desc: "Sept-Oct: Création monnaie.", completed: false },
                { id: 2, type: "team", title: "Équipes Inclusives", odd: "ODD 5 & 10", icon: "fa-users", desc: "Nov-Dec: Création équipes.", completed: false },
                { id: 3, type: "code", code: "ECO", title: "Obstacles Avenir", odd: "ODD 13", icon: "fa-recycle", desc: "Jan-Fév: Design épreuves.", completed: false },
                { id: 4, type: "rules", title: "Règlement", odd: "ODD 16", icon: "fa-scale-balanced", desc: "Fév-Mars: Fair-play.", completed: false },
                { id: 5, type: "code", code: "FOOD", title: "Ravitaillement", odd: "ODD 3", icon: "fa-apple-whole", desc: "Avril-Mai: Snacks sains.", completed: false },
                { id: 6, type: "code", code: "MAP", title: "Plan Parcours", odd: "ODD 11", icon: "fa-map", desc: "Mai-Juin: Tracé plan.", completed: false }
            ],
            journal: [],
            votes: { ling: false, soc: false },
            nominees: ["Les Titans", "Eco-Warriors", "Cyber-Français"],
            currentId: null
        };

        const QUIZ = {
            num: [{ q: "10 stylos = 20€. 1 stylo = ?", a: ["2€", "5€", "1€"], c: 0 }],
            fut: [{ q: "Demain je ___ (manger)", a: ["mangerai", "mangerais", "mange"], c: 0 }],
            part: [{ q: "Je veux ___ eau", a: ["de l'", "du", "de la"], c: 0 }]
        };
        let currentQuiz = [], qIndex = 0, score = 0;
        let chart = null, radarChart = null;

        const app = {
            init: () => {
                const grid = document.getElementById('sprite-container');
                SPRITES.forEach(icon => {
                    const div = document.createElement('div'); div.className = "avatar-item"; div.innerHTML = `<i class="fa-solid ${icon}"></i>`;
                    div.onclick = () => { document.querySelectorAll('.avatar-item').forEach(el => el.classList.remove('selected')); div.classList.add('selected'); DATA.user.sprite = icon; };
                    grid.appendChild(div);
                });
                const tCont = document.getElementById('trait-container');
                TRAITS.forEach(t => {
                    const span = document.createElement('span'); span.className = "trait-tag"; span.innerText = t;
                    span.onclick = () => { document.querySelectorAll('.trait-tag').forEach(el => el.classList.remove('selected')); span.classList.add('selected'); DATA.user.trait = t; document.getElementById('selected-trait').value = t; };
                    tCont.appendChild(span);
                });
            },

            saveProfile: () => {
                const name = document.getElementById('player-name').value;
                if(!DATA.user.sprite || !name || !DATA.user.trait) return alert("Complétez votre profil !");
                DATA.user.name = name;
                document.getElementById('mini-avatar').innerHTML = `<i class="fa-solid ${DATA.user.sprite}"></i>`;
                app.showView('view-home');
                document.getElementById('app-dock').style.display = 'flex';
            },

            nav: (viewName, el) => {
                document.querySelectorAll('.dock-item').forEach(i => i.classList.remove('active'));
                if(el) { if(typeof el === 'string') document.getElementById(el).classList.add('active'); else el.classList.add('active'); }
                app.showView('view-' + viewName);
                if(viewName === 'dashboard') { app.renderList(); setTimeout(app.initChart, 100); }
                if(viewName === 'journal') app.renderJournal();
            },

            showView: (id) => {
                document.querySelectorAll('.view').forEach(v => v.classList.remove('active-view'));
                document.getElementById(id).classList.add('active-view');
            },

            // --- FASES ---
            renderList: () => {
                const list = document.getElementById('missions-list'); list.innerHTML = "";
                DATA.missions.forEach(m => {
                    const status = m.completed ? 'completed' : '';
                    const locked = (!m.completed && m.id > 1 && !DATA.missions[m.id-2].completed) ? 'locked' : '';
                    const iconCheck = m.completed ? 'fa-check text-success' : (locked ? 'fa-lock text-secondary' : 'fa-play text-white');
                    
                    let action = `app.openModal(${m.id})`;
                    if (m.id === 2 && !locked) action = `app.goToDebate()`;
                    if (m.id === 4 && !locked) action = `app.nav('rules')`; // Fase Reglamento va a la firma

                    list.innerHTML += `<div class="solid-panel phase-card d-flex align-items-center ${status} ${locked}" onclick="${action}"><div class="me-3 text-center" style="width: 40px;"><i class="fa-solid ${m.icon} fa-xl text-secondary"></i></div><div class="flex-grow-1"><span class="odd-badge">${m.odd}</span><h6 class="mb-0 fw-bold text-white">${m.title}</h6></div><i class="fa-solid ${iconCheck}"></i></div>`;
                });
            },

            // --- FASE 2: DEBATE & RADAR ---
            goToDebate: () => {
                if(DATA.missions[1].completed) return;
                app.showView('view-debate');
                setTimeout(app.initRadar, 200);
            },
            initRadar: () => {
                if(radarChart) radarChart.destroy();
                const ctx = document.getElementById('radarChart').getContext('2d');
                // Simulamos datos de equipo (aleatorio para demo)
                const teamData = [Math.random()*10, Math.random()*10, Math.random()*10, Math.random()*10, Math.random()*10];
                
                radarChart = new Chart(ctx, {
                    type: 'radar',
                    data: {
                        labels: TRAITS,
                        datasets: [{
                            label: 'Équilibre Équipe',
                            data: teamData,
                            backgroundColor: 'rgba(77, 121, 255, 0.4)',
                            borderColor: '#4D79FF',
                            pointBackgroundColor: '#fff'
                        }]
                    },
                    options: {
                        scales: { r: { grid: { color: '#444' }, angleLines: { color: '#444' }, suggesteMin: 0, suggestedMax: 10, ticks: { display: false } } },
                        plugins: { legend: { display: false } }
                    }
                });
            },
            finalizeTeam: () => {
                const team = document.getElementById('team-name-create').value;
                if(!team) return alert("Nom ?");
                if(!document.getElementById('check-class').classList.contains('active')) return alert("Validez !");
                DATA.teamName = team;
                DATA.missions[1].completed = true;
                DATA.nominees.push(team);
                document.getElementById('home-team-badge').innerText = "Équipe: " + team;
                document.getElementById('home-team-badge').classList.replace('bg-secondary', 'bg-success');
                confetti();
                app.nav('dashboard');
            },

            // --- FASE 4: FIRMA REGLAS ---
            signPact: (el) => {
                el.innerHTML = "<i>Signé : " + DATA.user.name + "</i>";
                el.classList.add("signed");
                el.style.fontFamily = "var(--font-hand)";
                DATA.missions[3].completed = true;
                confetti();
                setTimeout(() => { app.nav('dashboard'); }, 1500);
            },

            // --- MODAL CÓDIGOS ---
            openModal: (id) => {
                DATA.currentId = id; const m = DATA.missions.find(x => x.id === id); if(m.completed) return;
                document.getElementById('modal-title').innerText = m.title; document.getElementById('modal-desc').innerText = m.desc; document.getElementById('modal-odd').innerText = m.odd;
                document.getElementById('user-input').value = ""; document.getElementById('feedback-msg').innerText = ""; document.getElementById('customModal').classList.add('show');
            },
            closeModal: () => document.getElementById('customModal').classList.remove('show'),
            validate: () => {
                const inp = document.getElementById('user-input').value.trim().toUpperCase();
                const m = DATA.missions.find(x => x.id === DATA.currentId);
                if(inp === m.code) {
                    m.completed = true; document.getElementById('feedback-msg').innerText = "Validé !"; document.getElementById('feedback-msg').style.color = "#28a745"; confetti();
                    setTimeout(() => { app.closeModal(); app.renderList(); app.initChart(); }, 1000);
                } else { document.getElementById('feedback-msg').innerText = "Incorrect"; document.getElementById('feedback-msg').style.color = "#dc3545"; }
            },

            // --- JUEGOS, JOURNAL & VOTES (Resumido igual que antes) ---
            startGame: (t) => { currentQuiz = QUIZ[t]; qIndex=0; score=0; document.getElementById('game-menu').style.display='none'; document.getElementById('game-interface').style.display='block'; app.renderQuestion(); },
            renderQuestion: () => { if(qIndex>=currentQuiz.length){ alert("Fin!"); app.exitGame(); return;} const q=currentQuiz[qIndex]; document.getElementById('game-question').innerText=q.q; const o=document.getElementById('game-options'); o.innerHTML=""; q.a.forEach((ans,i)=>{ o.innerHTML+=`<div class='solid-panel p-2 text-center' style='cursor:pointer' onclick='app.checkAnswer(${i})'>${ans}</div>`}); },
            checkAnswer: (i) => { if(i===currentQuiz[qIndex].c){score+=10; confetti();} setTimeout(()=>{qIndex++; app.renderQuestion()},500); },
            exitGame: () => { document.getElementById('game-interface').style.display='none'; document.getElementById('game-menu').style.display='block'; },
            
            selectMood: (e,m) => { document.querySelectorAll('.mood-btn').forEach(b=>b.classList.remove('selected')); e.classList.add('selected'); document.getElementById('selected-mood').value=m; },
            saveJournal: () => {
                const m=document.getElementById('selected-mood').value, t=document.getElementById('journal-text').value, f=document.getElementById('journal-photo');
                if(!m||!t) return alert("Remplissez !");
                const entry={d:new Date().toLocaleDateString(), m, t, i:null};
                if(f.files[0]){ const r=new FileReader(); r.onload=(e)=>{entry.i=e.target.result; DATA.journal.unshift(entry); app.renderJournal();}; r.readAsDataURL(f.files[0]); }
                else { DATA.journal.unshift(entry); app.renderJournal(); }
                document.getElementById('journal-text').value=""; confetti();
            },
            renderJournal: () => { const c=document.getElementById('journal-feed'); c.innerHTML=""; DATA.journal.forEach(e=>{ c.innerHTML+=`<div class='solid-panel journal-entry'><div class='d-flex justify-content-between'><span>${e.d}</span><span>${e.m}</span></div><p class='text-white'>${e.t}</p>${e.i?`<img src='${e.i}' class='journal-img'>`:''}</div>`}); },

            showNominees: (c) => { if(DATA.votes[c]) return alert("Déjà voté!"); document.getElementById('oscars-menu').style.display='none'; document.getElementById('oscars-voting').style.display='block'; const l=document.getElementById('nominees-list'); l.innerHTML=""; DATA.nominees.forEach(t=>{ if(t!==DATA.teamName) l.innerHTML+=`<div class='solid-panel p-2 mb-2 d-flex justify-content-between'><span class='text-white'>${t}</span><button class='btn btn-sm btn-outline-warning' onclick='app.submitVote("${c}","${t}")'>VOTE</button></div>` }); },
            submitVote: (c,t) => { if(confirm("Sûr?")){ DATA.votes[c]=true; app.exitVoting(); confetti(); } },
            exitVoting: () => { document.getElementById('oscars-voting').style.display='none'; document.getElementById('oscars-menu').style.display='block'; },

            // --- CHARTS ---
            initChart: () => {
                if(chart) chart.destroy();
                const ctx = document.getElementById('progressChart').getContext('2d');
                chart = new Chart(ctx, { type: 'doughnut', data: { datasets: [{ data: [0, 6], backgroundColor: ['#4D79FF', '#333'], borderWidth: 0 }] }, options: { responsive: true, maintainAspectRatio: false, cutout: '80%', events: [] } });
                app.updateChart();
            },
            updateChart: () => {
                if(!chart) return;
                const c = DATA.missions.filter(m => m.completed).length;
                chart.data.datasets[0].data = [c, 6-c];
                chart.update();
                document.getElementById('percent-text').innerText = Math.round((c/6)*100) + "%";
            }
        };
        app.init();
    </script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=True)
