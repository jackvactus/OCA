import { initRouter, parseModuleId } from './router.js';
import { getProgress, getStats, markModuleComplete, isModuleComplete, getGlobalProgressPercent, resetProgress, saveContactMessage, addModuleTime } from './progress.js';
import { initQuiz } from './quiz.js';
import { initExam } from './exam-simulator.js';
import { initI18n, t, getLocale, setLocale } from './i18n.js';

let modulesData = [];
let questionsData = [];
let sessionStart = Date.now();
let currentModuleId = null;

async function loadData() {
  const [modulesRes, questionsRes] = await Promise.all([
    fetch('data/modules.json'),
    fetch('data/questions.json')
  ]);
  const modulesJson = await modulesRes.json();
  const questionsJson = await questionsRes.json();
  modulesData = modulesJson.modules;
  questionsData = questionsJson.questions;
}

function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<i class="fa-solid fa-${type === 'success' ? 'check' : type === 'error' ? 'xmark' : 'info-circle'}"></i> ${message}`;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 4000);
}

function updateGlobalProgress() {
  const percent = getGlobalProgressPercent(modulesData.length);
  const fill = document.getElementById('global-progress-fill');
  const bar = document.querySelector('.global-progress-bar');
  if (fill) fill.style.width = `${percent}%`;
  if (bar) bar.setAttribute('aria-valuenow', percent);
}

function getCurrentRoute() {
  return window.location.hash.slice(1) || '/';
}

function refreshStaticTexts() {
  document.title = t('head.title');
  const descriptionMeta = document.querySelector('meta[name="description"]');
  if (descriptionMeta) descriptionMeta.setAttribute('content', t('head.description'));
  document.querySelector('.skip-link')?.textContent = t('skipLink');
  document.querySelector('.logo')?.setAttribute('aria-label', t('nav.logoAria'));

  const routeKeyMap = {
    home: 'nav.home',
    modules: 'nav.courses',
    quiz: 'nav.quiz',
    exam: 'nav.exam',
    progress: 'nav.progress',
    resources: 'nav.resources',
    about: 'nav.about'
  };

  document.querySelectorAll('#main-nav a[data-route]').forEach(link => {
    const route = link.dataset.route;
    const icon = link.querySelector('i');
    if (routeKeyMap[route]) {
      link.innerHTML = `${icon?.outerHTML || ''} ${t(routeKeyMap[route])}`;
    }
  });

  const toggle = document.getElementById('locale-toggle');
  if (toggle) {
    toggle.textContent = t('nav.switchLocale');
    toggle.setAttribute('aria-label', t('nav.switchLocaleAria'));
  }

  const footerCopy = document.querySelector('.footer-inner p:first-child');
  if (footerCopy) footerCopy.textContent = t('footer.copy');
  const footerNote = document.querySelector('.footer-note');
  if (footerNote) footerNote.textContent = t('footer.note');
  document.getElementById('modal-close')?.setAttribute('aria-label', t('modal.close'));
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

function getSectionHighlights(section) {
  const lines = (section.content || '')
    .split('\n')
    .map(line => line.trim())
    .filter(Boolean)
    .slice(0, 3);

  if (!lines.length) {
    return [t('module.highlightFallback')];
  }

  return lines.map(line => line.replace(/\s+/g, ' ').slice(0, 140));
}

function getSectionExpertTip(section, moduleTitle) {
  if (section.pitfalls?.length) {
    return t('module.avoidPitfall', { pitfall: section.pitfalls[0] });
  }

  return t('module.expertTip', { moduleTitle: moduleTitle.toLowerCase() });
}

function renderCodeBlock(code, result) {
  const id = 'code-' + Math.random().toString(36).slice(2, 8);
  return `
    <div class="code-block">
      <div class="code-toolbar">
        <button type="button" class="copy-btn" data-target="${id}" aria-label="${t('code.copyAria')}">
          <i class="fa-solid fa-copy"></i> ${t('code.copy')}
        </button>
        ${result ? `<button type="button" class="run-btn" data-result="${escapeHtml(result)}" aria-label="${t('code.resultAria')}">
          <i class="fa-solid fa-play"></i> ${t('code.result')}
        </button>` : ''}
      </div>
      <pre id="${id}"><code class="language-sql">${escapeHtml(code)}</code></pre>
      <div class="code-result hidden" role="region" aria-label="${t('code.resultAria')}"></div>
    </div>
  `;
}

function initCodeBlocks(container) {
  container.querySelectorAll('.copy-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      const pre = document.getElementById(btn.dataset.target);
      const code = pre?.textContent || '';
      try {
        await navigator.clipboard.writeText(code);
        showToast(t('code.copySuccess'), 'success');
      } catch {
        showToast(t('code.copyError'), 'error');
      }
    });
  });
  container.querySelectorAll('.run-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const block = btn.closest('.code-block');
      const resultEl = block.querySelector('.code-result');
      resultEl.textContent = btn.dataset.result;
      resultEl.classList.toggle('hidden');
    });
  });
  if (window.hljs) {
    container.querySelectorAll('pre code').forEach(block => hljs.highlightElement(block));
  }
}

function initAccordions(container) {
  container.querySelectorAll('.accordion-header').forEach(header => {
    header.addEventListener('click', () => {
      const expanded = header.getAttribute('aria-expanded') === 'true';
      const body = header.nextElementSibling;
      header.setAttribute('aria-expanded', !expanded);
      body.classList.toggle('open', !expanded);
    });
  });
}

function initTabs(container) {
  container.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const tabId = btn.dataset.tab;
      container.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      container.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      container.querySelector(`#${tabId}`)?.classList.add('active');
    });
  });
}

