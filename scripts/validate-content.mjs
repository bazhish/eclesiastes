import { readdirSync, readFileSync } from 'node:fs';
import { join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('..', import.meta.url));
const contentRoot = join(root, 'src', 'content', 'aulas');
const sourceIndex = JSON.parse(readFileSync(join(root, 'docs', 'source-index.json'), 'utf8'));

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
const sourceReferences = [];
for (const file of files) {
  const text = readFileSync(file, 'utf8');
  const match = text.match(/^---\r?\n([\s\S]+?)\r?\n---/);
  if (!match) throw new Error(`Frontmatter ausente: ${relative(root, file)}`);
  const data = JSON.parse(match[1]);
  if (!/^a\d+$|^q$/.test(data.aula)) throw new Error(`Identificador de aula inválido: ${relative(root, file)}`);
  if (data.atividade) {
    activities += 1;
    if (!data.atividade.fonte.startsWith('Material/')) throw new Error(`Fonte inválida: ${relative(root, file)}`);
    sourceReferences.push(data.atividade.fonte);
  }
  if (data.quizzes.length) {
    answerKeys += 1;
    questions += data.quizzes.length;
    for (const quiz of data.quizzes) {
      if (!quiz.fonte.startsWith('Material/')) throw new Error(`Fonte inválida: ${relative(root, file)}`);
      if (!quiz.alternativas.includes(quiz.resposta)) throw new Error(`Resposta fora das alternativas: ${relative(root, file)}`);
      sourceReferences.push(quiz.fonte);
    }
  }
}

if (activities !== 118) throw new Error(`Esperadas 118 atividades; encontradas ${activities}.`);
if (answerKeys !== 47) throw new Error(`Esperadas 47 páginas de pausas; encontradas ${answerKeys}.`);
if (questions !== 141) throw new Error(`Esperadas 141 questões; encontradas ${questions}.`);
if (sourceReferences.length !== sourceIndex.registros.length) throw new Error('Índice de fontes incompleto.');
if (new Set(sourceReferences).size !== sourceReferences.length) throw new Error('Uma fonte foi associada a mais de uma página.');
if (new Set(sourceIndex.registros.map((record) => record.fonte)).size !== sourceIndex.registros.length) throw new Error('O índice contém fonte duplicada.');
console.log(`Conteúdo validado: ${activities} atividades, ${answerKeys} páginas de pausas, ${questions} questões e ${sourceReferences.length} fontes rastreáveis.`);
