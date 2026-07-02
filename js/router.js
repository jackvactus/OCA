const routes = {};

export function registerRoute(path, handler) {
  routes[path] = handler;
}

export function navigate(path) {
  window.location.hash = path.startsWith('/') ? path : `/${path}`;
}

export function getCurrentRoute() {
  const hash = window.location.hash.slice(1) || '/';
  const [path, query] = hash.split('?');
  const params = new URLSearchParams(query || '');
  return { path: path || '/', params };
}

export function initRouter(onRouteChange) {
  const handleRoute = () => {
    const { path, params } = getCurrentRoute();
    updateActiveNav(path);
    onRouteChange(path, params);
  };

  window.addEventListener('hashchange', handleRoute);
  handleRoute();
}

function updateActiveNav(path) {
  const basePath = path.split('/')[1] ? `/${path.split('/')[1]}` : '/';
  document.querySelectorAll('.nav-link').forEach(link => {
    const route = link.getAttribute('data-route');
    const linkPath = route === 'home' ? '/' : `/${route}`;
    link.classList.toggle('active', linkPath === basePath || (basePath.startsWith('/module') && route === 'modules'));
  });
}

export function parseModuleId(path) {
  const match = path.match(/^\/module\/(\d+)/);
  return match ? parseInt(match[1], 10) : null;
}
