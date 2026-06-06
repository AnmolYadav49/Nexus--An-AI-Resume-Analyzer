document.addEventListener('DOMContentLoaded', () => {
    // === Core Career Persistence Engine === (Phase 12)
    const CareerPersistence = {
        saveAnalysis: (data) => {
            let history = JSON.parse(localStorage.getItem('nexus_history') || '[]');
            const entry = {
                id: Date.now(),
                timestamp: new Date().toISOString(),
                role: data.role,
                score: data.match_score,
                found_skills: data.found_skills,
                missing_skills: data.missing_skills
            };
            history.unshift(entry);
            localStorage.setItem('nexus_history', JSON.stringify(history.slice(0, 10))); // Cap at 10
        },
        getHistory: () => JSON.parse(localStorage.getItem('nexus_history') || '[]'),
        clearHistory: () => localStorage.removeItem('nexus_history')
    };

    // Dashboard Population Logic (Phase 12)
    if (window.location.pathname.includes('/dashboard')) {
        const history = CareerPersistence.getHistory();
        const table = document.getElementById('historyTableBody');
        const emptyMsg = document.getElementById('noHistoryMsg');
        const statAnalyses = document.getElementById('stat-analyses');
        const statAvg = document.getElementById('stat-avg');
        const statResumes = document.getElementById('stat-resumes');

        if (history.length === 0) {
            emptyMsg?.classList.remove('d-none');
        } else {
            statAnalyses.innerText = history.length;
            const avg = Math.round(history.reduce((a, b) => a + (b.score || 0), 0) / history.length);
            statAvg.innerText = avg + '%';
            
            // Build resumes from builder history if present
            const builderCount = JSON.parse(localStorage.getItem('nexus_builder_history') || '[]').length;
            statResumes.innerText = builderCount;

            (history || []).forEach(row => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td class="py-3 px-4 border-light border-opacity-10 border-bottom">
                        <div class="text-white fw-medium"><i class="bi bi-file-earmark-text text-primary opacity-75 me-2"></i> analysis_${row.id}.scan</div>
                        <span class="small opacity-50 ms-4">Domain alignment: ${row.role}</span>
                    </td>
                    <td class="py-3 px-4 text-center border-light border-opacity-10 border-bottom align-middle">
                        <span class="badge bg-${row.score > 75 ? 'success' : 'warning'} bg-opacity-25 text-${row.score > 75 ? 'emerald' : 'warning'} border border-${row.score > 75 ? 'success' : 'warning'} border-opacity-25 rounded-pill px-3 py-2">${row.score}%</span>
                    </td>
                    <td class="py-3 px-4 text-center border-light border-opacity-10 border-bottom align-middle text-white-50">${row.role}</td>
                    <td class="py-3 px-4 text-end border-light border-opacity-10 border-bottom align-middle small d-none d-md-table-cell">${new Date(row.timestamp).toLocaleDateString()}</td>
                `;
                table?.appendChild(tr);
            });
        }
    }


    // === Upload Interactions ===
    const dropzone = document.querySelector('.dropzone');
    const fileInput = document.querySelector('.dropzone-input');
    const uploadText = document.getElementById('upload-text');
    
    if (dropzone && fileInput) {
        dropzone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropzone.classList.add('active');
        });

        dropzone.addEventListener('dragleave', (e) => {
            e.preventDefault();
            dropzone.classList.remove('active');
        });

        fileInput.addEventListener('change', function() {
            dropzone.classList.remove('active');
            if (this.files && this.files.length > 0) {
                const fileName = this.files[0].name;
                const ext = fileName.split('.').pop().toLowerCase();
                
                if (ext === 'pdf' || ext === 'docx') {
                    dropzone.style.borderColor = 'var(--accent-emerald)';
                    uploadText.innerHTML = `<i class="bi bi-file-earmark-check text-emerald fs-3 d-block mb-2"></i>
                                            <span class="text-white d-block fw-medium">${fileName}</span>
                                            <span class="text-muted small">Ready to analyze</span>`;
                } else {
                    alert('Invalid file format. Please upload PDF or DOCX.');
                    this.value = '';
                    resetDropzone();
                }
            } else {
                resetDropzone();
            }
        });

        function resetDropzone() {
            dropzone.style.borderColor = 'var(--glass-highlight)';
            uploadText.innerHTML = `<i class="bi bi-cloud-arrow-up fs-2 d-block mb-3 text-muted"></i>
                                    <h5 class="fw-medium mb-1">Drag and drop your resume</h5>
                                    <p class="text-muted small mb-0">PDF or DOCX up to 5MB</p>`;
        }
    }

    // === Form Submit Overlay ===
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            if(!fileInput.value) {
                e.preventDefault();
                alert('Please upload a resume first.');
                return;
            }
            document.getElementById('analysisOverlay').classList.remove('d-none');
        });
    }

    // === Chart.js Initializations ===
    // If we're on the result page, initialize charts if canvases exist
    
    // 1. Resume DNA Radar Logic
    const dnaCtx = document.getElementById('dnaRadarChart');
    let activeDnaChart = null; // Store it globally to destroy on update
    
    if (dnaCtx) {
        const dnaData = JSON.parse(dnaCtx.getAttribute('data-dna'));
        Chart.defaults.color = 'rgba(255, 255, 255, 0.5)';
        
        activeDnaChart = new Chart(dnaCtx, {
            type: 'radar',
            data: {
                labels: ['Technical', 'Leadership', 'Impact', 'Communication', 'Problem Sec'],
                datasets: [{
                    label: 'DNA Profile',
                    data: dnaData,
                    backgroundColor: 'rgba(129, 140, 248, 0.25)',
                    borderColor: 'rgba(192, 132, 252, 0.9)',
                    pointBackgroundColor: '#34D399',
                    pointBorderColor: '#fff',
                    borderWidth: 2,
                    pointHoverRadius: 6,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        angleLines: { color: 'rgba(255,255,255,0.05)' },
                        grid: { color: 'rgba(255,255,255,0.1)' },
                        pointLabels: { color: 'rgba(255,255,255,0.7)', font: { size: 10, family: 'Inter' } },
                        ticks: { display: false, max: 100, min: 0, stepSize: 20 }
                    }
                },
                plugins: { legend: { display: false }, tooltip: { backgroundColor: 'rgba(5, 5, 8, 0.9)', padding: 10, cornerRadius: 8 } }
            }
        });
    }

    // === Intersection Observer for Scroll Reveals ===
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };
    
    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, observerOptions);
    
    const revealElements = document.querySelectorAll('.scroll-reveal');
    revealElements.forEach(el => observer.observe(el));

    // ===================================
    // === Authentication Domain Logic ===
    // ===================================

    // Smooth Dual-Pane Switching
    window.toggleAuth = function(mode) {
        const loginForm = document.getElementById('loginForm');
        const signupForm = document.getElementById('signupForm');
        
        if (mode === 'signup') {
            loginForm.classList.remove('active');
            loginForm.classList.add('hidden');
            setTimeout(() => {
                signupForm.classList.remove('hidden');
                signupForm.classList.add('active');
            }, 100);
        } else {
            signupForm.classList.remove('active');
            signupForm.classList.add('hidden');
            setTimeout(() => {
                loginForm.classList.remove('hidden');
                loginForm.classList.add('active');
            }, 100);
        }
    };

    // Live Password Strength Matrix
    const signupPassword = document.getElementById('signupPassword');
    if (signupPassword) {
        signupPassword.addEventListener('input', function(e) {
            let val = e.target.value;
            let score = 0;
            if(val.length > 7) score++;
            if(/[A-Z]/.test(val)) score++;
            if(/[0-9]/.test(val)) score++;
            if(/[^A-Za-z0-9]/.test(val)) score++;
            
            ['str1', 'str2', 'str3', 'str4'].forEach((id, i) => {
                const bar = document.getElementById(id);
                bar.className = 'strength-bar rounded h-100 bg-light opacity-10 w-25'; // reset to base
                if (i < score) {
                    bar.classList.remove('bg-light', 'opacity-10');
                    if(score <= 2) bar.classList.add('bg-danger');
                    else if(score === 3) bar.classList.add('bg-warning');
                    else bar.classList.add('bg-emerald');
                }
            });
            
            const txt = document.getElementById('strengthText');
            if(score === 0) { txt.innerText = "Password must be at least 8 characters"; txt.className = "text-muted small mt-2 d-block"; }
            else if(score <= 2) { txt.innerText = "Weak"; txt.className = "small mt-2 d-block text-danger"; }
            else if(score === 3) { txt.innerText = "Medium"; txt.className = "small mt-2 d-block text-warning"; }
            else { txt.innerText = "Strong"; txt.className = "small mt-2 d-block text-emerald"; }
        });
    }

    // Smart Welcome Greeting Popup (4 seconds, then fades cleanly)
    if(document.getElementById('welcomeState')) {
        setTimeout(() => {
            const welcome = document.getElementById('welcomeState');
            welcome.classList.remove('d-none');
            welcome.classList.add('animate-up');
            
            setTimeout(() => {
                welcome.style.opacity = 0;
                welcome.style.transform = 'translate(-50%, -20px)';
                welcome.style.transition = 'all 0.6s ease';
                setTimeout(() => welcome.classList.add('d-none'), 600); // cleanup
            }, 4500);
        }, 600);
    }

    // ===================================
    // === Nexus AI Global Chat Engine ===
    // ===================================

    window.toggleCoach = function(forceOpen) {
        const panel = document.getElementById('coachPanel');
        const btn = document.getElementById('coachMinBtn');
        if(!panel || !btn) return;
        
        const open = forceOpen !== undefined ? forceOpen : panel.classList.contains('d-none');
        
        if (open) {
            panel.classList.remove('d-none');
            panel.classList.add('show');
            btn.style.transform = 'scale(0)';
            setTimeout(() => document.getElementById('coachInput').focus(), 300);
        } else {
            panel.classList.add('d-none');
            panel.classList.remove('show');
            setTimeout(() => { btn.style.transform = 'scale(1)'; }, 300);
        }
    };
    
    // Context Engine
    function initContextChips() {
        const path = window.location.pathname;
        const chips = document.getElementById('coachQuickChips');
        let html = '';
        
        if(path === '/' || path.includes('analyze')) {
            html += `<span class="premium-pill border border-primary border-opacity-25 text-white-50 small cursor-pointer" onclick="document.getElementById('coachInput').value='Explain my ATS score'; sendCoachUrlMsg()"><i class="bi bi-magic text-primary me-1"></i> Explain ATS score</span>`;
            html += `<span class="premium-pill border border-emerald border-opacity-25 text-white-50 small cursor-pointer" onclick="document.getElementById('coachInput').value='Suggest missing skills'; sendCoachUrlMsg()"><i class="bi bi-tools text-emerald me-1"></i> Missing skills</span>`;
        } else if (path.includes('builder')) {
            html += `<span class="premium-pill border border-warning border-opacity-25 text-white-50 small cursor-pointer" onclick="document.getElementById('coachInput').value='Rewrite my project description'; sendCoachUrlMsg()"><i class="bi bi-pen text-warning me-1"></i> Rewrite project</span>`;
            html += `<span class="premium-pill border border-primary border-opacity-25 text-white-50 small cursor-pointer" onclick="document.getElementById('coachInput').value='Help me build a resume'; sendCoachUrlMsg()"><i class="bi bi-building text-primary me-1"></i> Guide Builder Steps</span>`;
        } else if (path.includes('dashboard')) {
            html += `<span class="premium-pill border border-danger border-opacity-25 text-white-50 small cursor-pointer" onclick="document.getElementById('coachInput').value='How to improve my averages?'; sendCoachUrlMsg()"><i class="bi bi-graph-up-arrow text-danger me-1"></i> Improve averages</span>`;
        } else {
            html += `<span class="premium-pill border border-primary border-opacity-25 text-white-50 small cursor-pointer" onclick="document.getElementById('coachInput').value='What does ATS mean?'; sendCoachUrlMsg()"><i class="bi bi-question-circle text-primary me-1"></i> What does ATS mean?</span>`;
            html += `<span class="premium-pill border border-emerald border-opacity-25 text-white-50 small cursor-pointer" onclick="document.getElementById('coachInput').value='Navigating the UI'; sendCoachUrlMsg()"><i class="bi bi-compass text-emerald me-1"></i> Navigating the UI</span>`;
        }
        
        if (chips) chips.innerHTML = html;
        
        // Greeting State & Proactive Strategy
        const greet = document.getElementById('coachGreeting');
        if(greet) {
            const history = CareerPersistence.getHistory();
            if(path.includes('builder')) greet.innerHTML = "Cognitive mapping complete. Shall we refactor your project syntax for high-performance verbs?";
            else if(path.includes('dashboard')) {
                 const best = history.length > 0 ? history[0].role : "Candidate";
                 greet.innerHTML = `Analyzing aggregate vectors for ${best}. Looking to pivot into higher-density roles?`;
            } else if(history.length > 0) {
                 greet.innerHTML = `Welcome back. Your previous ${history[0].role} profile was solid. Want to simulate it against different job vectors?`;
            } else {
                 greet.innerHTML = "Ready to optimize your application vectors. How can I help?";
            }
        }
    }
    
    // Call Context Builder
    initContextChips();

    window.sendCoachUrlMsg = function(msgFallback) {
        const input = document.getElementById('coachInput');
        const msg = msgFallback || input.value;
        if(!msg || !msg.trim()) return;
        const box = document.getElementById('coachHistory');
        
        // Render User Block
        box.innerHTML += `
        <div class="d-flex align-items-start flex-row-reverse gap-2 w-100 mt-2">
            <div class="bg-glass bg-opacity-25 p-2 rounded-4 rounded-top-right-0 text-white small border border-primary border-opacity-25 shadow-sm" style="max-width: 85%;">
                ${msg}
            </div>
        </div>`;
        input.value = '';
        box.scrollTop = box.scrollHeight;
        
        // Map Fake Loading Indicator
        const loaderId = 'loader_' + Date.now();
        box.innerHTML += `
        <div id="${loaderId}" class="d-flex align-items-center gap-2 w-100 mt-2 animate-up">
            <div class="bg-primary bg-opacity-25 text-indigo rounded-circle d-flex justify-content-center align-items-center flex-shrink-0" style="width: 30px; height: 30px;">
                <i class="bi bi-stars small"></i>
            </div>
            <div class="bg-dark bg-opacity-50 px-3 py-2 rounded-4 rounded-top-left-0 border border-light border-opacity-10 d-flex align-items-center shadow-sm">
                <span class="spinner-grow spinner-grow-sm text-primary text-opacity-50 mx-1" style="width: 0.3rem; height: 0.3rem;"></span>
                <span class="spinner-grow spinner-grow-sm text-primary text-opacity-75 mx-1" style="width: 0.3rem; height: 0.3rem; animation-delay: 0.2s;"></span>
                <span class="spinner-grow spinner-grow-sm text-primary mx-1" style="width: 0.3rem; height: 0.3rem; animation-delay: 0.4s;"></span>
            </div>
        </div>`;
        box.scrollTop = box.scrollHeight;
        
        // Simulating Real-Time Context Stream
        setTimeout(() => {
            if(document.getElementById(loaderId)) document.getElementById(loaderId).remove();
            
            let reply = "I am parsing your context layers. Let me synthesize a specific path forward for you shortly.";
            const lmsg = msg.toLowerCase();
            if(lmsg.includes('format')) reply = "Standardizing formatting structures generally passes 90% of basic parsing tests. Stick to PDF vectors.";
            if(lmsg.includes('verb') || lmsg.includes('rewrite') || lmsg.includes('project')) reply = "Passive syntaxes degrade performance metrics. I recommend applying engineering verb replacements.";
            if(lmsg.includes('skill')) reply = "Integrate your missing keywords natively into the chronological sequence of your project definitions. Don't force them.";
            if(lmsg.includes('improve') || lmsg.includes('average')) reply = "Elevating an average requires stripping superfluous jargon and quantifying output structures (achieved X, by Y, resulting in Z).";
            if(lmsg.includes('ats')) reply = "ATS (Applicant Tracking System) evaluates chronological keyword hierarchies against specific role vectors.";
            
            box.innerHTML += `
            <div class="d-flex align-items-start gap-2 w-100 mt-2 animate-up">
                <div class="bg-primary bg-opacity-25 text-indigo rounded-circle d-flex justify-content-center align-items-center mt-1 flex-shrink-0" style="width: 30px; height: 30px;">
                    <i class="bi bi-stars small"></i>
                </div>
                <div class="bg-dark bg-opacity-50 p-2 rounded-4 rounded-top-left-0 text-white-50 small border border-light border-opacity-10 shadow-sm" style="max-width: 85%;">
                    ${reply}
                </div>
            </div>`;
            box.scrollTop = box.scrollHeight;
        }, Math.random() * 800 + 800);
    };

});

