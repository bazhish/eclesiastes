import { getCollection, type CollectionEntry } from 'astro:content';

export type Aula = CollectionEntry<'aulas'>;

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

export function agruparNavegacao(aulas: Aula[]) {
  const materias = new Map<string, { nome: string; semanas: Map<number, Aula[]> }>();
  for (const aula of aulas) {
    const existente = materias.get(aula.data.materiaSlug) ?? {
      nome: aula.data.materia,
      semanas: new Map<number, Aula[]>(),
    };
    const semana = existente.semanas.get(aula.data.semana) ?? [];
    semana.push(aula);
    existente.semanas.set(aula.data.semana, semana);
    materias.set(aula.data.materiaSlug, existente);
  }
  return materias;
}
