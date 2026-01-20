import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="J.O. De l'Avenir",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🏅"
)

# Ocultar elementos nativos
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
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Montserrat:wght@800&family=Reenie+Beanie&display=swap" rel="stylesheet">
    
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>

    <style>
        :root {
            --primary: #4D79FF;
            --accent: #FFD93D;
            --success: #28a745;
            --danger: #dc3545;
            --card-bg: rgba(30, 30, 30, 0.9);
            --text-main: #FFFFFF;
            --font-head: 'Montserrat', sans-serif;
            --font-body: 'Poppins', sans-serif;
            --font-hand: 'Reenie Beanie', cursive;
        }

        body {
            /* FONDO DEPORTIVO */
            background-image: url('https://images.unsplash.com/photo-1533107862482-0e6974b06ec4?q=80&w=2574&auto=format&fit=crop');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: var(--text-main);
            font-family: var(--font-body);
            margin: 0; padding: 0;
            overflow-x: hidden;
            padding-bottom: 90px;
        }

        body::before {
            content: ''; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(10, 10, 20, 0.85); z-index: -1;
        }

        /* --- UI COMPONENTES --- */
        .solid-panel {
            background-color: var(--card-bg); border-radius: 12px; padding: 20px;
            margin-bottom: 15px; border: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 4px 15px rgba(0,0,0,0.5); backdrop-filter: blur(5px);
        }

        .btn-solid {
            background-color: var(--primary); color: white; border: none; border-radius: 8px;
            padding: 12px; width: 100%; font-weight: 700; text-transform: uppercase;
            font-family: var(--font-head); margin-top: 10px; cursor: pointer; transition: 0.2s;
        }
        .btn-solid:active { transform: scale(0.95); }

        .btn-outline {
            background: transparent; border: 2px solid #555; color: #aaa;
            border-radius: 8px; padding: 10px; width: 100%; font-weight: 700;
            margin-top: 5px; cursor: pointer;
        }
        .btn-outline.active { border-color: var(--success); color: var(--success); background: rgba(40, 167, 69, 0.1); }

        .solid-input, .solid-textarea {
            background-color: rgba(0,0,0,0.5); border: 1px solid #555; color: white;
            padding: 12px; border-radius: 8px; width: 100%; font-size: 1rem;
            margin-bottom: 10px; font-family: var(--font-body); text-align: center;
        }
        .solid-textarea { text-align: left; }

        /* --- MAPA REAL --- */
        .map-container {
            position: relative; width: 100%; height: 350px; background: #000;
            border-radius: 15px; overflow: hidden; border: 2px solid #444;
        }
        .map-frame {
            width: 100%; height: 100%; border: 0; 
            pointer-events: none; /* Fondo fijo */
            filter: brightness(0.8) contrast(1.1);
        }
        .map-pin {
            position: absolute; width: 40px; height: 40px; background: var(--accent);
            border-radius: 50%; display: flex; align-items: center; justify-content: center;
            color: #000; font-weight: bold; cursor: pointer; border: 3px solid #fff;
            box-shadow: 0 4px 8px rgba(0,0,0,0.8); transform: translate(-50%, -50%);
            transition: transform 0.2s; font-size: 1.2rem; z-index: 10;
        }
        .map-pin:active { transform: translate(-50%, -50%) scale(1.2); }
        .map-pin.locked { background: #555; border-color: #777; color: #888; }

        /* --- TERMÓMETROS --- */
        .thermo-container {
            background: rgba(0,0,0,0.6); border-radius: 15px; padding: 15px; 
            margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.1);
        }
        .progress-bar-bg { background: #444; height: 20px; border-radius: 10px; overflow: hidden; margin-top: 8px; }
        .fill-team { background: linear-gradient(90deg, #4D79FF, #00d2ff); height: 100%; width: 0%; transition: width 1s ease-out; }
        .fill-global { background: linear-gradient(90deg, #FFD93D, #FF6B6B); height: 100%; width: 35%; transition: width 1s ease-out; }

        /* --- RADAR CHART --- */
        .radar-container { background: rgba(0,0,0,0.5); border-radius: 15px; padding: 10px; border: 1px solid #444; height: 250px; }

        /* --- CONTRATO --- */
        .parchment {
            background: #fdfbf7; color: #333; padding: 20px; border-radius: 5px;
            box-shadow: 0 0 20px rgba(0,0,0,0.5); font-family: var(--font-body);
            position: relative; border: 10px solid #2C2C2C;
        }
        .parchment h4 { font-family: var(--font-head); color: #000; text-transform: uppercase; border-bottom: 2px solid #000; padding-bottom: 10px; }
        .signature-pad {
            width: 100%; height: 80px; border: 2px dashed #999;
            background: rgba(255,255,255,0.5); margin-top: 20px;
            display: flex; align-items: center; justify-content: center;
            font-family: var(--font-hand); font-size: 2rem; color: #000080;
            cursor: pointer; position: relative;
        }
        .signature-pad::after { content: 'Cliquez pour signer'; font-family: var(--font-body); font-size: 0.8rem; color: #999; position: absolute; bottom: 5px; }
        .signature-pad.signed::after { content: ''; }

        /* --- HOME GRID --- */
        .home-btn {
            background-color: var(--card-bg); border: 1px solid rgba(255,255,255,0.1);
            border-radius: 15px; padding: 15px 10px; text-align: center;
            cursor: pointer; height: 100%; display: flex; flex-direction: column;
            justify-content: center; align-items: center; min-height: 110px;
        }
        .home-btn:active { transform: scale(0.95); background: rgba(255,255,255,0.1); }
        .home-btn i { font-size: 1.8rem; margin-bottom: 8px; }
        .home-btn h3 { font-size: 0.75rem; margin: 0; font-weight: 700; text-transform: uppercase; }

        /* --- AVATAR --- */
        .avatar-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 20px; }
        .avatar-item { background: rgba(0,0,0,0.5); border: 2px solid #444; border-radius: 10px; padding: 10px; text-align: center; cursor: pointer; }
        .avatar-item.selected { background: rgba(77, 121, 255, 0.3); border-color: var(--primary); }
        .trait-selector { display: flex; overflow-x: auto; padding-bottom: 10px; }
        .trait-tag { background: #333; padding: 5px 15px; border-radius: 20px; white-space: nowrap; cursor: pointer; border: 1px solid #444; font-size: 0.85rem; margin-right: 5px; }
        .trait-tag.selected { background: var(--accent); color: black; font-weight: bold; }

        /* --- OTHERS --- */
        .phase-card { cursor: pointer; border-left: 4px solid #555; background: var(--card-bg); padding: 15px; margin-bottom: 10px; border-radius: 8px; }
        .phase-card.completed { border-left-color: var(--success); background: rgba(40, 167, 69, 0.1); }
        .odd-badge { font-size: 0.65rem; background: #333; padding: 2px 6px; border-radius: 4px; color: var(--accent); font-weight: bold; margin-bottom: 4px; display: inline-block; }
        .view { display: none; padding: 20px; min-height: 100vh; }
        .active-view { display: block; animation: fadeIn 0.4s; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .dock-nav { position: fixed; bottom: 0; left: 0; width: 100%; background-color: #1a1a1a; border-top: 1px solid #333; display: flex; justify-content: space-around; padding: 15px 0; z-index: 1000; }
        .dock-item { font-size: 1.4rem; color: #666; cursor: pointer; }
        .dock-item.active { color: var(--primary); transform: translateY(-5px); }
        .custom-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.95); z-index: 2000; justify-content: center; align-items: center; }
        .custom-modal.show { display: flex; }
        .modal-content-solid { background: #222; border: 1px solid #444; border-radius: 12px; padding: 30px; width: 90%; max-width: 400px; text-align: center; }
        .mood-btn { font-size: 2rem; background: #333; border: 1px solid #444; border-radius: 10px; padding: 10px; cursor: pointer; flex: 1; text-align: center; margin: 0 2px; }
        .mood-btn.selected { background: var(--primary); border-color: var(--primary); transform: scale(1.1); }
        .journal-entry { border-left: 3px solid var(--accent); margin-bottom: 10px; }
        .journal-img { width: 100%; border-radius: 8px; margin-top: 10px; }
        .game-opt { background: #333; padding: 15px; margin-bottom: 10px; border-radius: 8px; cursor: pointer; text-align: center; font-weight: bold; }
        .game-opt.correct { border-color: var(--success); background: rgba(40, 167, 69, 0.2); }
        .game-opt.wrong { border-color: #dc3545; background: rgba(220, 53, 69, 0.2); }
        .vote-card { background: #333; padding: 15px; border-radius: 8px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
    </style>
</head>
<body>

    <section id="view-avatar" class="view active-view">
        <div class="text-center mt-4 mb-4">
            <h2 style="font-family: var(--font-head); text-transform: uppercase;">Crée ton Athlète</h2>
            <p class="text-secondary small">CHOISISSEZ VOTRE CHAMPION</p>
        </div>
        <div class="avatar-grid" id="sprite-container"></div>
        <div class="solid-panel mt-4">
            <label class="small text-secondary mb-2 d-block text-start">NOM</label>
            <input type="text" id="player-name" class="solid-input" placeholder="Pseudo...">
            <label class="small text-secondary mb-2 d-block text-start mt-3">SUPER-POUVOIR</label>
            <div class="trait-selector" id="trait-container"></div>
            <input type="hidden" id="selected-trait">
        </div>
        <button onclick="app.saveProfile()" class="btn-solid mt-2">ENTRER DANS LE STADE <i class="fa-solid fa-person-running"></i></button>
    </section>

    <section id="view-home" class="view">
        <div class="d-flex align-items-center justify-content-between mb-4 mt-3">
            <div>
                <h1 style="font-family: var(--font-head); font-size: 1.8rem; line-height: 1; text-transform: uppercase;">J.O. AVENIR</h1>
                <small class="text-secondary">LYCÉE OLYMPIQUE</small>
            </div>
            <div class="text-center" onclick="app.showView('view-avatar')" style="cursor:pointer">
                <div id="mini-avatar" style="font-size: 1.8rem; color: var(--accent); background: rgba(255,255,255,0.1); padding: 5px; border-radius: 50%;"></div>
            </div>
        </div>
        
        <div class="thermo-container">
            <div class="d-flex justify-content-between align-items-end">
                <h6 class="mb-0 fw-bold text-white"><i class="fa-solid fa-earth-americas text-warning me-2"></i> IMPACT GLOBAL</h6>
                <small class="text-accent fw-bold">CLASSE</small>
            </div>
            <div class="progress-bar-bg">
                <div class="fill-global"></div>
            </div>
            <small class="text-secondary" style="font-size: 0.65rem;">Objectif commun (ODD 17)</small>
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
                <div class="home-btn" onclick="app.nav('games', 'nav-games')">
                    <i class="fa-solid fa-gamepad text-primary"></i>
                    <h3>ARCADE</h3>
                </div>
            </div>
            <div class="col-12">
                <div class="home-btn flex-row gap-3 py-3" style="min-height: auto;" onclick="app.nav('oscars', 'nav-oscars')">
                    <i class="fa-solid fa-award text-accent mb-0"></i><h3 class="mb-0">VOTE & ÉVALUATION</h3>
                </div>
            </div>
        </div>
    </section>

    <section id="view-dashboard" class="view">
        <h4 class="fw-bold mb-3">PROGRESSION</h4>
        
        <div class="thermo-container">
            <div class="d-flex justify-content-between align-items-end">
                <h6 class="mb-0 fw-bold text-white"><i class="fa-solid fa-people-group text-primary me-2"></i> MON ÉQUIPE</h6>
                <small id="team-percent-text" class="text-primary fw-bold">0%</small>
            </div>
            <div class="progress-bar-bg">
                <div id="team-progress-bar" class="fill-team"></div>
            </div>
        </div>

        <div id="missions-list"></div>
    </section>

    <section id="view-map" class="view">
        <h4 class="fw-bold mb-3">PLAN DU CAMPUS</h4>
        <p class="text-secondary small">Localisation des épreuves</p>
        
        <div class="map-container">
            <iframe class="map-frame" 
                src="https://maps.google.com/maps?q=Carr.+de+Piedrabuena,+S/N,+13002+Ciudad+Real&t=k&z=19&output=embed" 
                frameborder="0" scrolling="no" marginheight="0" marginwidth="0">
            </iframe>

            <div class="map-pin" style="top: 30%; left: 40%;" onclick="alert('Zone Obstacles')">🏋️</div>
            <div class="map-pin" style="top: 60%; left: 60%;" onclick="alert('Grande Gymkhana')">🏁</div>
            <div class="map-pin" style="top: 80%; left: 30%;" onclick="alert('Ravitaillement')">🍎</div>
            <div class="map-pin locked" style="top: 20%; left: 80%;">🔒</div>
        </div>
        <div class="solid-panel mt-3">
            <h6 class="text-white mb-2"><i class="fa-solid fa-location-dot text-danger"></i> Légende</h6>
            <ul class="list-unstyled text-secondary small mb-0">
                <li>🏋️ Zone Obstacles (Jan-Fév)</li>
                <li>🍎 Ravitaillement (Avril)</li>
                <li>🏁 Arrivée Finale (Juin)</li>
            </ul>
        </div>
        <button onclick="app.nav('home')" class="btn btn-link text-secondary w-100">Retour</button>
    </section>

    <section id="view-debate" class="view">
        <div class="text-center mt-4 mb-3">
            <h2 style="font-family: var(--font-head);">ZONE DE DÉBAT</h2>
            <p class="text-secondary small">PHASE 2: ÉQUIPES INCLUSIVES</p>
        </div>
        
        <div class="radar-container mb-3">
            <canvas id="radarChart"></canvas>
        </div>
        <p class="text-center text-white-50 small mb-3">Est-ce que votre équipe est équilibrée ?</p>

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
            <p class="small">Nous nous engageons à :</p>
            <ul class="small ps-3">
                <li>Respecter les adversaires (ODD 16).</li>
                <li>Accepter la défaite.</li>
                <li>Jouer sans tricher.</li>
            </ul>
            <div class="text-center mt-4">
                <strong>Signature :</strong>
                <div class="signature-pad" id="sign-pad" onclick="app.signPact(this)"></div>
            </div>
        </div>
        <button onclick="app.nav('dashboard')" class="btn btn-link text-secondary w-100">Retour</button>
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
            <input type="text" id="user-input" class="solid-input text-uppercase" placeholder="CODE PROFESSEUR">
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
                if(viewName === 'dashboard') { app.renderList(); setTimeout(app.updateThermo, 100); }
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
                    if (m.id === 4 && !locked) action = `app.nav('rules')`;

                    list.innerHTML += `<div class="solid-panel phase-card d-flex align-items-center ${status} ${locked}" onclick="${action}"><div class="me-3 text-center" style="width: 40px;"><i class="fa-solid ${m.icon} fa-xl text-secondary"></i></div><div class="flex-grow-1"><span class="odd-badge">${m.odd}</span><h6 class="mb-0 fw-bold text-white">${m.title}</h6></div><i class="fa-solid ${iconCheck}"></i></div>`;
                });
            },

            // --- MODAL / VALIDACIÓN ---
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
                    setTimeout(() => { app.closeModal(); app.renderList(); app.updateThermo(); }, 1000);
                } else { document.getElementById('feedback-msg').innerText = "Incorrect"; document.getElementById('feedback-msg').style.color = "#dc3545"; }
            },

            // --- DEBATE, RULES, JUEGOS, ETC. ---
            goToDebate: () => { if(DATA.missions[1].completed) return; app.showView('view-debate'); setTimeout(app.initRadar, 200); },
            initRadar: () => {
                if(radarChart) radarChart.destroy();
                const ctx = document.getElementById('radarChart').getContext('2d');
                radarChart = new Chart(ctx, { type: 'radar', data: { labels: TRAITS, datasets: [{ label: 'Équilibre', data: [8,6,7,9,5], backgroundColor: 'rgba(77, 121, 255, 0.4)', borderColor: '#4D79FF', pointBackgroundColor: '#fff' }] }, options: { scales: { r: { grid: { color: '#444' }, angleLines: { color: '#444' }, suggesteMin: 0, suggestedMax: 10, ticks: { display: false } } }, plugins: { legend: { display: false } } } });
            },
            finalizeTeam: () => {
                const team = document.getElementById('team-name-create').value; if(!team || !document.getElementById('check-class').classList.contains('active')) return alert("Nom + Validation requis!");
                DATA.teamName = team; DATA.missions[1].completed = true; DATA.nominees.push(team);
                document.getElementById('home-team-badge').innerText = "Équipe: " + team; document.getElementById('home-team-badge').classList.replace('bg-secondary', 'bg-success');
                confetti(); app.nav('dashboard');
            },
            signPact: (el) => { el.innerHTML = "<i>Signé : " + DATA.user.name + "</i>"; el.classList.add("signed"); el.style.fontFamily = "var(--font-hand)"; DATA.missions[3].completed = true; confetti(); setTimeout(() => { app.nav('dashboard'); }, 1500); },
            
            startGame: (t) => { currentQuiz = QUIZ[t]; qIndex=0; score=0; document.getElementById('game-menu').style.display='none'; document.getElementById('game-interface').style.display='block'; app.renderQuestion(); },
            renderQuestion: () => { if(qIndex>=currentQuiz.length){ alert("Fin!"); app.exitGame(); return;} const q=currentQuiz[qIndex]; document.getElementById('game-question').innerText=q.q; const o=document.getElementById('game-options'); o.innerHTML=""; q.a.forEach((ans,i)=>{ o.innerHTML+=`<div class='solid-panel p-2 text-center' style='cursor:pointer' onclick='app.checkAnswer(${i})'>${ans}</div>`}); },
            checkAnswer: (i) => { if(i===currentQuiz[qIndex].c){score+=10; confetti();} setTimeout(()=>{qIndex++; app.renderQuestion()},500); },
            exitGame: () => { document.getElementById('game-interface').style.display='none'; document.getElementById('game-menu').style.display='block'; },
            
            selectMood: (e,m) => { document.querySelectorAll('.mood-btn').forEach(b=>b.classList.remove('selected')); e.classList.add('selected'); document.getElementById('selected-mood').value=m; },
            saveJournal: () => { const m=document.getElementById('selected-mood').value, t=document.getElementById('journal-text').value, f=document.getElementById('journal-photo'); if(!m||!t) return alert("Remplissez !"); const e={d:new Date().toLocaleDateString(), m, t, i:null}; if(f.files[0]){ const r=new FileReader(); r.onload=(ev)=>{e.i=ev.target.result; DATA.journal.unshift(e); app.renderJournal();}; r.readAsDataURL(f.files[0]); } else { DATA.journal.unshift(e); app.renderJournal(); } document.getElementById('journal-text').value=""; confetti(); },
            renderJournal: () => { const c=document.getElementById('journal-feed'); c.innerHTML=""; DATA.journal.forEach(e=>{ c.innerHTML+=`<div class='solid-panel journal-entry'><div class='d-flex justify-content-between'><span>${e.d}</span><span>${e.m}</span></div><p class='text-white'>${e.t}</p>${e.i?`<img src='${e.i}' class='journal-img'>`:''}</div>`}); },

            showNominees: (c) => { if(DATA.votes[c]) return alert("Déjà voté!"); document.getElementById('oscars-menu').style.display='none'; document.getElementById('oscars-voting').style.display='block'; const l=document.getElementById('nominees-list'); l.innerHTML=""; DATA.nominees.forEach(t=>{ if(t!==DATA.teamName) l.innerHTML+=`<div class='vote-card'><span class='text-white fw-bold'>${t}</span><button class='btn btn-sm btn-outline-warning' onclick='app.submitVote("${c}","${t}")'>VOTER</button></div>` }); },
            submitVote: (c,t) => { if(confirm("Sûr?")){ DATA.votes[c]=true; app.exitVoting(); confetti(); } },
            exitVoting: () => { document.getElementById('oscars-voting').style.display='none'; document.getElementById('oscars-menu').style.display='block'; },

            // --- THERMOS ---
            updateThermo: () => {
                const c = DATA.missions.filter(m => m.completed).length; const t = DATA.missions.length; const pct = Math.round((c/t)*100);
                document.getElementById('team-progress-bar').style.width = pct + "%"; document.getElementById('team-percent-text').innerText = pct + "%";
            }
        };
        app.init();
    </script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=True)
