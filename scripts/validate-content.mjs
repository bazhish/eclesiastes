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
const sourceReferences = [];
const routes = new Set();
let activities = 0;
let pauses = 0;
let questions = 0;
let inlineFiles = 0;
let codedActivities = 0;

for (const file of files) {
  const text = readFileSync(file, 'utf8');
  const match = text.match(/^---\r?\n([\s\S]+?)\r?\n---/);
  if (!match) throw new Error(`Frontmatter ausente: ${relative(root, file)}`);
  const data = JSON.parse(match[1]);
  if (!/^(?:a|q)\d+$/.test(data.aula)) throw new Error(`Identificador inválido: ${relative(root, file)}`);
  if (!['pausa', 'roteiro', 'registro', 'aula'].includes(data.tipo)) throw new Error(`Tipo inválido: ${relative(root, file)}`);

  const route = `/${data.materiaSlug}/${data.bimestre}/semana-${data.semana}/${data.aula}`;
  if (routes.has(route)) throw new Error(`Rota duplicada: ${route}`);
  routes.add(route);

  if (data.atividade) {
    activities += 1;
    if (!data.atividade.fonte.startsWith('gabarito/')) throw new Error(`Fonte inválida: ${relative(root, file)}`);
    sourceReferences.push(data.atividade.fonte);
    if (!Array.isArray(data.atividade.arquivos)) throw new Error(`Arquivos inline ausentes: ${relative(root, file)}`);
    inlineFiles += data.atividade.arquivos.length;
    if (data.atividade.arquivos.length) codedActivities += 1;
    for (const code of data.atividade.arquivos) {
      if (!code.caminho || !code.linguagem || typeof code.conteudo !== 'string') throw new Error(`Arquivo inline inválido: ${relative(root, file)}`);
      if (code.caminho.includes('..') || code.caminho.includes('\\') || code.caminho.startsWith('.git/')) throw new Error(`Caminho inline inseguro: ${code.caminho}`);
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
if (inlineFiles !== sourceIndex.contagens.arquivosCodigo) throw new Error(`Arquivos inline divergentes: ${inlineFiles}.`);
if (codedActivities !== sourceIndex.contagens.atividadesComCodigo) throw new Error(`Atividades com código divergentes: ${codedActivities}.`);
if (records.some((record) => 'artefato' in record)) throw new Error('Índice ainda contém artefatos.');

console.log(`Conteúdo validado: ${activities} roteiros, ${pauses} pausas, ${questions} questões, ${inlineFiles} arquivos inline em ${codedActivities} atividades e ${files.length} documentos.`);
