# Guia editorial e de manutenção

## Propósito

O Gabarito é um material de consulta. Ele não declara que uma atividade foi enviada, aceita, corrigida ou executada por determinada pessoa. A redação deve sempre separar três camadas: o que o roteiro pede, a resposta de referência e a evidência que ainda precisa ser produzida pelo estudante.

## Fonte, fato e interpretação

- **Fato de origem:** título da atividade, pergunta do quiz, enunciado e artefato vinculados ao arquivo preservado em `R3B`.
- **Resposta de referência:** explicação técnica que pode orientar estudo, revisão e adaptação; não substitui a execução solicitada.
- **Evidência própria:** teste, print, log, link, registro de decisão ou resultado real produzido pelo estudante. Ela não deve ser inventada nem reutilizada de outra pessoa.

Não afirmar notas, conclusão de curso, progresso no AVA, autoria de terceiros ou resultados de testes que não ocorreram. Não inserir credenciais, dados pessoais, identificadores estudantis, nomes de colegas ou conteúdo privado de plataformas.

## Como editar ou adicionar uma aula

Cada aula é um arquivo Markdown/MDX em `src/content/aulas/<materia>/semana-<n>/`. Os identificadores permanecem curtos: `a1`, `a2` e `q` para o gabarito semanal. O frontmatter deve obedecer a `src/content.config.ts`; `npm run check` acusa inconsistências antes do build.

Para recriar a coleção a partir da fonte atual, execute `npm run migrate:content`. O script lê `../R3B/materias`, cria os registros de consulta e copia os artefatos referenciados para `public/artefatos`; ele não altera a pasta `R3B`.

## Linguagem e acessibilidade

Escreva títulos curtos, com verbo ou assunto claro. Prefira frases diretas, descreva siglas na primeira menção e explique termos necessários. Não dependa de cor para indicar resposta, status ou prioridade. Todo novo controle interativo deve ter rótulo visível, foco perceptível e operação por teclado.

## Revisão antes de publicar

Verifique se a fonte permite publicação, se não há dados pessoais ou credenciais, se links e artefatos funcionam e se a resposta não promete execução ou aprovação. A publicação só acontece depois da escolha explícita de visibilidade e plataforma.
