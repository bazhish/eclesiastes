import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const quizSchema = z
  .object({
    pergunta: z.string().min(1),
    resposta: z.string().min(1),
    justificativa: z.string().min(1).optional(),
  });

const atividadeSchema = z.object({
  enunciado: z.string().min(1),
  resposta: z.string().min(1),
  artefato: z
    .object({
      linguagem: z.enum(['text', 'bash', 'css', 'html', 'javascript', 'jsx', 'python', 'sql', 'typescript']),
      conteudo: z.string().min(1),
      url: z.string().startsWith('/').optional(),
    })
    .optional(),
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
      bimestre: z.literal(3),
      semana: z.number().int().min(15).max(21),
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
