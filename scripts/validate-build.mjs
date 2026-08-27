import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('..', import.meta.url));
const checks = [
  'dist/index.html',
  'dist/back-end/index.html',
  'dist/back-end/3/index.html',
  'dist/back-end/3/semana-15/index.html',
  'dist/back-end/3/semana-15/a2/index.html',
  'dist/back-end/3/semana-15/q/index.html',
  'dist/programacao-mobile/3/semana-15/a2/index.html',
  'dist/versionamento-de-codigo/3/semana-20/q/index.html',
];

for (const relativePath of checks) {
  const file = join(root, relativePath);
  if (!existsSync(file)) throw new Error(`Página não gerada: ${relativePath}`);
  const html = readFileSync(file, 'utf8');
  if (!html.includes('Gabarito')) throw new Error(`Conteúdo esperado ausente: ${relativePath}`);
}
console.log(`Build validado: ${checks.length} páginas de referência existem e contêm a interface.`);
