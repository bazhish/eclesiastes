import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const contentTypeSchema = z.enum(['pausa', 'roteiro', 'registro', 'aula']);

const codeFileSchema = z.object({
  caminho: z.string().min(1),
  linguagem: z.string().min(1),
  conteudo: z.string(),
});

const quizSchema = z.object({
  pergunta: z.string().min(1),
  resposta: z.string().min(1),
  fonte: z.string().min(1),
});

const atividadeSchema = z.object({
  enunciado: z.string().min(1),
  resposta: z.string().min(1),
  conteudo: z.string().min(1),
  fonte: z.string().min(1),
  arquivos: z.array(codeFileSchema).default([]),
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
      aula: z.string().regex(/^(?:a|q)\d+$/),
      tipo: contentTypeSchema,
      titulo: z.string().min(1),
      atividade: atividadeSchema.optional(),
      quizzes: z.array(quizSchema).default([]),
    })
    .refine((aula) => aula.atividade || aula.quizzes.length > 0, {
      message: 'Cada aula precisa ter uma atividade prática ou pelo menos uma questão.',
    }),
});

export const collections = { aulas };
