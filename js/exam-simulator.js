import { saveExamAttempt } from './progress.js';

const EXAM_SIZE = 63;
const EXAM_DURATION_MS = 120 * 60 * 1000;
const PASS_THRESHOLD = 0.63;

let questions = [];
let examQuestions = [];
let currentIndex = 0;
let answers = {};
let flagged = new Set();
let timerInterval = null;
let endTime = null;
let container = null;
let examStarted = false;

export function initExam(questionsData, targetContainer) {
  questions = questionsData;
  container = targetContainer;
  renderIntro();
}

function renderIntro() {
  container.innerHTML = `
    <div class="page-header">
      <h1><i class="fa-solid fa-clock" aria-hidden="true"></i> Simulateur d'examen</h1>
      <p>Conditions réelles de la certification Oracle Database SQL 1Z0-071</p>
    </div>
    <div class="exam-intro card">
      <i class="fa-solid fa-certificate" style="font-size:3rem;color:var(--primary);margin-bottom:1rem"></i>
      <h2>Examen blanc — 1Z0-071</h2>
      <ul class="exam-rules">
        <li><strong>${EXAM_SIZE} questions</strong> sélectionnées aléatoirement</li>
        <li><strong>120 minutes</strong> — chronomètre actif dès le début</li>
        <li>Score de passage : <strong>63%</strong> (${Math.ceil(EXAM_SIZE * PASS_THRESHOLD)} bonnes réponses minimum)</li>
        <li>Navigation libre entre les questions</li>
        <li>Marquage des questions pour révision</li>
        <li>Revue finale avant soumission</li>
      </ul>
      <button class="btn btn-primary btn-lg" id="exam-start">
        <i class="fa-solid fa-play"></i> Commencer l'examen
      </button>
    </div>
  `;
  document.getElementById('exam-start').addEventListener('click', startExam);
}

function startExam() {
  examQuestions = shuffle([...questions]).slice(0, EXAM_SIZE);
  currentIndex = 0;
  answers = {};
  flagged = new Set();
  examStarted = true;
  endTime = Date.now() + EXAM_DURATION_MS;
  renderExam();
  startTimer();
}

function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function startTimer() {
  if (timerInterval) clearInterval(timerInterval);
  timerInterval = setInterval(updateTimer, 1000);
  updateTimer();
}

function updateTimer() {
  const remaining = endTime - Date.now();
  const el = document.getElementById('exam-timer');
  if (!el) return;

  if (remaining <= 0) {
    clearInterval(timerInterval);
    submitExam(true);
    return;
  }

  const mins = Math.floor(remaining / 60000);
  const secs = Math.floor((remaining % 60000) / 1000);
  el.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  el.classList.toggle('warning', remaining < 30 * 60000);
  el.classList.toggle('critical', remaining < 10 * 60000);
}

function renderExam() {
  const q = examQuestions[currentIndex];
  const answeredCount = Object.keys(answers).length;

  container.innerHTML = `
    <div class="exam-header">
      <div>
        <strong>Examen 1Z0-071</strong>
        <span class="text-muted" style="color:rgba(255,255,255,0.7);margin-left:1rem">${answeredCount}/${EXAM_SIZE} répondues</span>
      </div>
      <div class="exam-timer" id="exam-timer" aria-live="polite">120:00</div>
    </div>

    <div class="exam-nav-grid" role="navigation" aria-label="Navigation questions">
      ${examQuestions.map((_, i) => `
        <button class="exam-nav-btn ${i === currentIndex ? 'current' : ''} ${answers[i] !== undefined ? 'answered' : ''} ${flagged.has(i) ? 'flagged' : ''}"
          data-index="${i}" aria-label="Question ${i + 1}${flagged.has(i) ? ', marquée' : ''}${answers[i] !== undefined ? ', répondue' : ''}">
          ${i + 1}
        </button>
      `).join('')}
    </div>

    <div class="card quiz-container">
      <div class="quiz-header">
        <span>Question ${currentIndex + 1} / ${EXAM_SIZE}</span>
        <span class="badge badge-primary">Module ${q.module}</span>
      </div>
      <div class="quiz-question">${escapeHtml(q.question)}</div>
      ${q.code ? `<div class="code-block"><pre><code class="language-sql">${escapeHtml(q.code)}</code></pre></div>` : ''}
      <ul class="quiz-options">
        ${q.options.map((opt, i) => `
          <li>
            <button class="quiz-option ${answers[currentIndex] === i ? 'correct' : ''}"
              data-index="${i}" style="${answers[currentIndex] === i ? 'border-color:var(--primary);background:rgba(231,76,60,0.08)' : ''}">
              ${escapeHtml(opt)}
            </button>
          </li>
        `).join('')}
      </ul>
    </div>

    <div class="exam-actions">
      <button class="btn btn-outline" id="exam-prev" ${currentIndex === 0 ? 'disabled' : ''}>
        <i class="fa-solid fa-chevron-left"></i> Précédent
      </button>
      <button class="btn btn-secondary" id="exam-flag">
        <i class="fa-solid fa-flag"></i> ${flagged.has(currentIndex) ? 'Retirer le marqueur' : 'Marquer'}
      </button>
      <button class="btn btn-outline" id="exam-next" ${currentIndex >= EXAM_SIZE - 1 ? 'disabled' : ''}>
        Suivant <i class="fa-solid fa-chevron-right"></i>
      </button>
      <button class="btn btn-primary" id="exam-submit">
        <i class="fa-solid fa-paper-plane"></i> Terminer l'examen
      </button>
    </div>
  `;

  container.querySelectorAll('.exam-nav-btn').forEach(btn => {
    btn.addEventListener('click', () => goToQuestion(parseInt(btn.dataset.index, 10)));
  });

  container.querySelectorAll('.quiz-option').forEach(btn => {
    btn.addEventListener('click', () => {
      answers[currentIndex] = parseInt(btn.dataset.index, 10);
      renderExam();
    });
  });

  document.getElementById('exam-prev')?.addEventListener('click', () => goToQuestion(currentIndex - 1));
  document.getElementById('exam-next')?.addEventListener('click', () => goToQuestion(currentIndex + 1));
  document.getElementById('exam-flag')?.addEventListener('click', toggleFlag);
  document.getElementById('exam-submit')?.addEventListener('click', () => confirmSubmit());

  if (window.hljs) {
    container.querySelectorAll('pre code').forEach(block => hljs.highlightElement(block));
  }
}

