import { existsSync, readdirSync, readFileSync } from 'node:fs';
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
const sourceReferences = [];
const routes = new Set();
let activities = 0;
let pauses = 0;
let questions = 0;
let artifacts = 0;

for (const file of files) {
  const text = readFileSync(file, 'utf8');
  const match = text.match(/^---\r?\n([\s\S]+?)\r?\n---/);
  if (!match) throw new Error(`Frontmatter ausente: ${relative(root, file)}`);
  const data = JSON.parse(match[1]);
  if (!/^(?:a|q)\d+$/.test(data.aula)) throw new Error(`Identificador inválido: ${relative(root, file)}`);

  const route = `/${data.materiaSlug}/${data.bimestre}/semana-${data.semana}/${data.aula}`;
  if (routes.has(route)) throw new Error(`Rota duplicada: ${route}`);
  routes.add(route);

  if (data.atividade) {
    activities += 1;
    if (!data.atividade.fonte.startsWith('gabarito/')) throw new Error(`Fonte inválida: ${relative(root, file)}`);
    sourceReferences.push(data.atividade.fonte);
    if (data.atividade.artefato) {
      artifacts += 1;
      const artifact = join(root, 'public', data.atividade.artefato.href);
      if (!existsSync(artifact)) throw new Error(`ZIP ausente: ${relative(root, artifact)}`);
    }
  }
  if (data.quizzes.length) {
    pauses += 1;
    questions += data.quizzes.length;
    const quizSources = new Set();
    for (const quiz of data.quizzes) {
      if (!quiz.fonte.startsWith('gabarito/')) throw new Error(`Fonte inválida: ${relative(root, file)}`);
      quizSources.add(quiz.fonte);
    }
    if (quizSources.size !== 1) throw new Error(`Bloco de pausa com fontes misturadas: ${relative(root, file)}`);
    sourceReferences.push([...quizSources][0]);
  }
}

const records = sourceIndex.registros;
if (files.length !== records.length) throw new Error(`Cobertura incompleta: ${files.length}/${records.length} documentos.`);
if (activities !== sourceIndex.contagens.roteiros) throw new Error(`Roteiros divergentes: ${activities}.`);
if (pauses !== sourceIndex.contagens.pausas) throw new Error(`Pausas divergentes: ${pauses}.`);
if (questions !== sourceIndex.contagens.questoes) throw new Error(`Questões divergentes: ${questions}.`);
if (new Set(sourceReferences).size !== sourceReferences.length) throw new Error('Uma fonte foi associada a mais de uma página.');
if (new Set(records.map((record) => record.fonte)).size !== records.length) throw new Error('O índice contém fonte duplicada.');
if (new Set(records.map((record) => record.rota)).size !== records.length) throw new Error('O índice contém rota duplicada.');
if (artifacts !== records.filter((record) => record.artefato).length) throw new Error('Cobertura de artefatos divergente.');

console.log(`Conteúdo validado: ${activities} roteiros, ${pauses} pausas, ${questions} questões, ${artifacts} ZIPs e ${files.length} documentos.`);
