from flask import Flask, render_template_string

app = Flask(__name__)

# Aquí guardamos todo el código Frontend (HTML + CSS + JS) en una sola variable
# para que no tengas que crear múltiples archivos.
PAGE_CONTENT = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Gymkhana Gen Z - App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        :root {
            --bg-gradient: linear-gradient(-45deg, #1a1a2e, #16213e, #0f3460, #e94560);
            --glass-bg: rgba(255, 255, 255, 0.1);
            --glass-border: 1px solid rgba(255, 255, 255, 0.15);
            --neon-blue: #00f2fe;
            --text-color: #fff;
            --font-main: 'Poppins', sans-serif;
        }
        body {
            font-family: var(--font-main);
            color: var(--text-color);
            margin: 0;
            background: #1a1a2e;
            height: 100vh;
            overflow: hidden;
        }
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
        .glass-panel {
            background: var(--glass-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: 24px;
            border: var(--glass-border);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        }
        .glass-input {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 50px;
            padding: 15px;
            color: white;
            text-align: center;
            width: 100%;
        }
        .btn-neon {
            background: linear-gradient(90deg, var(--neon-blue), #4facfe);
            color: #000;
            border: none;
            padding: 12px;
            border-radius: 50px;
            font-weight: 800;
            width: 100%;
            margin-top: 10px;
        }
        .view {
            display: none;
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.4s ease, transform 0.4s ease;
            height: 100%;
            overflow-y: auto;
            padding-bottom: 100px;
        }
        .active-view {
            display: block;
            opacity: 1;
            transform: translateY(0);
        }
        .mission-item.completed {
            border-left: 4px solid #00f2fe;
            background: rgba(0, 242, 254, 0.1);
        }
        .mission-item.locked {
            opacity: 0.5;
            filter: grayscale(1);
            pointer-events: none;
        }
        .dock-nav {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(25, 25, 35, 0.9);
            padding: 10px 25px;
            border-radius: 50px;
            display: flex;
            gap: 25px;
            z-index: 1000;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .dock-item {
            font-size: 1.5rem;
            color: rgba(255,255,255,0.5);
            cursor: pointer;
            transition: 0.3s;
        }
        .dock-item.active {
            color: var(--neon-blue);
            transform: scale(1.2);
        }
        .text-gold { color: #fce38a; }
        .oscar-card { border: 1px solid rgba(252, 227, 138, 0.2); }
    </style>
</head>
<body>

    <div class="bg-animation"></div>

    <section id="view-login" class="view active-view d-flex flex-column justify-content-center align-items-center p-4">
        <div class="glass-panel p-5 text-center">
            <i class="fa-solid fa-rocket fa-4x mb-3" style="color: var(--neon-blue);"></i>
            <h1 class="fw-bold mb-0">GYMKHANA</h1>
            <p class="text-white-50 small">INNOVATION & ODD</p>
            <div class="mt-4">
                <input type="text" id="team-input" class="glass-input mb-3" placeholder="Nom de l'équipe">
                <button onclick="app.login()" class="btn-neon">COMMENCER</button>
            </div>
        </div>
    </section>

    <section id="view-dashboard" class="view p-3">
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h5 id="display-team" class="fw-bold mb-0">...</h5>
            <span class="badge bg-dark border border-secondary"><i class="fa-solid fa-star text-warning"></i> <span id="medal-count">0</span>/4</span>
        </div>

        <div class="glass-panel p-3 mb-4 d-flex justify-content-center align-items-center position-relative" style="height: 180px;">
            <canvas id="progressChart"></canvas>
            <div class="position-absolute text-center" style="pointer-events: none;">
                <h2 id="percent-text" class="fw-bold m-0 text-white">0%</h2>
            </div>
        </div>

        <div id="missions-list"></div>
    </section>

    <section id="view-oscars" class="view p-3 text-center">
        <h2 class="fw-bold mb-1">Les Oscars</h2>
        <p class="text-white-50 small mb-4">Cérémonie de l'Innovation</p>
        <div class="row g-3">
            <div class="col-6"><div class="glass-panel oscar-card p-3"><i class="fa-solid fa-microphone-lines fa-2x text-gold mb-2"></i><h6 class="small fw-bold">Scénario</h6></div></div>
            <div class="col-6"><div class="glass-panel oscar-card p-3"><i class="fa-solid fa-users fa-2x text-gold mb-2"></i><h6 class="small fw-bold">Casting</h6></div></div>
            <div class="col-6"><div class="glass-panel oscar-card p-3"><i class="fa-solid fa-lightbulb fa-2x text-gold mb-2"></i><h6 class="small fw-bold">FX Spéciaux</h6></div></div>
            <div class="col-6"><div class="glass-panel oscar-card p-3"><i class="fa-solid fa-earth-europe fa-2x text-gold mb-2"></i><h6 class="small fw-bold">Documentaire</h6></div></div>
        </div>
    </section>

    <div id="bottom-nav" class="dock-nav d-none">
        <div class="dock-item active" onclick="app.nav('dashboard', this)"><i class="fa-solid fa-gamepad"></i></div>
        <div class="dock-item" onclick="app.nav('oscars', this)"><i class="fa-solid fa-trophy"></i></div>
    </div>

    <div class="modal fade" id="missionModal" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content glass-panel" style="background: rgba(20,20,30,0.95);">
                <div class="modal-body text-center p-4">
                    <h4 id="modal-title" class="fw-bold mb-2">...</h4>
                    <p id="modal-desc" class="text-white-50 small mb-4">...</p>
                    <input type="text" id="secret-code" class="glass-input text-uppercase fs-4 mb-3" placeholder="CODE">
                    <button onclick="app.validate()" class="btn-neon">Vérifier</button>
                    <div id="feedback-msg" class="mt-3 small fw-bold"></div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
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

        const app = {
            login: () => {
                const input = document.getElementById('team-input').value;
                if (!input) return;
                GAME_DATA.teamName = input;
                document.getElementById('display-team').innerText = input;
                app.switchView('view-login', 'view-dashboard');
                document.getElementById('bottom-nav').classList.remove('d-none');
                app.renderMissions();
                setTimeout(app.initChart, 100); 
            },
            nav: (target, el) => {
                document.querySelectorAll('.dock-item').forEach(i => i.classList.remove('active'));
                el.classList.add('active');
                document.querySelectorAll('.view').forEach(v => {
                    v.style.opacity = 0;
                    v.style.transform = 'translateY(-20px)';
                    setTimeout(() => v.classList.remove('active-view'), 300);
                });
                setTimeout(() => {
                    const next = document.getElementById(`view-${target}`);
                    next.classList.add('active-view');
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
                    const status = m.completed ? 'completed' : (isLocked ? 'locked' : '');
                    const icon = m.completed ? 'fa-check text-info' : 'fa-play text-white-50';
                    container.innerHTML += `
                        <div class="glass-panel p-3 mb-3 mission-item d-flex align-items-center ${status}" onclick="app.openMission(${m.id})">
                            <i class="fa-solid ${icon} fa-xl me-3"></i>
                            <div>
                                <small class="text-white-50 text-uppercase fw-bold" style="font-size:0.65rem">Cherchez: ${m.group}</small>
                                <h6 class="mb-0 fw-bold">${m.title}</h6>
                            </div>
                        </div>`;
                });
                document.getElementById('medal-count').innerText = GAME_DATA.missions.filter(m => m.completed).length;
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
                const input = document.getElementById('secret-code').value.toUpperCase();
                const m = GAME_DATA.missions.find(x => x.id === GAME_DATA.currentMissionId);
                if (input === m.code) {
                    m.completed = true;
                    document.getElementById('feedback-msg').innerHTML = '<span class="text-info">Correct!</span>';
                    setTimeout(() => {
                        bootstrap.Modal.getInstance(document.getElementById('missionModal')).hide();
                        app.renderMissions();
                        app.updateChart();
                    }, 1000);
                } else {
                    document.getElementById('feedback-msg').innerHTML = '<span class="text-danger">Incorrect.</span>';
                }
            },
            initChart: () => {
                const ctx = document.getElementById('progressChart').getContext('2d');
                progressChart = new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        datasets: [{
                            data: [0, 4],
                            backgroundColor: ['#00f2fe', 'rgba(255,255,255,0.1)'],
                            borderWidth: 0,
                            cutout: '85%'
                        }]
                    },
                    options: { responsive: true, maintainAspectRatio: false, events: [] }
                });
            },
            updateChart: () => {
                const completed = GAME_DATA.missions.filter(m => m.completed).length;
                progressChart.data.datasets[0].data = [completed, 4 - completed];
                progressChart.update();
                document.getElementById('percent-text').innerText = Math.round((completed/4)*100) + '%';
            }
        };
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(PAGE_CONTENT)

if __name__ == '__main__':
    # Ejecuta la app en el puerto 5000
    app.run(debug=True, port=5000)