function goToQuestion(index) {
  if (index >= 0 && index < EXAM_SIZE) {
    currentIndex = index;
    renderExam();
  }
}

function toggleFlag() {
  if (flagged.has(currentIndex)) flagged.delete(currentIndex);
  else flagged.add(currentIndex);
  renderExam();
}

function confirmSubmit() {
  const unanswered = EXAM_SIZE - Object.keys(answers).length;
  const msg = unanswered > 0
    ? `Il reste ${unanswered} question(s) sans réponse. Voulez-vous vraiment terminer ?`
    : 'Confirmer la soumission de l\'examen ?';
  if (confirm(msg)) submitExam(false);
}

function submitExam(timedOut) {
  clearInterval(timerInterval);
  examStarted = false;

  let score = 0;
  examQuestions.forEach((q, i) => {
    if (answers[i] === q.correctIndex) score++;
  });

  const durationMinutes = Math.round((EXAM_DURATION_MS - Math.max(0, endTime - Date.now())) / 60000);
  saveExamAttempt(score, EXAM_SIZE, durationMinutes, answers);

  const percent = Math.round((score / EXAM_SIZE) * 100);
  const passed = score / EXAM_SIZE >= PASS_THRESHOLD;

  container.innerHTML = `
    <div class="exam-results card">
      <h2>${timedOut ? 'Temps écoulé !' : 'Examen terminé'}</h2>
      <div class="exam-score-circle ${passed ? 'pass' : 'fail'}">
        <span class="score">${score}/${EXAM_SIZE}</span>
        <span>${percent}%</span>
      </div>
      <p class="badge ${passed ? 'badge-success' : 'badge-primary'}" style="font-size:1rem;padding:0.5rem 1rem">
        ${passed ? 'RÉUSSI — Score ≥ 63%' : 'NON VALIDÉ — Continuez à vous entraîner'}
      </p>
      <p class="text-muted">Durée : ${durationMinutes} minutes | Seuil : ${Math.ceil(EXAM_SIZE * PASS_THRESHOLD)}/${EXAM_SIZE}</p>
      <button class="btn btn-primary" id="exam-review"><i class="fa-solid fa-list-check"></i> Revue des réponses</button>
      <button class="btn btn-outline" id="exam-restart"><i class="fa-solid fa-rotate-right"></i> Nouvel examen</button>
      <a href="#/progress" class="btn btn-secondary">Voir progression</a>
    </div>
    <div id="exam-review-area" class="hidden"></div>
  `;

  document.getElementById('exam-review').addEventListener('click', () => renderReview(score));
  document.getElementById('exam-restart').addEventListener('click', () => {
    renderIntro();
  });
}

function renderReview(score) {
  const area = document.getElementById('exam-review-area');
  area.classList.remove('hidden');
  area.innerHTML = `
    <h2 class="mt-2">Revue détaillée</h2>
    <div class="review-list">
      ${examQuestions.map((q, i) => {
        const userAnswer = answers[i];
        const isCorrect = userAnswer === q.correctIndex;
        return `
          <div class="review-item ${isCorrect ? 'correct' : 'incorrect'} card">
            <strong>Q${i + 1}.</strong> ${escapeHtml(q.question)}
            ${q.code ? `<div class="code-block"><pre><code class="language-sql">${escapeHtml(q.code)}</code></pre></div>` : ''}
            <p><strong>Votre réponse :</strong> ${userAnswer !== undefined ? escapeHtml(q.options[userAnswer]) : '<em>Non répondue</em>'}</p>
            ${!isCorrect ? `<p><strong>Bonne réponse :</strong> ${escapeHtml(q.options[q.correctIndex])}</p>` : ''}
            <p class="text-muted">${escapeHtml(q.explanation)}</p>
          </div>
        `;
      }).join('')}
    </div>
  `;
  if (window.hljs) {
    area.querySelectorAll('pre code').forEach(block => hljs.highlightElement(block));
  }
  area.scrollIntoView({ behavior: 'smooth' });
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

export function isExamActive() {
  return examStarted;
}
