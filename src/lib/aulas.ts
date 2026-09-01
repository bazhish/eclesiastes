import { getCollection, type CollectionEntry } from 'astro:content';

export type Aula = CollectionEntry<'aulas'>;
export type ContentType = Aula['data']['tipo'];

export async function todasAsAulas() {
  return (await getCollection('aulas')).sort((a, b) => {
    const subject = a.data.materia.localeCompare(b.data.materia, 'pt-BR');
    if (subject !== 0) return subject;
    if (a.data.semana !== b.data.semana) return a.data.semana - b.data.semana;
    return a.data.ordem - b.data.ordem;
  });
}

export function rotaDaAula(aula: Aula) {
  return `/${aula.data.materiaSlug}/${aula.data.bimestre}/semana-${aula.data.semana}/${aula.data.aula}`;
}

export function comBase(path: string) {
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  return `${base}${path}`;
}

export function agruparNavegacao(aulas: Aula[]) {
  const materias = new Map<string, { nome: string; bimestres: Map<number, Map<number, Aula[]>> }>();
  for (const aula of aulas) {
    const existente = materias.get(aula.data.materiaSlug) ?? {
      nome: aula.data.materia,
      bimestres: new Map<number, Map<number, Aula[]>>(),
    };
    const semanas = existente.bimestres.get(aula.data.bimestre) ?? new Map<number, Aula[]>();
    const semana = semanas.get(aula.data.semana) ?? [];
    semana.push(aula);
    semanas.set(aula.data.semana, semana);
    existente.bimestres.set(aula.data.bimestre, semanas);
    materias.set(aula.data.materiaSlug, existente);
  }
  return materias;
}

export function temaDaSemana(aulas: Aula[]) {
  const title = aulas[0]?.data.titulo ?? '';
  return title
    .replace(/\s*·\s*Pausa e Responda\s*·\s*Aula\s*\d+$/i, '')
    .replace(/\s*·\s*Aula\s*\d+$/i, '')
    .trim();
}

export function semanasPorBimestre(aulas: Aula[]) {
  const grouped = new Map<number, Map<number, Aula[]>>();
  for (const aula of aulas) {
    const weeks = grouped.get(aula.data.bimestre) ?? new Map<number, Aula[]>();
    const entries = weeks.get(aula.data.semana) ?? [];
    entries.push(aula);
    weeks.set(aula.data.semana, entries);
    grouped.set(aula.data.bimestre, weeks);
  }
  return Array.from(grouped.entries()).sort(([a], [b]) => a - b).map(([bimestre, weeks]) => ({
    bimestre,
    semanas: Array.from(weeks.entries()).sort(([a], [b]) => a - b).map(([semana, itens]) => ({
      semana,
      tema: temaDaSemana(itens),
      paths: itens.sort((a, b) => a.data.ordem - b.data.ordem).map(rotaDaAula),
    })),
  }));
}
