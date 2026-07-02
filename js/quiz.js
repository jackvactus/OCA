import { saveQuizScore } from './progress.js';

let questions = [];
let filtered = [];
let currentIndex = 0;
let answered = false;
let score = 0;
let container = null;
let onComplete = null;

export function initQuiz(questionsData, targetContainer, completeCallback) {
  questions = questionsData;
  container = targetContainer;
  onComplete = completeCallback;
  renderFilters();
}

function renderFilters() {
  container.innerHTML = `
    <div class="page-header">
      <h1><i class="fa-solid fa-circle-question" aria-hidden="true"></i> Quiz QCM</h1>
      <p>Entraînez-vous avec des questions type certification Oracle 1Z0-071</p>
    </div>
    <div class="quiz-filters">
      <label for="quiz-module-filter">Module :</label>
      <select id="quiz-module-filter" aria-label="Filtrer par module">
        <option value="all">Tous les modules</option>
        ${[...new Set(questions.map(q => q.module))].sort((a, b) => a - b).map(m =>
          `<option value="${m}">Module ${m}</option>`
        ).join('')}
      </select>
      <label for="quiz-count">Questions :</label>
      <select id="quiz-count" aria-label="Nombre de questions">
        <option value="10">10 questions</option>
        <option value="20" selected>20 questions</option>
        <option value="30">30 questions</option>
        <option value="all">Toutes</option>
      </select>
      <button class="btn btn-primary" id="quiz-start"><i class="fa-solid fa-play"></i> Démarrer</button>
    </div>
    <div id="quiz-area"></div>
  `;

  document.getElementById('quiz-start').addEventListener('click', startQuiz);
}

function startQuiz() {
  const moduleFilter = document.getElementById('quiz-module-filter').value;
  const count = document.getElementById('quiz-count').value;
  let pool = moduleFilter === 'all' ? [...questions] : questions.filter(q => q.module === parseInt(moduleFilter, 10));
  pool = shuffle(pool);
  if (count !== 'all') pool = pool.slice(0, parseInt(count, 10));
  filtered = pool;
  currentIndex = 0;
  score = 0;
  answered = false;
  renderQuestion();
}

function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function renderQuestion() {
  const area = document.getElementById('quiz-area');
  if (!area) return;

  if (currentIndex >= filtered.length) {
    renderResults(area);
    return;
  }

  const q = filtered[currentIndex];
  answered = false;
  const progress = Math.round(((currentIndex) / filtered.length) * 100);

  area.innerHTML = `
    <div class="quiz-container card">
      <div class="quiz-header">
        <span>Question ${currentIndex + 1} / ${filtered.length}</span>
        <span class="badge badge-primary">Module ${q.module}</span>
        <div class="quiz-progress" role="progressbar" aria-valuenow="${progress}" aria-valuemin="0" aria-valuemax="100">
          <div class="quiz-progress-fill" style="width:${progress}%"></div>
        </div>
      </div>
      <div class="quiz-question" id="quiz-question-text">${escapeHtml(q.question)}</div>
      ${q.code ? renderCodeBlock(q.code) : ''}
      <ul class="quiz-options" role="listbox" aria-label="Options de réponse">
        ${q.options.map((opt, i) =>
          `<li><button class="quiz-option" data-index="${i}" role="option">${escapeHtml(opt)}</button></li>`
        ).join('')}
      </ul>
      <div id="quiz-feedback"></div>
      <div class="exam-actions hidden" id="quiz-next-area">
        <button class="btn btn-primary" id="quiz-next">${currentIndex + 1 >= filtered.length ? 'Voir les résultats' : 'Question suivante'}</button>
      </div>
    </div>
  `;

  area.querySelectorAll('.quiz-option').forEach(btn => {
    btn.addEventListener('click', () => handleAnswer(parseInt(btn.dataset.index, 10), q));
  });

  if (window.hljs) {
    area.querySelectorAll('pre code').forEach(block => hljs.highlightElement(block));
  }
}

function handleAnswer(selectedIndex, q) {
  if (answered) return;
  answered = true;
  const isCorrect = selectedIndex === q.correctIndex;
  if (isCorrect) score++;

  const options = document.querySelectorAll('.quiz-option');
  options.forEach((btn, i) => {
    btn.disabled = true;
    if (i === q.correctIndex) btn.classList.add('correct');
    else if (i === selectedIndex) btn.classList.add('incorrect');
  });

  const feedback = document.getElementById('quiz-feedback');
  feedback.innerHTML = `
    <div class="quiz-explanation">
      <h4>${isCorrect ? '<i class="fa-solid fa-check" style="color:var(--success)"></i> Correct !' : '<i class="fa-solid fa-xmark" style="color:var(--error)"></i> Incorrect'}</h4>
      <p>${escapeHtml(q.explanation)}</p>
    </div>
  `;

  document.getElementById('quiz-next-area').classList.remove('hidden');
  document.getElementById('quiz-next').addEventListener('click', () => {
    currentIndex++;
    renderQuestion();
  });
}

function renderResults(area) {
  const moduleId = filtered[0]?.module || 'all';
  if (moduleId !== 'all' && typeof moduleId === 'number') {
    saveQuizScore(moduleId, score, filtered.length);
  }

  const percent = Math.round((score / filtered.length) * 100);
  area.innerHTML = `
    <div class="quiz-container card text-center">
      <h2>Résultats du quiz</h2>
      <div class="exam-score-circle ${percent >= 63 ? 'pass' : ''}">
        <span class="score">${score}/${filtered.length}</span>
        <span class="text-muted">${percent}%</span>
      </div>
      <p>${percent >= 63 ? 'Excellent ! Vous êtes prêt pour l\'examen.' : 'Continuez à réviser les modules faibles.'}</p>
      <button class="btn btn-primary" id="quiz-restart"><i class="fa-solid fa-rotate-right"></i> Recommencer</button>
      <a href="#/progress" class="btn btn-outline">Voir ma progression</a>
    </div>
  `;
  document.getElementById('quiz-restart').addEventListener('click', () => {
    document.getElementById('quiz-area').innerHTML = '';
    startQuiz();
  });
  if (onComplete) onComplete(score, filtered.length);
}

function renderCodeBlock(code) {
  return `<div class="code-block"><pre><code class="language-sql">${escapeHtml(code)}</code></pre></div>`;
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

export function getQuestionsByModule(questionsData, moduleId) {
  return questionsData.filter(q => q.module === moduleId);
}
