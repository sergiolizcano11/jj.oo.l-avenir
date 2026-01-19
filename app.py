import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="J.O. De l'Avenir",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🏅"
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

        /* --- UI COMPONENTES --- */
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
            margin-top: 10px; cursor: pointer;
        }
        .btn-solid:active { background-color: #3a5bbf; transform: scale(0.98); }

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

        /* --- AVATAR GRID --- */
        .avatar-grid {
            display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 20px;
        }
        .avatar-item {
            background: #2C2C2C; border: 2px solid #444; border-radius: 10px;
            padding: 10px; text-align: center; cursor: pointer; transition: all 0.2s;
        }
        .avatar-item.selected {
            background: rgba(77, 121, 255, 0.2); border-color: var(--primary);
            box-shadow: 0 0 10px var(--primary);
        }
        .avatar-item i { font-size: 1.5rem; color: #fff; }

        .trait-selector { display: flex; gap: 5px; overflow-x: auto; padding-bottom: 10px; }
        .trait-tag {
            background: #333; padding: 5px 15px; border-radius: 20px;
            white-space: nowrap; cursor: pointer; border: 1px solid #444; font-size: 0.85rem;
        }
        .trait-tag.selected { background: var(--accent); color: black; font-weight: bold; }

        /* --- HOME GRID --- */
        .home-btn {
            background-color: var(--card-bg); border: 1px solid #444;
            border-radius: 15px; padding: 20px 10px; text-align: center;
            cursor: pointer; height: 100%; display: flex; flex-direction: column;
            justify-content: center; align-items: center;
        }
        .home-btn i { font-size: 1.8rem; margin-bottom: 8px; }
        .home-btn h3 { font-size: 0.8rem; margin: 0; font-weight: 700; text-transform: uppercase; }

        /* --- JOURNAL --- */
        .mood-btn {
            font-size: 2rem; background: #2C2C2C; border: 1px solid #444;
            border-radius: 10px; padding: 10px; cursor: pointer; transition: 0.2s; flex: 1; text-align: center; margin: 0 2px;
        }
        .mood-btn.selected { background: var(--primary); border-color: var(--primary); transform: scale(1.1); }
        .journal-entry { border-left: 3px solid var(--accent); position: relative; }
        .journal-img { width: 100%; border-radius: 8px; margin-top: 10px; border: 1px solid #444; }

        /* --- GAMES & VOTES --- */
        .game-opt {
            background: #333; padding: 15px; margin-bottom: 10px; border-radius: 8px; 
            cursor: pointer; border: 2px solid transparent; text-align: center; font-weight: bold;
        }
        .game-opt.correct { border-color: var(--success); background: rgba(40, 167, 69, 0.2); }
        .game-opt.wrong { border-color: #dc3545; background: rgba(220, 53, 69, 0.2); }

        .vote-card {
            background: #252525; padding: 15px; border-radius: 8px; margin-bottom: 10px; 
            display: flex; justify-content: space-between; align-items: center; border: 1px solid #444;
        }

        /* --- VISTAS --- */
        .view { display: none; padding: 20px; min-height: 100vh; }
        .active-view { display: block; animation: fadeIn 0.4s; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        /* --- DOCK --- */
        .dock-nav {
            position: fixed; bottom: 0; left: 0; width: 100%;
            background-color: #1E1E1E; border-top: 1px solid #333;
            display: flex; justify-content: space-around;
            padding: 15px 0; z-index: 1000;
        }
        .dock-item { font-size: 1.4rem; color: #666; cursor: pointer; position: relative; }
        .dock-item.active { color: var(--primary); transform: translateY(-5px); }
        .dock-item.active::after {
            content: ''; position: absolute; bottom: -5px; left: 50%; transform: translateX(-50%);
            width: 4px; height: 4px; background: var(--primary); border-radius: 50%;
        }

        /* --- FASES --- */
        .phase-card { cursor: pointer; border-left: 4px solid #555; background: #252525; padding: 15px; margin-bottom: 10px; border-radius: 8px;}
        .phase-card.completed { border-left-color: var(--success); }
        .odd-badge { font-size: 0.65rem; background: #333; padding: 2px 6px; border-radius: 4px; color: var(--accent); font-weight: bold; margin-bottom: 4px; display: inline-block; }

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

    <section id="view-avatar" class="view active-view">
        <div class="text-center mt-4 mb-4">
            <h2 style="font-family: var(--font-head);">CRÉEZ VOTRE PROFIL</h2>
            <p class="text-secondary small">CHOISISSEZ VOTRE CHAMPION</p>
        </div>
        <div class="avatar-grid" id="sprite-container"></div>
        <div class="solid-panel mt-4">
            <label class="small text-secondary mb-2 d-block text-start">VOTRE NOM</label>
            <input type="text" id="player-name" class="solid-input" placeholder="Pseudo...">
            <label class="small text-secondary mb-2 d-block text-start mt-3">VOTRE SUPER-POUVOIR</label>
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
            <i class="fa-solid fa-users-slash me-2"></i> Pas d'équipe
        </div>

        <div class="row g-3">
            <div class="col-6">
                <div class="home-btn" onclick="app.nav('dashboard', 'nav-dash')">
                    <i class="fa-solid fa-list-check text-white"></i>
                    <h3>PHASES</h3>
                </div>
            </div>
            <div class="col-6">
                <div class="home-btn" onclick="app.nav('games', 'nav-games')">
                    <i class="fa-solid fa-gamepad text-success"></i>
                    <h3>ARCADE</h3>
                </div>
            </div>
            <div class="col-6">
                <div class="home-btn" onclick="app.nav('journal', 'nav-journal')">
                    <i class="fa-solid fa-book-open text-info"></i>
                    <h3>JOURNAL</h3>
                </div>
            </div>
            <div class="col-6">
                <div class="home-btn" onclick="app.nav('oscars', 'nav-oscars')">
                    <i class="fa-solid fa-award text-warning"></i>
                    <h3>VOTE</h3>
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

    <section id="view-journal" class="view">
        <h4 class="fw-bold mb-3" style="font-family: var(--font-head);">JOURNAL DE BORD</h4>
        <div class="solid-panel">
            <label class="small text-secondary mb-2">MOOD</label>
            <div class="d-flex justify-content-between mb-3">
                <div class="mood-btn" onclick="app.selectMood(this, '🤩')">🤩</div>
                <div class="mood-btn" onclick="app.selectMood(this, '🙂')">🙂</div>
                <div class="mood-btn" onclick="app.selectMood(this, '😐')">😐</div>
                <div class="mood-btn" onclick="app.selectMood(this, '🥱')">🥱</div>
            </div>
            <input type="hidden" id="selected-mood">
            
            <label class="small text-secondary mb-2 mt-2">RÉFLEXION</label>
            <textarea id="journal-text" class="solid-textarea" rows="2" placeholder="J'ai appris..."></textarea>
            
            <label class="small text-secondary mb-2 mt-2">PHOTO (OPTIONNEL)</label>
            <input type="file" id="journal-photo" class="form-control bg-dark text-white border-secondary mb-3" accept="image/*">
            
            <button onclick="app.saveJournal()" class="btn-solid">POSTER</button>
        </div>
        <div id="journal-feed" class="mt-4"></div>
    </section>

    <section id="view-games" class="view">
        <h4 class="fw-bold mb-3" style="font-family: var(--font-head);">SALLE D'ARCADE</h4>
        
        <div id="game-menu">
            <div class="solid-panel game-opt" onclick="app.startGame('num')">
                <h6 class="mb-0 text-white"><i class="fa-solid fa-calculator text-primary me-2"></i> Les Nombres</h6>
            </div>
            <div class="solid-panel game-opt" onclick="app.startGame('fut')">
                <h6 class="mb-0 text-white"><i class="fa-solid fa-rocket text-warning me-2"></i> Futur Simple</h6>
            </div>
            <div class="solid-panel game-opt" onclick="app.startGame('part')">
                <h6 class="mb-0 text-white"><i class="fa-solid fa-pizza-slice text-danger me-2"></i> Les Partitifs</h6>
            </div>
        </div>

        <div id="game-interface" style="display:none;">
            <div class="solid-panel">
                <div class="d-flex justify-content-between mb-3">
                    <span class="badge bg-secondary">Quiz</span>
                    <span class="text-white fw-bold" id="game-score">Score: 0</span>
                </div>
                <h5 id="game-question" class="fw-bold mb-4 text-center">...</h5>
                <div id="game-options"></div>
            </div>
            <button onclick="app.exitGame()" class="btn btn-outline text-white w-100">Quitter</button>
        </div>
    </section>

    <section id="view-oscars" class="view">
        <h2 class="text-center fw-bold mb-4">VOTEZ !</h2>
        <p class="text-center small text-secondary mb-4">1 vote par catégorie (Irréversible)</p>
        
        <div id="oscars-menu">
            <div class="solid-panel text-center mb-3" onclick="app.showNominees('ling')" style="cursor:pointer">
                <i class="fa-solid fa-comments text-warning fa-2x mb-2"></i>
                <h6 class="mb-1">Francophones d'Or</h6>
                <small id="status-ling" class="text-secondary">Non voté</small>
            </div>
            <div class="solid-panel text-center mb-3" onclick="app.showNominees('soc')" style="cursor:pointer">
                <i class="fa-solid fa-users text-warning fa-2x mb-2"></i>
                <h6 class="mb-1">Esprit d'Équipe</h6>
                <small id="status-soc" class="text-secondary">Non voté</small>
            </div>
            <div class="solid-panel text-center mb-3" onclick="app.showNominees('inno')" style="cursor:pointer">
                <i class="fa-solid fa-lightbulb text-warning fa-2x mb-2"></i>
                <h6 class="mb-1">Les Innovateurs</h6>
                <small id="status-inno" class="text-secondary">Non voté</small>
            </div>
        </div>

        <div id="oscars-voting" style="display:none;">
            <h5 id="voting-cat-title" class="fw-bold mb-3 text-warning text-center">...</h5>
            <div id="nominees-list"></div>
            <button onclick="app.exitVoting()" class="btn btn-link text-white w-100 mt-3">Retour</button>
        </div>
    </section>

    <section id="view-debate" class="view">
        <div class="text-center mt-4 mb-4">
            <h2 style="font-family: var(--font-head);">CRÉATION D'ÉQUIPE</h2>
        </div>
        <div class="solid-panel d-flex align-items-center bg-black border-primary">
            <div id="debate-avatar" class="me-3 text-center" style="font-size: 2rem; width: 50px;"></div>
            <div>
                <h5 id="debate-name" class="mb-0 fw-bold text-white">Nom</h5>
                <small id="debate-trait" class="badge bg-warning text-dark">Trait</small>
            </div>
        </div>
        <div class="solid-panel">
            <h6 class="fw-bold mb-3">L'ÉQUIPE</h6>
            <input type="text" id="team-name-create" class="solid-input mb-3" placeholder="NOM DE L'ÉQUIPE">
            <div class="p-3 border rounded mb-3" style="border-color: #444 !important;">
                <label class="small text-secondary mb-2">AUTO-VALIDATION</label>
                <button id="check-mixed" class="btn-outline" onclick="this.classList.toggle('active')"><i class="fa-regular fa-square"></i> Équipe Mixte</button>
                <button id="check-skills" class="btn-outline" onclick="this.classList.toggle('active')"><i class="fa-regular fa-square"></i> Compétences</button>
                <button id="check-class" class="btn-outline" onclick="this.classList.toggle('active')"><i class="fa-regular fa-square"></i> Validé par la classe</button>
            </div>
            <button onclick="app.finalizeTeam()" class="btn-solid">CONFIRMER</button>
        </div>
        <button onclick="app.nav('dashboard')" class="btn btn-link text-secondary w-100">Retour</button>
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
            <input type="text" id="user-input" class="solid-input text-uppercase" placeholder="CODE PROFESSEUR">
            <button onclick="app.validate()" class="btn-solid mb-2">VALIDER</button>
            <button onclick="app.closeModal()" class="btn btn-link text-secondary text-decoration-none">Fermer</button>
            <div id="feedback-msg" class="mt-3 small fw-bold"></div>
        </div>
    </div>

    <script>
        const SPRITES = ["fa-dragon", "fa-ghost", "fa-robot", "fa-cat", "fa-bolt", "fa-fire", "fa-snowflake", "fa-leaf"];
        const TRAITS = ["Fort", "Rapide", "Intelligent", "Sociable", "Créatif"];

        const DATA = {
            user: { sprite: "", name: "", trait: "" },
            teamName: "",
            missions: [
                { id: 1, type: "code", code: "MONNAIE", title: "L'Argent Solidaire", odd: "ODD 1 & 12", icon: "fa-coins", desc: "Sept-Oct: Création monnaie.", completed: false },
                { id: 2, type: "team", title: "Équipes Inclusives", odd: "ODD 5 & 10", icon: "fa-users", desc: "Nov-Dec: Création équipes.", completed: false },
                { id: 3, type: "code", code: "ECO", title: "Obstacles Avenir", odd: "ODD 13", icon: "fa-recycle", desc: "Jan-Fév: Design épreuves.", completed: false },
                { id: 4, type: "code", code: "RULES", title: "Règlement", odd: "ODD 16", icon: "fa-scale-balanced", desc: "Fév-Mars: Fair-play.", completed: false },
                { id: 5, type: "code", code: "FOOD", title: "Ravitaillement", odd: "ODD 3", icon: "fa-apple-whole", desc: "Avril-Mai: Snacks sains.", completed: false },
                { id: 6, type: "code", code: "MAP", title: "Plan Parcours", odd: "ODD 11", icon: "fa-map", desc: "Mai-Juin: Tracé plan.", completed: false }
            ],
            journal: [],
            votes: { ling: false, soc: false, inno: false },
            nominees: ["Les Titans", "Eco-Warriors", "Cyber-Français", "Green Team", "Les Olympiens"],
            currentId: null,
            score: 0
        };

        const QUIZ = {
            num: [{ q: "10 stylos = 20€. 1 stylo = ?", a: ["2€", "5€", "1€"], c: 0 }, { q: "Quatre-vingt-dix-neuf", a: ["89", "99", "98"], c: 1 }],
            fut: [{ q: "Demain je ___ (manger)", a: ["mangerai", "mangerais", "mange"], c: 0 }, { q: "Ils ___ (être)", a: ["seront", "sont", "serons"], c: 0 }],
            part: [{ q: "Je veux ___ eau", a: ["de l'", "du", "de la"], c: 0 }, { q: "Il mange ___ pommes", a: ["des", "de la", "du"], c: 0 }]
        };
        let currentQuiz = [], qIndex = 0;

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

            // --- JUEGOS ---
            startGame: (type) => {
                currentQuiz = QUIZ[type]; qIndex = 0; DATA.score = 0;
                document.getElementById('game-menu').style.display = 'none';
                document.getElementById('game-interface').style.display = 'block';
                app.renderQuestion();
            },
            renderQuestion: () => {
                if(qIndex >= currentQuiz.length) { alert("Terminé! Score: " + DATA.score); app.exitGame(); return; }
                const q = currentQuiz[qIndex];
                document.getElementById('game-score').innerText = "Score: " + DATA.score;
                document.getElementById('game-question').innerText = q.q;
                const opts = document.getElementById('game-options'); opts.innerHTML = "";
                q.a.forEach((ans, idx) => { opts.innerHTML += `<div class="solid-panel game-opt" onclick="app.checkAnswer(${idx})">${ans}</div>`; });
            },
            checkAnswer: (idx) => {
                const correct = currentQuiz[qIndex].c;
                const opts = document.querySelectorAll('.game-opt');
                if(idx === correct) { opts[idx].classList.add('correct'); DATA.score += 10; confetti({ particleCount: 50, spread: 30, origin: { y: 0.6 } }); }
                else { opts[idx].classList.add('wrong'); }
                setTimeout(() => { qIndex++; app.renderQuestion(); }, 1000);
            },
            exitGame: () => { document.getElementById('game-interface').style.display = 'none'; document.getElementById('game-menu').style.display = 'block'; },

            // --- VOTES ---
            showNominees: (cat) => {
                if(DATA.votes[cat]) return alert("Déjà voté !");
                document.getElementById('oscars-menu').style.display = 'none';
                document.getElementById('oscars-voting').style.display = 'block';
                document.getElementById('voting-cat-title').innerText = "Votez pour " + cat;
                const list = document.getElementById('nominees-list'); list.innerHTML = "";
                DATA.nominees.forEach(team => {
                    if(team === DATA.teamName) return; 
                    list.innerHTML += `<div class="vote-card"><span class="text-white fw-bold">${team}</span><button class="btn btn-sm btn-outline-warning text-warning border-warning" onclick="app.submitVote('${cat}', '${team}')">VOTER</button></div>`;
                });
            },
            submitVote: (cat, team) => {
                if(confirm("Confirmer pour " + team + " ?")) {
                    DATA.votes[cat] = true;
                    document.getElementById('status-' + cat).innerText = "Voté ✅";
                    document.getElementById('status-' + cat).className = "text-success fw-bold";
                    app.exitVoting(); confetti();
                }
            },
            exitVoting: () => { document.getElementById('oscars-voting').style.display = 'none'; document.getElementById('oscars-menu').style.display = 'block'; },

            // --- JOURNAL ---
            selectMood: (el, mood) => {
                document.querySelectorAll('.mood-btn').forEach(b => b.classList.remove('selected'));
                el.classList.add('selected');
                document.getElementById('selected-mood').value = mood;
            },
            saveJournal: () => {
                const mood = document.getElementById('selected-mood').value;
                const text = document.getElementById('journal-text').value;
                const fileInput = document.getElementById('journal-photo');
                if(!mood || !text) return alert("Remplissez tout !");
                
                const entry = { date: new Date().toLocaleDateString(), mood, text, img: null };
                
                if(fileInput.files && fileInput.files[0]) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        entry.img = e.target.result;
                        DATA.journal.unshift(entry);
                        app.renderJournal();
                        confetti();
                    }
                    reader.readAsDataURL(fileInput.files[0]);
                } else {
                    DATA.journal.unshift(entry);
                    app.renderJournal();
                    confetti();
                }
                document.getElementById('journal-text').value = "";
                document.getElementById('selected-mood').value = "";
                document.querySelectorAll('.mood-btn').forEach(b => b.classList.remove('selected'));
                document.getElementById('journal-photo').value = "";
            },
            renderJournal: () => {
                const feed = document.getElementById('journal-feed'); feed.innerHTML = "";
                DATA.journal.forEach(e => {
                    let imgHtml = e.img ? `<img src="${e.img}" class="journal-img">` : '';
                    feed.innerHTML += `<div class="solid-panel journal-entry"><div class="d-flex justify-content-between mb-2"><span class="badge bg-secondary">${e.date}</span><span style="font-size: 1.2rem;">${e.mood}</span></div><p class="mb-0 text-white">${e.text}</p>${imgHtml}</div>`;
                });
            },

            // --- FASES ---
            renderList: () => {
                const list = document.getElementById('missions-list'); list.innerHTML = "";
                DATA.missions.forEach(m => {
                    const status = m.completed ? 'completed' : '';
                    const locked = (!m.completed && m.id > 1 && !DATA.missions[m.id-2].completed) ? 'locked' : '';
                    const iconCheck = m.completed ? 'fa-check text-success' : (locked ? 'fa-lock text-secondary' : 'fa-play text-white');
                    const action = (m.id === 2 && !locked) ? `app.goToDebate()` : `app.openModal(${m.id})`;
                    list.innerHTML += `<div class="solid-panel phase-card d-flex align-items-center ${status} ${locked}" onclick="${action}"><div class="me-3 text-center" style="width: 40px;"><i class="fa-solid ${m.icon} fa-xl text-secondary"></i></div><div class="flex-grow-1"><span class="odd-badge">${m.odd}</span><h6 class="mb-0 fw-bold text-white">${m.title}</h6></div><i class="fa-solid ${iconCheck}"></i></div>`;
                });
            },
            goToDebate: () => {
                if(DATA.missions[1].completed) return;
                document.getElementById('debate-avatar').innerHTML = `<i class="fa-solid ${DATA.user.sprite} text-white"></i>`;
                document.getElementById('debate-name').innerText = DATA.user.name;
                document.getElementById('debate-trait').innerText = DATA.user.trait;
                app.showView('view-debate');
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
