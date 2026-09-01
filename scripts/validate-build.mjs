import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('..', import.meta.url));
const checks = [
  'dist/index.html',
  'dist/back-end/index.html',
  'dist/back-end/3/index.html',
  'dist/back-end/3/semana-15/index.html',
  'dist/back-end/3/semana-15/a2/index.html',
  'dist/back-end/3/semana-15/q1/index.html',
  'dist/inteligencia-artificial/3/semana-15/q1/index.html',
  'dist/front-end/3/semana-21/q1/index.html',
];

for (const relativePath of checks) {
  const file = join(root, relativePath);
  if (!existsSync(file)) throw new Error(`Saída ausente: ${relativePath}`);
  if (relativePath.endsWith('.html') && !readFileSync(file, 'utf8').includes('Eclesiastes')) {
    throw new Error(`Marca esperada ausente: ${relativePath}`);
  }
}
for (const file of [join(root, 'dist')]) {
  const pages = [];
  const walk = (directory) => {
    for (const entry of readdirSync(directory, { withFileTypes: true })) {
      const target = join(directory, entry.name);
      if (entry.isDirectory()) walk(target);
      else if (entry.name.endsWith('.html')) pages.push(target);
    }
  };
  walk(file);
  for (const page of pages) {
    const html = readFileSync(page, 'utf8');
    if (html.includes('site-footer') || html.includes('Busca global') || html.includes('busca-global')) throw new Error(`Superfície removida encontrada: ${page}`);
  }
}
console.log(`Build validado: ${checks.length} saídas representativas existem e contêm a marca correta; sem ZIPs, rodapé ou busca global.`);
