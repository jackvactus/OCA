const STORAGE_KEY = 'oracle_1z0_071_progress';

const defaultProgress = () => ({
  modulesCompleted: [],
  moduleTime: {},
  quizScores: {},
  quizAttempts: [],
  examAttempts: [],
  totalTimeMinutes: 0,
  lastVisit: null,
  contactMessages: []
});

export function getProgress() {
  try {
    const data = localStorage.getItem(STORAGE_KEY);
    if (!data) return defaultProgress();
    return { ...defaultProgress(), ...JSON.parse(data) };
  } catch {
    return defaultProgress();
  }
}

export function saveProgress(progress) {
  progress.lastVisit = new Date().toISOString();
  localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
}

export function markModuleComplete(moduleId) {
  const progress = getProgress();
  if (!progress.modulesCompleted.includes(moduleId)) {
    progress.modulesCompleted.push(moduleId);
    saveProgress(progress);
  }
  return progress;
}

export function isModuleComplete(moduleId) {
  return getProgress().modulesCompleted.includes(moduleId);
}

export function addModuleTime(moduleId, minutes) {
  const progress = getProgress();
  progress.moduleTime[moduleId] = (progress.moduleTime[moduleId] || 0) + minutes;
  progress.totalTimeMinutes = (progress.totalTimeMinutes || 0) + minutes;
  saveProgress(progress);
}

export function saveQuizScore(moduleId, score, total) {
  const progress = getProgress();
  const entry = { moduleId, score, total, date: new Date().toISOString(), percent: Math.round((score / total) * 100) };
  progress.quizAttempts.push(entry);
  const prev = progress.quizScores[moduleId];
  if (!prev || entry.percent > prev.percent) {
    progress.quizScores[moduleId] = entry;
  }
  saveProgress(progress);
  return entry;
}

export function saveExamAttempt(score, total, durationMinutes, answers) {
  const progress = getProgress();
  const entry = {
    score, total,
    percent: Math.round((score / total) * 100),
    durationMinutes,
    date: new Date().toISOString(),
    passed: score / total >= 0.63
  };
  progress.examAttempts.push(entry);
  saveProgress(progress);
  return entry;
}

export function getGlobalProgressPercent(totalModules) {
  const completed = getProgress().modulesCompleted.length;
  return totalModules ? Math.round((completed / totalModules) * 100) : 0;
}

export function resetProgress() {
  localStorage.removeItem(STORAGE_KEY);
}

export function saveContactMessage(message) {
  const progress = getProgress();
  progress.contactMessages.push({ ...message, date: new Date().toISOString() });
  saveProgress(progress);
}

export function getStats(totalModules, totalQuestions) {
  const p = getProgress();
  const quizScores = Object.values(p.quizScores);
  const avgQuiz = quizScores.length
    ? Math.round(quizScores.reduce((s, q) => s + q.percent, 0) / quizScores.length)
    : 0;
  const lastExam = p.examAttempts.length ? p.examAttempts[p.examAttempts.length - 1] : null;
  return {
    modulesCompleted: p.modulesCompleted.length,
    totalModules,
    globalPercent: getGlobalProgressPercent(totalModules),
    avgQuizScore: avgQuiz,
    quizAttempts: p.quizAttempts.length,
    examAttempts: p.examAttempts.length,
    lastExamScore: lastExam ? lastExam.percent : null,
    totalTimeMinutes: p.totalTimeMinutes || 0,
    totalQuestions
  };
}
