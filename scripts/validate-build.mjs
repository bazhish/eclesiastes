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
  'dist/back-end/3/semana-15/q1/index.html',
  'dist/inteligencia-artificial/3/semana-15/q1/index.html',
  'dist/front-end/3/semana-21/q1/index.html',
  'dist/artefatos/back-end/semana-15/a2.zip',
];

for (const relativePath of checks) {
  const file = join(root, relativePath);
  if (!existsSync(file)) throw new Error(`Saída ausente: ${relativePath}`);
  if (relativePath.endsWith('.html') && !readFileSync(file, 'utf8').includes('Eclesiastes')) {
    throw new Error(`Marca esperada ausente: ${relativePath}`);
  }
}
console.log(`Build validado: ${checks.length} saídas representativas existem e contêm a marca correta.`);
