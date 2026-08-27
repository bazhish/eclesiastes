import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const quizSchema = z
  .object({
    pergunta: z.string().min(1),
    alternativas: z.array(z.string().min(1)).min(2),
    resposta: z.string().min(1),
    justificativa: z.string().min(1).optional(),
    fonte: z.string().min(1),
  });

const atividadeSchema = z.object({
  tipo: z.enum(['pratica', 'resposta']),
  enunciado: z.string().min(1),
  resposta: z.string().min(1),
  fonte: z.string().min(1),
});

const aulas = defineCollection({
  loader: glob({
    base: './src/content/aulas',
    pattern: '**/*.{md,mdx}',
  }),
  schema: z
    .object({
      materia: z.string().min(1),
      materiaSlug: z.string().regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/),
      bimestre: z.number().int().positive(),
      semana: z.number().int().positive(),
      ordem: z.number().int().positive(),
      aula: z.string().regex(/^[a-z][a-z0-9-]*$/),
      titulo: z.string().min(1),
      atividade: atividadeSchema.optional(),
      quizzes: z.array(quizSchema).default([]),
    })
    .refine((aula) => aula.atividade || aula.quizzes.length > 0, {
      message: 'Cada aula precisa ter uma atividade prática ou pelo menos um quiz.',
    }),
});

export const collections = { aulas };
