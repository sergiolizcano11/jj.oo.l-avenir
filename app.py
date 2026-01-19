import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="J.O. De l'Avenir",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🏅"
)

# Ocultar elementos nativos de Streamlit
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
            --danger: #dc3545;
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

        /* --- HOME GRID --- */
        .home-btn {
            background-color: var(--card-bg); border: 1px solid #444;
            border-radius: 15px; padding: 15px 10px; text-align: center;
            cursor: pointer; height: 100%; display: flex; flex-direction: column;
            justify-content: center; align-items: center; min-height: 110px;
        }
        .home-btn:active { transform: scale(0.95); background: #252525; }
        .home-btn i { font-size: 1.8rem; margin-bottom: 8px; }
        .home-btn h3 { font-size: 0.75rem; margin: 0; font-weight: 700; text-transform: uppercase; }

        /* --- IMPACTO GLOBAL (TERMÓMETRO) --- */
        .impact-container {
            background: #222; border-radius: 15px; padding: 15px; margin-bottom: 20px;
            border: 1px solid #444;
        }
        .progress-bar-bg {
            background: #444; height: 15px; border-radius: 10px; overflow: hidden; margin-top: 5px;
        }
        .progress-bar-fill {
            background: linear-gradient(90deg, var(--primary), var(--accent));
            height: 100%; width: 0%; transition: width 1s ease-out;
        }

        /* --- MAPA --- */
        .map-container {
            position: relative; width: 100%; height: 300px; background: #2b3e50;
            border-radius: 15px; overflow: hidden; border: 2px solid #444;
            background-image: radial-gradient(#3a4b5c 15%, transparent 16%), radial-gradient(#3a4b5c 15%, transparent 16%);
            background-size: 20px 20px;
        }
        .map-pin {
            position: absolute; width: 35px; height: 35px; background: var(--accent);
            border-radius: 50%; display: flex; align-items: center; justify-content: center;
            color: #000; font-weight: bold; cursor: pointer; border: 2px solid #fff;
            box-shadow: 0 4px 8px rgba(0,0,0,0.5); transform: translate(-50%, -50%);
            transition: transform 0.2s;
        }
        .map-pin:active { transform: translate(-50%, -50%) scale(1.2); }
        .map-pin.locked { background: #555; border-color: #777; color: #888; }

        /* --- INVENTARIO (ATELIER) --- */
        .inventory-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
        .inv-item {
            background: #2C2C2C; border: 1px solid #444; border-radius: 10px;
            padding: 10px; text-align: center; position: relative;
        }
        .inv-count {
            position: absolute; top: 5px; right: 5px; background: var(--primary);
            color: white; font-size: 0.7rem; padding: 2px 6px; border-radius: 10px;
        }

        /* --- MURO (WALL) --- */
        .wall-card {
            background: #1E1E1E; border-radius: 10px; overflow: hidden; margin-bottom: 15px;
            border: 1px solid #333;
        }
        .wall-img { width: 100%; height: 180px; object-fit: cover; background: #333; }
        .wall-footer { padding: 10px; display: flex; justify-content: space-between; align-items: center; }
        .like-btn { cursor: pointer; color: #666; transition: 0.2s; }
        .like-btn.liked { color: var(--danger); animation: pop 0.3s; }
        @keyframes pop { 50% { transform: scale(1.3); } }

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
        
        /* Helpers */
        .phase-card { cursor: pointer; border-left: 4px solid #555; background: #252525; padding: 15px; margin-bottom: 10px; border-radius: 8px;}
        .phase-card.completed { border-left-color: var(--success); }
        .odd-badge { font-size: 0.65rem; background: #333; padding: 2px 6px; border-radius: 4px; color: var(--accent); font-weight: bold; margin-bottom: 4px; display: inline-block; }
        .avatar-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 20px; }
        .avatar-item { background: #2C2C2C; border: 2px solid #444; border-radius: 10px; padding: 10px; text-align: center; cursor: pointer; }
        .avatar-item.selected { background: rgba(77, 121, 255, 0.2); border-color: var(--primary); }
        .trait-tag { background: #333; padding: 5px 15px; border-radius: 20px; white-space: nowrap; cursor: pointer; border: 1px solid #444; font-size: 0.85rem; }
        .trait-tag.selected { background: var(--accent); color: black; font-weight: bold; }
        .trait-selector { display: flex; gap: 5px; overflow-x: auto; padding-bottom: 10px; }
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
        
        <div class="impact-container">
            <div class="d-flex justify-content-between align-items-end">
                <h6 class="mb-0 fw-bold text-white"><i class="fa-solid fa-earth-americas text-success me-2"></i> IMPACT GLOBAL</h6>
                <small class="text-accent fw-bold">1250 / 5000 PTS</small>
            </div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" style="width: 25%;"></div>
            </div>
            <small class="text-secondary" style="font-size: 0.65rem;">Objectif commun de la classe (ODD 17)</small>
        </div>

        <div id="home-team-badge" class="badge bg-secondary mb-4 px-3 py-2 w-100" style="font-size: 0.9rem;">
            <i class="fa-solid fa-users-slash me-2"></i> Pas d'équipe (Voir Phase 2)
        </div>

        <div class="row g-2">
            <div class="col-6">
                <div class="home-btn" onclick="app.nav('dashboard', 'nav-dash')">
                    <i class="fa-solid fa-list-check text-white"></i>
                    <h3>PHASES</h3>
                </div>
            </div>
            <div class="col-6">
                <div class="home-btn" onclick="app.nav('journal', 'nav-journal')">
                    <i class="fa-solid fa-book-open text-info"></i>
                    <h3>JOURNAL</h3>
                </div>
            </div>
            <div class="col-6">
                <div class="home-btn" onclick="app.nav('map', 'nav-games')">
                    <i class="fa-solid fa-map-location-dot text-success"></i>
                    <h3>PLAN</h3>
                </div>
            </div>
            <div class="col-6">
                <div class="home-btn" onclick="app.nav('inventory', 'nav-games')">
                    <i class="fa-solid fa-recycle text-warning"></i>
                    <h3>ATELIER</h3>
                </div>
            </div>
            <div class="col-6">
                <div class="home-btn" onclick="app.nav('games', 'nav-games')">
                    <i class="fa-solid fa-gamepad text-primary"></i>
                    <h3>ARCADE</h3>
                </div>
            </div>
            <div class="col-6">
                <div class="home-btn" onclick="app.nav('wall', 'nav-journal')">
                    <i class="fa-solid fa-camera-retro text-danger"></i>
                    <h3>MUR</h3>
                </div>
            </div>
            <div class="col-12">
                <div class="home-btn flex-row gap-3 py-3" style="min-height: auto;" onclick="app.nav('oscars', 'nav-oscars')">
                    <i class="fa-solid fa-award text-accent mb-0"></i>
                    <h3 class="mb-0">VOTE & ÉVALUATION</h3>
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
            <textarea id="journal-text" class="solid-textarea mt-2" rows="2" placeholder="Réflexion..."></textarea>
            <button onclick="app.saveJournal()" class="btn-solid">POSTER</button>
        </div>
        <div id="journal-feed" class="mt-4"></div>
    </section>

    <section id="view-map" class="view">
        <h4 class="fw-bold mb-3" style="font-family: var(--font-head);">PLAN DU CAMPUS</h4>
        <p class="text-secondary small">Localisation des épreuves</p>
        
        <div class="map-container">
            <div class="map-pin" style="top: 20%; left: 20%;" onclick="alert('Gymnase: Zone Obstacles')">🏋️</div>
            <div class="map-pin" style="top: 50%; left: 50%;" onclick="alert('Cour: Grande Gymkhana')">🏁</div>
            <div class="map-pin" style="top: 80%; left: 30%;" onclick="alert('Cafétéria: Ravitaillement')">🍎</div>
            <div class="map-pin locked" style="top: 30%; left: 80%;">🔒</div>
        </div>
        <div class="solid-panel mt-3">
            <h6 class="text-white mb-2"><i class="fa-solid fa-location-dot text-danger"></i> Légende</h6>
            <ul class="list-unstyled text-secondary small mb-0">
                <li>🏋️ Zone Obstacles (Jan-Fév)</li>
                <li>🍎 Ravitaillement (Avril)</li>
                <li>🏁 Arrivée Finale (Juin)</li>
            </ul>
        </div>
    </section>

    <section id="view-inventory" class="view">
        <h4 class="fw-bold mb-3" style="font-family: var(--font-head);">ATELIER ÉCO</h4>
        <p class="text-secondary small">Matériaux recyclés collectés (ODD 13)</p>
        
        <div class="inventory-grid" id="inv-grid">
            </div>
        
        <button class="btn-solid mt-4" onclick="app.addInvItem()"><i class="fa-solid fa-plus"></i> AJOUTER MATÉRIEL</button>
    </section>

    <section id="view-wall" class="view">
        <h4 class="fw-bold mb-3" style="font-family: var(--font-head);">MUR DES CHAMPIONS</h4>
        <p class="text-secondary small">Les meilleures photos de la classe</p>
        
        <div id="wall-feed">
            </div>
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

    <section id="view-debate" class="view">
        <h2 class="text-center fw-bold mt-4">CRÉATION D'ÉQUIPE</h2>
        <div class="solid-panel">
            <input type="text" id="team-name-create" class="solid-input mb-3" placeholder="NOM DE L'ÉQUIPE">
            <button id="check-class" class="btn-outline mb-3 w-100" onclick="this.classList.toggle('active')">Validé par la classe</button>
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
            <p id="modal-desc" class="text-secondary small mb-4">...</p>
            <input type="text" id="user-input" class="solid-input text-uppercase" placeholder="CODE PROF">
            <button onclick="app.validate()" class="btn-solid mb-2">VALIDER</button>
            <button onclick="app.closeModal()" class="btn btn-link text-secondary text-decoration-none">Fermer</button>
            <div id="feedback-msg" class="mt-3 small fw-bold"></div>
        </div>
    </div>

    <script>
        const SPRITES = ["fa-dragon", "fa-ghost", "fa-robot", "fa-cat", "fa-bolt", "fa-fire", "fa-snowflake", "fa-leaf"];
        const TRAITS = ["Fort", "Rapide", "Intelligent", "Sociable", "Créatif"];
        
        // MOCK DATA INICIAL
        const DATA = {
            user: { sprite: "", name: "", trait: "" },
            teamName: "",
            missions: [
                { id: 1, type: "code", code: "MONNAIE", title: "L'Argent", odd: "ODD 1", icon: "fa-coins", desc: "Création monnaie.", completed: false },
                { id: 2, type: "team", title: "Équipes", odd: "ODD 5", icon: "fa-users", desc: "Création équipes.", completed: false },
                { id: 3, type: "code", code: "ECO", title: "Obstacles", odd: "ODD 13", icon: "fa-recycle", desc: "Design épreuves.", completed: false },
                { id: 4, type: "code", code: "RULES", title: "Règlement", odd: "ODD 16", icon: "fa-scale-balanced", desc: "Fair-play.", completed: false },
                { id: 5, type: "code", code: "FOOD", title: "Ravitaillement", odd: "ODD 3", icon: "fa-apple-whole", desc: "Snacks sains.", completed: false },
                { id: 6, type: "code", code: "MAP", title: "Plan", odd: "ODD 11", icon: "fa-map", desc: "Tracé plan.", completed: false }
            ],
            journal: [],
            inventory: [
                { icon: "fa-bottle-water", count: 12, name: "Bouteilles" },
                { icon: "fa-box-open", count: 5, name: "Cartons" },
                { icon: "fa-tire", count: 2, name: "Pneus" }
            ],
            wall: [
                { user: "Sophie", img: "https://via.placeholder.com/300x180/333/fff?text=Obstacle+Eco", likes: 12, liked: false },
                { user: "Team A", img: "https://via.placeholder.com/300x180/444/fff?text=Monnaie+Solidaire", likes: 8, liked: false }
            ],
            votes: { ling: false, soc: false },
            nominees: ["Les Titans", "Eco-Warriors", "Cyber-Français"],
            currentId: null,
            score: 0
        };

        const QUIZ = {
            num: [{ q: "10 stylos = 20€. 1 stylo = ?", a: ["2€", "5€", "1€"], c: 0 }],
            fut: [{ q: "Demain je ___ (manger)", a: ["mangerai", "mangerais", "mange"], c: 0 }],
            part: [{ q: "Je veux ___ eau", a: ["de l'", "du", "de la"], c: 0 }]
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
                // Renderizar Inventario y Muro al inicio (aunque ocultos)
                app.renderInventory();
                app.renderWall();
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

            // --- INVENTORY ---
            renderInventory: () => {
                const grid = document.getElementById('inv-grid'); grid.innerHTML = "";
                DATA.inventory.forEach(item => {
                    grid.innerHTML += `<div class="inv-item"><div class="inv-count">x${item.count}</div><i class="fa-solid ${item.icon} fa-2x text-white mb-2"></i><br><small class="text-secondary">${item.name}</small></div>`;
                });
            },
            addInvItem: () => {
                DATA.inventory[0].count++; // Simulación simple
                app.renderInventory();
                alert("Item ajouté ! (+1 Bouteille)");
            },

            // --- WALL ---
            renderWall: () => {
                const wall = document.getElementById('wall-feed'); wall.innerHTML = "";
                DATA.wall.forEach((post, idx) => {
                    const heartClass = post.liked ? 'fa-solid text-danger' : 'fa-regular';
                    wall.innerHTML += `<div class="wall-card"><img src="${post.img}" class="wall-img"><div class="wall-footer"><small class="text-white fw-bold">@${post.user}</small><div class="like-btn ${post.liked?'liked':''}" onclick="app.toggleLike(${idx})"><i class="${heartClass} fa-heart me-1"></i> ${post.likes}</div></div></div>`;
                });
            },
            toggleLike: (idx) => {
                const post = DATA.wall[idx];
                post.liked = !post.liked;
                post.likes += post.liked ? 1 : -1;
                app.renderWall();
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
                document.getElementById('game-question').innerText = q.q;
                const opts = document.getElementById('game-options'); opts.innerHTML = "";
                q.a.forEach((ans, idx) => { opts.innerHTML += `<div class="solid-panel p-2 mb-2 text-center" style="cursor:pointer;" onclick="app.checkAnswer(${idx})">${ans}</div>`; });
            },
            checkAnswer: (idx) => {
                const correct = currentQuiz[qIndex].c;
                if(idx === correct) { DATA.score += 10; confetti(); }
                setTimeout(() => { qIndex++; app.renderQuestion(); }, 500);
            },
            exitGame: () => { document.getElementById('game-interface').style.display = 'none'; document.getElementById('game-menu').style.display = 'block'; },

            // --- VOTES ---
            showNominees: (cat) => {
                if(DATA.votes[cat]) return alert("Déjà voté !");
                document.getElementById('oscars-menu').style.display = 'none';
                document.getElementById('oscars-voting').style.display = 'block';
                document.getElementById('voting-cat-title').innerText = "Vote pour " + cat;
                const list = document.getElementById('nominees-list'); list.innerHTML = "";
                DATA.nominees.forEach(team => {
                    if(team === DATA.teamName) return; 
                    list.innerHTML += `<div class="solid-panel p-2 mb-2 d-flex justify-content-between align-items-center"><span class="text-white fw-bold">${team}</span><button class="btn btn-sm btn-outline-warning" onclick="app.submitVote('${cat}', '${team}')">VOTER</button></div>`;
                });
            },
            submitVote: (cat, team) => {
                if(confirm("Confirmer pour " + team + " ?")) {
                    DATA.votes[cat] = true;
                    document.getElementById('status-' + cat).innerText = "Voté ✅";
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
                if(!mood || !text) return alert("Remplissez tout !");
                DATA.journal.unshift({ date: new Date().toLocaleDateString(), mood, text });
                document.getElementById('journal-text').value = "";
                app.renderJournal();
                confetti();
            },
            renderJournal: () => {
                const feed = document.getElementById('journal-feed'); feed.innerHTML = "";
                DATA.journal.forEach(e => {
                    feed.innerHTML += `<div class="solid-panel journal-entry"><div class="d-flex justify-content-between mb-2"><span class="badge bg-secondary">${e.date}</span><span style="font-size: 1.2rem;">${e.mood}</span></div><p class="mb-0 text-white">${e.text}</p></div>`;
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