function initRevealEffects(container) {
  if (!container || typeof IntersectionObserver === 'undefined') return;
  const elements = container.querySelectorAll('[data-reveal]');
  if (!elements.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });

  elements.forEach(el => observer.observe(el));
}

function renderHome() {
  const stats = getStats(modulesData.length, questionsData.length);
  const main = document.getElementById('main-content');
  main.innerHTML = `
    <section class="hero" aria-labelledby="hero-title" data-reveal>
      <span class="badge">${t('home.heroBadge')}</span>
      <h1 id="hero-title">${t('home.heroTitle')}</h1>
      <p>${t('home.heroDescription')}</p>
      <div class="hero-actions">
        <a href="#/modules" class="btn btn-primary"><i class="fa-solid fa-book-open"></i> ${t('home.heroStartCourses')}</a>
        <a href="#/exam" class="btn btn-outline" style="border-color:#fff;color:#fff"><i class="fa-solid fa-clock"></i> ${t('home.heroStartExam')}</a>
      </div>
      <div class="hero-metrics">
        <div class="metric-pill"><span>63</span><small>${t('home.heroMetricQuestions')}</small></div>
        <div class="metric-pill"><span>120</span><small>${t('home.heroMetricMinutes')}</small></div>
        <div class="metric-pill"><span>63%</span><small>${t('home.heroMetricThreshold')}</small></div>
      </div>
    </section>

    <div class="card-grid mb-2">
      <div class="card stat-card" data-reveal>
        <div class="stat-value">${stats.modulesCompleted}/${stats.totalModules}</div>
        <div class="stat-label">${t('home.statsCompleted')}</div>
      </div>
      <div class="card stat-card" data-reveal>
        <div class="stat-value">${stats.globalPercent}%</div>
        <div class="stat-label">${t('home.statsProgress')}</div>
      </div>
      <div class="card stat-card" data-reveal>
        <div class="stat-value">${stats.avgQuizScore || '—'}${stats.avgQuizScore ? '%' : ''}</div>
        <div class="stat-label">${t('home.statsScore')}</div>
      </div>
      <div class="card stat-card" data-reveal>
        <div class="stat-value">${questionsData.length}</div>
        <div class="stat-label">${t('home.statsQuestions')}</div>
      </div>
    </div>

    <section class="intro-grid">
      <article class="card spotlight-card" data-reveal>
        <div class="card-icon"><i class="fa-solid fa-graduation-cap"></i></div>
        <h2>${t('home.introHeading')}</h2>
        <p>${t('home.introDescription')}</p>
        <ul class="check-list">
          <li>${t('home.introItem1')}</li>
          <li>${t('home.introItem2')}</li>
          <li>${t('home.introItem3')}</li>
        </ul>
      </article>
      <article class="card exam-card" data-reveal>
        <h3>${t('home.examInfoHeading')}</h3>
        <div class="exam-info-grid">
          <div class="info-tile"><span>63</span><small>${t('home.heroMetricQuestions')}</small></div>
          <div class="info-tile"><span>120</span><small>${t('home.heroMetricMinutes')}</small></div>
          <div class="info-tile"><span>63%</span><small>${t('home.heroMetricThreshold')}</small></div>
          <div class="info-tile"><span>19c</span><small>Oracle</small></div>
        </div>
        <p class="text-muted">${t('home.examInfoText')}</p>
        <a href="#/exam" class="btn btn-outline"><i class="fa-solid fa-play"></i> ${t('home.examButton')}</a>
      </article>
    </section>

    <section class="card" data-reveal>
      <div class="section-heading">
        <h2>${t('home.planHeading')}</h2>
        <p>${t('home.planDescription')}</p>
      </div>
      <div class="timeline">
        <div class="timeline-step">
          <strong>${t('home.planStep1Title')}</strong>
          <p>${t('home.planStep1Desc')}</p>
        </div>
        <div class="timeline-step">
          <strong>${t('home.planStep2Title')}</strong>
          <p>${t('home.planStep2Desc')}</p>
        </div>
        <div class="timeline-step">
          <strong>${t('home.planStep3Title')}</strong>
          <p>${t('home.planStep3Desc')}</p>
        </div>
      </div>
    </section>

    <h2>${t('home.modulesHeading')}</h2>
    <div class="card-grid">
      ${modulesData.map(m => `
        <article class="card module-card ${isModuleComplete(m.id) ? 'completed' : ''}" data-module="${m.id}" tabindex="0" role="button" aria-label="Module ${m.id}: ${escapeHtml(m.title)}" data-reveal>
          <span class="module-num">${m.id}</span>
          <h3>${escapeHtml(m.title)}</h3>
          <p class="text-muted">${escapeHtml(m.summary)}</p>
          <span class="badge ${isModuleComplete(m.id) ? 'badge-success' : 'badge-primary'}">
            ${isModuleComplete(m.id) ? t('home.completedBadge') : t('home.studyBadge')}
          </span>
        </article>
      `).join('')}
    </div>
  `;

  main.querySelectorAll('.module-card').forEach(card => {
    const go = () => { window.location.hash = `/module/${card.dataset.module}`; };
    card.addEventListener('click', go);
    card.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); }
    });
  });
  initRevealEffects(main);
}

