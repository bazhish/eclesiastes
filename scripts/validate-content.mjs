import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('..', import.meta.url));
const contentRoot = join(root, 'src', 'content', 'aulas');
const publicRoot = join(root, 'public');

function filesAt(directory) {
  return readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const path = join(directory, entry.name);
    return entry.isDirectory() ? filesAt(path) : [path];
  });
}

const files = filesAt(contentRoot).filter((file) => file.endsWith('.mdx'));
let activities = 0;
let answerKeys = 0;
let questions = 0;
for (const file of files) {
  const text = readFileSync(file, 'utf8');
  const match = text.match(/^---\r?\n([\s\S]+?)\r?\n---/);
  if (!match) throw new Error(`Frontmatter ausente: ${relative(root, file)}`);
  const data = JSON.parse(match[1]);
  if (!/^a\d+$|^q$/.test(data.aula)) throw new Error(`Identificador de aula inválido: ${relative(root, file)}`);
  if (data.atividade) {
    activities += 1;
    const artifact = data.atividade.artefato;
    if (artifact?.url && !existsSync(join(publicRoot, artifact.url.slice(1)))) throw new Error(`Artefato ausente: ${artifact.url}`);
  }
  if (data.quizzes.length) {
    answerKeys += 1;
    questions += data.quizzes.length;
  }
}

if (activities !== 118) throw new Error(`Esperadas 118 atividades; encontradas ${activities}.`);
if (answerKeys !== 47) throw new Error(`Esperados 47 gabaritos; encontrados ${answerKeys}.`);
if (questions !== 141) throw new Error(`Esperadas 141 questões; encontradas ${questions}.`);
console.log(`Conteúdo validado: ${activities} atividades, ${answerKeys} gabaritos, ${questions} questões.`);
