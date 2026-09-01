export const FAVORITES_KEY = 'eclesiastes:favoritos:v1';
export const VISITS_KEY = 'eclesiastes:visitas:v1';

export function readSet(key: string) {
  try {
    const value = JSON.parse(localStorage.getItem(key) ?? '[]');
    return new Set(Array.isArray(value) && value.every((item) => typeof item === 'string') ? value : []);
  } catch {
    return new Set<string>();
  }
}

export function writeSet(key: string, values: Set<string>) {
  try {
    localStorage.setItem(key, JSON.stringify([...values]));
    return true;
  } catch {
    return false;
  }
}

export function weekProgress(paths: string[], visits: Set<string>) {
  const completed = paths.filter((path) => visits.has(path)).length;
  const total = paths.length;
  return { completed, total, percentage: total ? Math.round((completed / total) * 100) : 0 };
}