function renderModulesList() {
  const main = document.getElementById('main-content');
  main.innerHTML = `
    <div class="page-header">
      <h1><i class="fa-solid fa-book" aria-hidden="true"></i> ${t('modules.pageHeaderTitle')}</h1>
      <p>${t('modules.pageHeaderSubtitle')}</p>
    </div>
    <div class="card-grid">
      ${modulesData.map(m => `
        <a href="#/module/${m.id}" class="card module-card ${isModuleComplete(m.id) ? 'completed' : ''}" style="text-decoration:none;color:inherit">
          <span class="module-num">${m.id}</span>
          <h3>${escapeHtml(m.title)}</h3>
          <p class="text-muted">${escapeHtml(m.summary)}</p>
          <p><span class="badge badge-primary">${m.sections.length} sections</span></p>
        </a>
      `).join('')}
    </div>
  `;
}

function renderModuleDetail(moduleId) {
  const mod = modulesData.find(m => m.id === moduleId);
  if (!mod) { renderModulesList(); return; }

  currentModuleId = moduleId;
  sessionStart = Date.now();

  const main = document.getElementById('main-content');
  main.innerHTML = `
    <div class="module-layout">
      <aside class="module-sidebar" aria-label="Navigation modules">
        <h3>Modules</h3>
        <ul class="module-nav-list">
          ${modulesData.map(m => `
            <li><a href="#/module/${m.id}" class="${m.id === moduleId ? 'active' : ''} ${isModuleComplete(m.id) ? 'completed' : ''}">
              ${m.id}. ${escapeHtml(m.title)}
            </a></li>
          `).join('')}
        </ul>
      </aside>
      <article class="module-content">
        <div class="page-header">
          <span class="badge badge-primary">Module ${mod.id}</span>
          <h1>${escapeHtml(mod.title)}</h1>
          <p>${escapeHtml(mod.summary)}</p>
        </div>

        <div class="module-summary-grid">
          <div class="summary-card">
            <h4><i class="fa-solid fa-chess-knight"></i> Ce que vous allez maîtriser</h4>
            <p>${escapeHtml(mod.summary)}</p>
          </div>
          <div class="summary-card">
            <h4><i class="fa-solid fa-lightbulb"></i> Conseils d’expert</h4>
            <p>Travaillez chaque section en trois temps : compréhension, application et correction des erreurs fréquentes.</p>
          </div>
        </div>

        ${mod.objectives ? `
          <div class="tip-box">
            <h4><i class="fa-solid fa-bullseye"></i> Objectifs pédagogiques</h4>
            <ul>${mod.objectives.map(o => `<li>${escapeHtml(o)}</li>`).join('')}</ul>
          </div>
        ` : ''}

        <div class="accordion" role="region" aria-label="Sections du module">
          ${mod.sections.map((sec, i) => {
            const highlights = getSectionHighlights(sec);
            const expertTip = getSectionExpertTip(sec, mod.title);
            return `
              <div class="accordion-item">
                <button class="accordion-header" aria-expanded="${i === 0}" aria-controls="sec-${moduleId}-${i}">
                  ${escapeHtml(sec.title)}
                  <i class="fa-solid fa-chevron-down accordion-icon" aria-hidden="true"></i>
                </button>
                <div class="accordion-body ${i === 0 ? 'open' : ''}" id="sec-${moduleId}-${i}">
                  ${sec.content.split('\n').map(p => p.trim() ? `<p>${p}</p>` : '').join('')}
                  <div class="section-explainer">
                    <div class="section-highlight-block">
                      <h5><i class="fa-solid fa-star"></i> ${t('module.keyPoints')}</h5>
                      <ul>${highlights.map(h => `<li>${escapeHtml(h)}</li>`).join('')}</ul>
                    </div>
                    <div class="section-highlight-block accent">
                      <h5><i class="fa-solid fa-wand-magic-sparkles"></i> ${t('module.takeaway')}</h5>
                      <p>${escapeHtml(expertTip)}</p>
                    </div>
                  </div>
                  ${sec.code ? renderCodeBlock(sec.code, sec.result) : ''}
                  ${sec.pitfalls?.length ? `
                    <div class="pitfall-box">
                      <h4><i class="fa-solid fa-triangle-exclamation"></i> Pièges examen</h4>
                      <ul>${sec.pitfalls.map(p => `<li>${escapeHtml(p)}</li>`).join('')}</ul>
                    </div>
                  ` : ''}
                </div>
              </div>
            `;
          }).join('')}
        </div>

        <div class="mt-2" style="display:flex;gap:1rem;flex-wrap:wrap">
          <button class="btn btn-primary" id="mark-complete">
            <i class="fa-solid fa-check"></i> ${isModuleComplete(moduleId) ? t('module.completed') : t('module.markComplete')}
          </button>
          <a href="#/quiz" class="btn btn-outline"><i class="fa-solid fa-circle-question"></i> ${t('module.quizButton')}</a>
        </div>
      </article>
    </div>
  `;

  initAccordions(main);
  initCodeBlocks(main);
  initRevealEffects(main);

  document.getElementById('mark-complete')?.addEventListener('click', () => {
    markModuleComplete(moduleId);
    const mins = Math.round((Date.now() - sessionStart) / 60000) || 1;
    addModuleTime(moduleId, mins);
    updateGlobalProgress();
    showToast(t('module.markedCompleteToast'), 'success');
    renderModuleDetail(moduleId);
  });
}

function renderQuiz() {
  const main = document.getElementById('main-content');
  initQuiz(questionsData, main, () => updateGlobalProgress());
}

function renderExam() {
  const main = document.getElementById('main-content');
  initExam(questionsData, main);
}

function renderProgress() {
  const progress = getProgress();
  const stats = getStats(modulesData.length, questionsData.length);
  const main = document.getElementById('main-content');

  main.innerHTML = `
    <div class="page-header">
      <h1><i class="fa-solid fa-chart-line" aria-hidden="true"></i> ${t('progress.pageHeaderTitle')}</h1>
      <p>${t('progress.pageHeaderSubtitle')}</p>
    </div>

    <div class="progress-grid">
      <div class="card stat-card">
        <div class="stat-value">${stats.globalPercent}%</div>
        <div class="stat-label">${t('progress.globalLabel')}</div>
        <div class="progress-bar-inline"><div class="progress-bar-inline-fill" style="width:${stats.globalPercent}%"></div></div>
      </div>
      <div class="card stat-card">
        <div class="stat-value">${stats.modulesCompleted}</div>
        <div class="stat-label">${t('progress.modulesCompletedLabel')}</div>
      </div>
      <div class="card stat-card">
        <div class="stat-value">${stats.quizAttempts}</div>
        <div class="stat-label">${t('progress.quizPassedLabel')}</div>
      </div>
      <div class="card stat-card">
        <div class="stat-value">${stats.examAttempts}</div>
        <div class="stat-label">${t('progress.examAttemptsLabel')}</div>
      </div>
      <div class="card stat-card">
        <div class="stat-value">${stats.totalTimeMinutes}</div>
        <div class="stat-label">${t('progress.timeMinutesLabel')}</div>
      </div>
      <div class="card stat-card">
        <div class="stat-value">${stats.lastExamScore !== null ? stats.lastExamScore + '%' : '—'}</div>
        <div class="stat-label">${t('progress.lastExamLabel')}</div>
      </div>
    </div>

    <div class="card chart-placeholder">
      <h2>${t('progress.detailByModule')}</h2>
      <ul class="module-progress-list">
        ${modulesData.map(m => {
          const done = isModuleComplete(m.id);
          const quiz = progress.quizScores[m.id];
          const time = progress.moduleTime[m.id] || 0;
          return `
            <li class="module-progress-item">
              <span class="module-num" style="margin:0">${m.id}</span>
              <div style="flex:1">
                <strong>${escapeHtml(m.title)}</strong>
                <div class="progress-bar-inline">
                  <div class="progress-bar-inline-fill" style="width:${done ? 100 : 0}%"></div>
                </div>
                <small class="text-muted">${time} ${t('progress.timeMinutesLabel').toLowerCase()} | ${t('progress.quizLabel')}: ${quiz ? quiz.percent + '%' : '—'}</small>
              </div>
              <span class="badge ${done ? 'badge-success' : 'badge-primary'}">${done ? t('progress.statusDone') : t('progress.statusInProgress')}</span>
            </li>
          `;
        }).join('')}
      </ul>
    </div>

    ${progress.examAttempts.length ? `
      <div class="card mt-2">
        <h2>${t('progress.examHistoryHeading')}</h2>
        <table class="data-table">
          <thead><tr><th>${t('progress.tableDate')}</th><th>${t('progress.tableScore')}</th><th>${t('progress.tableDuration')}</th><th>${t('progress.tableResult')}</th></tr></thead>
          <tbody>
            ${progress.examAttempts.slice().reverse().map(e => `
              <tr>
                <td>${new Date(e.date).toLocaleDateString(getLocale())}</td>
                <td>${e.score}/${e.total} (${e.percent}%)</td>
                <td>${e.durationMinutes} ${t('progress.timeMinutesLabel').toLowerCase()}</td>
                <td><span class="badge ${e.passed ? 'badge-success' : 'badge-primary'}">${e.passed ? t('progress.passed') : t('progress.failed')}</span></td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    ` : ''}

    <button class="btn btn-outline mt-2" id="reset-progress" style="color:var(--error);border-color:var(--error)">
      <i class="fa-solid fa-trash"></i> ${t('progress.resetButton')}
    </button>
  `;

  document.getElementById('reset-progress')?.addEventListener('click', () => {
    if (confirm(t('progress.resetPrompt'))) {
      resetProgress();
      updateGlobalProgress();
      showToast(t('progress.resetToast'), 'info');
      renderProgress();
    }
  });
}

function renderResources() {
  const main = document.getElementById('main-content');
  main.innerHTML = `
    <div class="page-header">
      <h1><i class="fa-solid fa-download" aria-hidden="true"></i> ${t('resources.pageHeaderTitle')}</h1>
      <p>${t('resources.pageHeaderSubtitle')}</p>
    </div>

    <div class="tabs">
      <ul class="tab-list" role="tablist">
        <li><button class="tab-btn active" data-tab="tab-scripts" role="tab">${t('resources.tabScripts')}</button></li>
        <li><button class="tab-btn" data-tab="tab-cheatsheets" role="tab">${t('resources.tabCheatsheets')}</button></li>
        <li><button class="tab-btn" data-tab="tab-links" role="tab">${t('resources.tabLinks')}</button></li>
      </ul>

      <div id="tab-scripts" class="tab-panel active" role="tabpanel">
        <ul class="resource-list">
          <li class="resource-item">
            <div class="resource-item-info">
              <i class="fa-solid fa-file-code" aria-hidden="true"></i>
              <div>
                <strong>${t('resources.scriptsTitle')}</strong>
                <p class="text-muted">${t('resources.scriptsDescription')}</p>
              </div>
            </div>
            <a href="assets/resources/hr_schema.sql" download class="btn btn-primary btn-sm"><i class="fa-solid fa-download"></i> ${t('resources.downloadButton')}</a>
          </li>
          <li class="resource-item">
            <div class="resource-item-info">
              <i class="fa-solid fa-file-code" aria-hidden="true"></i>
              <div>
                <strong>${t('resources.dataTitle')}</strong>
                <p class="text-muted">${t('resources.dataDescription')}</p>
              </div>
            </div>
            <a href="assets/resources/hr_data.sql" download class="btn btn-primary btn-sm"><i class="fa-solid fa-download"></i> ${t('resources.downloadButton')}</a>
          </li>
          <li class="resource-item">
            <div class="resource-item-info">
              <i class="fa-solid fa-file-code" aria-hidden="true"></i>
              <div>
                <strong>${t('resources.practiceTitle')}</strong>
                <p class="text-muted">${t('resources.practiceDescription')}</p>
              </div>
            </div>
            <a href="assets/resources/practice_queries.sql" download class="btn btn-primary btn-sm"><i class="fa-solid fa-download"></i> ${t('resources.downloadButton')}</a>
          </li>
        </ul>
      </div>

      <div id="tab-cheatsheets" class="tab-panel" role="tabpanel">
        <div class="card">
          <h3>${t('resources.cheatsheetsTitle')}</h3>
          <table class="data-table">
            <thead><tr><th>${t('resources.category')}</th><th>${t('resources.functions')}</th></tr></thead>
            <tbody>
              <tr><td>${t('resources.categoryText')}</td><td>UPPER, LOWER, INITCAP, SUBSTR, INSTR, LENGTH, TRIM, LPAD, RPAD, CONCAT, REPLACE</td></tr>
              <tr><td>${t('resources.categoryNumeric')}</td><td>ROUND, TRUNC, MOD, CEIL, FLOOR, POWER, SQRT</td></tr>
              <tr><td>${t('resources.categoryDate')}</td><td>SYSDATE, ADD_MONTHS, MONTHS_BETWEEN, NEXT_DAY, LAST_DAY, EXTRACT</td></tr>
              <tr><td>${t('resources.categoryConversion')}</td><td>TO_CHAR, TO_DATE, TO_NUMBER, CAST</td></tr>
              <tr><td>${t('resources.categoryGeneral')}</td><td>NVL, NVL2, NULLIF, COALESCE, DECODE, CASE</td></tr>
              <tr><td>${t('resources.categoryAggregate')}</td><td>COUNT, SUM, AVG, MIN, MAX, GROUP BY, HAVING</td></tr>
              <tr><td>${t('resources.categoryAnalytics')}</td><td>ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, FIRST_VALUE, LAST_VALUE</td></tr>
            </tbody>
          </table>
        </div>
        <div class="card">
          <h3>${t('resources.joinsTitle')}</h3>
          <table class="data-table">
            <thead><tr><th>${t('resources.type')}</th><th>${t('resources.syntaxAnsi')}</th><th>${t('resources.syntaxOracle')}</th></tr></thead>
            <tbody>
              <tr><td>${t('resources.leftOuter')}</td><td>LEFT OUTER JOIN</td><td>(+) ${t('resources.rightTable')}</td></tr>
              <tr><td>${t('resources.rightOuter')}</td><td>RIGHT OUTER JOIN</td><td>(+) ${t('resources.leftTable')}</td></tr>
              <tr><td>${t('resources.fullOuter')}</td><td>FULL OUTER JOIN</td><td>${t('resources.noPlusEquivalent')}</td></tr>
            </tbody>
          </table>
        </div>
        <div class="pitfall-box">
          <h4><i class="fa-solid fa-triangle-exclamation"></i> ${t('resources.warningsTitle')}</h4>
          <ul>
            <li>${t('resources.warn1')}</li>
            <li>${t('resources.warn2')}</li>
            <li>${t('resources.warn3')}</li>
            <li>${t('resources.warn4')}</li>
            <li>${t('resources.warn5')}</li>
          </ul>
        </div>
      </div>

      <div id="tab-links" class="tab-panel" role="tabpanel">
        <ul class="resource-list">
          <li class="resource-item">
            <div class="resource-item-info">
              <i class="fa-solid fa-link" aria-hidden="true"></i>
              <div><strong>${t('resources.link1Title')}</strong><p class="text-muted">${t('resources.link1Desc')}</p></div>
            </div>
            <a href="https://education.oracle.com/oracle-database-sql/pexam_1Z0-071" target="_blank" rel="noopener" class="btn btn-outline btn-sm">${t('button.visit')}</a>
          </li>
          <li class="resource-item">
            <div class="resource-item-info">
              <i class="fa-solid fa-link" aria-hidden="true"></i>
              <div><strong>${t('resources.link2Title')}</strong><p class="text-muted">${t('resources.link2Desc')}</p></div>
            </div>
            <a href="https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/" target="_blank" rel="noopener" class="btn btn-outline btn-sm">${t('button.visit')}</a>
          </li>
          <li class="resource-item">
            <div class="resource-item-info">
              <i class="fa-solid fa-link" aria-hidden="true"></i>
              <div><strong>${t('resources.link3Title')}</strong><p class="text-muted">${t('resources.link3Desc')}</p></div>
            </div>
            <a href="https://livesql.oracle.com/" target="_blank" rel="noopener" class="btn btn-outline btn-sm">${t('button.visit')}</a>
          </li>
        </ul>
      </div>
    </div>
  `;
  initTabs(main);
}

function renderAbout() {
  const main = document.getElementById('main-content');
  main.innerHTML = `
    <div class="page-header">
      <h1><i class="fa-solid fa-circle-info" aria-hidden="true"></i> ${t('about.pageHeaderTitle')}</h1>
      <p>${t('about.pageHeaderSubtitle')}</p>
    </div>

    <section class="intro-grid">
      <div class="card spotlight-card" data-reveal>
        <div class="card-icon"><i class="fa-solid fa-lightbulb"></i></div>
        <h2>${t('about.whyTitle')}</h2>
        <p>${t('about.whyDesc')}</p>
        <ul class="check-list">
          <li>${t('about.benefit1')}</li>
          <li>${t('about.benefit2')}</li>
          <li>${t('about.benefit3')}</li>
        </ul>
      </div>
      <div class="card exam-card" data-reveal>
        <h3>${t('about.examSummaryTitle')}</h3>
        <div class="exam-info-grid">
          <div class="info-tile"><span>1Z0-071</span><small>${t('about.codeLabel')}</small></div>
          <div class="info-tile"><span>245 $</span><small>${t('about.costLabel')}</small></div>
          <div class="info-tile"><span>19c</span><small>${t('about.versionLabel')}</small></div>
          <div class="info-tile"><span>Associate</span><small>${t('about.certificationLabel')}</small></div>
        </div>
        <p class="text-muted">${t('about.examSummaryText')}</p>
      </div>
    </section>

    <div class="card" data-reveal>
      <h2>${t('about.faqHeading')}</h2>
      <div class="accordion">
        ${[
          { q: t('about.faq1'), a: t('about.faq1Answer') },
          { q: t('about.faq2'), a: t('about.faq2Answer') },
          { q: t('about.faq3'), a: t('about.faq3Answer') },
          { q: t('about.faq4'), a: t('about.faq4Answer') },
          { q: t('about.faq5'), a: t('about.faq5Answer') }
        ].map((f, i) => `
          <div class="accordion-item faq-item">
            <button class="accordion-header" aria-expanded="false" aria-controls="faq-${i}">
              ${escapeHtml(f.q)}
              <i class="fa-solid fa-chevron-down accordion-icon"></i>
            </button>
            <div class="accordion-body" id="faq-${i}"><p>${escapeHtml(f.a)}</p></div>
          </div>
        `).join('')}
      </div>
    </div>

    <div class="card contact-form" data-reveal>
      <h2>${t('contact.title')}</h2>
      <form id="contact-form" novalidate>
        <div class="form-group">
          <label for="contact-name">${t('contact.name')}</label>
          <input type="text" id="contact-name" required autocomplete="name">
        </div>
        <div class="form-group">
          <label for="contact-email">${t('contact.email')}</label>
          <input type="email" id="contact-email" required autocomplete="email">
        </div>
        <div class="form-group">
          <label for="contact-subject">${t('contact.subject')}</label>
          <select id="contact-subject">
            <option value="question">${t('contact.subjectQuestion')}</option>
            <option value="bug">${t('contact.subjectBug')}</option>
            <option value="suggestion">${t('contact.subjectSuggestion')}</option>
            <option value="other">${t('contact.subjectOther')}</option>
          </select>
        </div>
        <div class="form-group">
          <label for="contact-message">${t('contact.message')}</label>
          <textarea id="contact-message" rows="5" required></textarea>
        </div>
        <button type="submit" class="btn btn-primary"><i class="fa-solid fa-paper-plane"></i> ${t('contact.send')}</button>
      </form>
    </div>
  `;

  initAccordions(main);
  initRevealEffects(main);
  document.getElementById('contact-form')?.addEventListener('submit', e => {
    e.preventDefault();
    const name = document.getElementById('contact-name').value.trim();
    const email = document.getElementById('contact-email').value.trim();
    const subject = document.getElementById('contact-subject').value;
    const message = document.getElementById('contact-message').value.trim();
    if (!name || !email || !message) {
      showToast(t('contact.fillFields'), 'error');
      return;
    }
    saveContactMessage({ name, email, subject, message });
    showToast(t('contact.thanks'), 'success');
    e.target.reset();
  });
}

function handleRoute(path) {
  const moduleId = parseModuleId(path);

  if (moduleId) {
    renderModuleDetail(moduleId);
  } else if (path === '/' || path === '/home') {
    renderHome();
  } else if (path === '/modules') {
    renderModulesList();
  } else if (path === '/quiz') {
    renderQuiz();
  } else if (path === '/exam') {
    renderExam();
  } else if (path === '/progress') {
    renderProgress();
  } else if (path === '/resources') {
    renderResources();
  } else if (path === '/about') {
    renderAbout();
  } else {
    renderHome();
  }

  document.getElementById('main-content')?.focus();
  updateGlobalProgress();
  refreshStaticTexts();
}

function initNav() {
  const toggle = document.getElementById('nav-toggle');
  const nav = document.getElementById('main-nav');
  toggle?.setAttribute('aria-label', t('nav.openMenu'));
  toggle?.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open);
    toggle.setAttribute('aria-label', open ? t('nav.closeMenu') : t('nav.openMenu'));
  });
  nav?.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => nav.classList.remove('open'));
  });

  const localeToggle = document.getElementById('locale-toggle');
  localeToggle?.addEventListener('click', () => {
    const nextLocale = getLocale() === 'en' ? 'fr' : 'en';
    setLocale(nextLocale);
    refreshStaticTexts();
    handleRoute(getCurrentRoute());
  });

  document.getElementById('modal-close')?.addEventListener('click', () => {
    document.getElementById('modal-overlay').classList.add('hidden');
  });
}

async function init() {
  try {
    initI18n();
    await loadData();
    initNav();
    refreshStaticTexts();
    initRouter(handleRoute);
    updateGlobalProgress();
  } catch (err) {
    document.getElementById('main-content').innerHTML = `
      <div class="card">
        <h2>${t('error.loadingTitle')}</h2>
        <p>${t('error.loadingMessage')}</p>
        <p class="text-muted">${escapeHtml(err.message)}</p>
      </div>
    `;
  }
}

init();
