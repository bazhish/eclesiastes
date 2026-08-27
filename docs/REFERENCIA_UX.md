# Referência de UX do AVA

**Objetivo:** preservar convenções de navegação que já são familiares para quem usa o AVA, sem reproduzir a identidade visual, o conteúdo, a marca ou os ativos proprietários da plataforma observada.

**Base da observação:** navegação autenticada no AVA em 27/08/2026, limitada à página inicial, à disciplina Programação Back-End, ao 3º bimestre, a uma atividade de registro e a um quiz H5P. Esta referência descreve padrões de interface, não dados pessoais, notas, conteúdos submetidos ou informações de conta.

## Padrões a preservar

### Hierarquia de navegação

O percurso principal é previsível e deve ser mantido no Gabarito:

```text
Disciplinas → Bimestre → Semana → Aula → Item da aula
```

Na página inicial, as disciplinas aparecem como cartões de acesso. Dentro de uma disciplina, os bimestres são listados como destinos independentes. A página do bimestre apresenta as semanas como seções expansíveis; cada semana contém uma breve apresentação e aulas expansíveis; cada aula mostra os seus itens.

No Gabarito, essa estrutura será representada por uma árvore lateral e por páginas estáticas de aula. A árvore deve manter a semana e a aula corrente abertas, sem obrigar a pessoa a reaprender a localização do material.

### Contexto e retorno

As páginas internas exibem uma trilha de navegação completa: início, bimestre, semana, aula e item atual. O título da página repete o item selecionado. Esse duplo contexto — breadcrumb no topo e item destacado na árvore — evita perda de orientação em coleções longas.

O Gabarito deve oferecer breadcrumb textual e navegável, com o último item marcado como página atual. A página da aula também deve apresentar links para aula anterior e próxima quando existirem.

### Agrupamento e expansão

Semanas e aulas usam cabeçalhos clicáveis com indicador de expansão e ação de “contrair tudo”. Os itens ficam visualmente subordinados dentro do cartão da aula. É um bom padrão para navegar 15–21 semanas sem transformar a tela em uma lista plana.

O Gabarito preservará a expansão por semana/aula, mas com controles semânticos `button`, estado `aria-expanded`, foco visível e preferência persistida apenas no navegador. A ação global será rotulada de forma inequívoca: “Recolher todas as semanas”.

### Tipos de item e estado

Cada item do AVA combina três sinais: ícone/tipo, nome e estado de conclusão. Na amostra observada, materiais, quizzes H5P e tarefas de registro são distinguíveis mesmo antes de abrir o item. Esse reconhecimento rápido deve ser mantido.

No Gabarito, os tipos serão reduzidos a:

- **Atividade prática:** enunciado, resposta e cópia.
- **Quiz:** pergunta, alternativas, correta e justificativa; não terá botão de cópia.

O site não exibirá nota, submissão, comentários, pendências pessoais ou status importado do AVA. Quando útil, haverá apenas indicadores locais e neutros, como “Resposta disponível” e “Quiz revisado”.

### Registro da atividade

A página de tarefa observada apresenta título, materiais necessários, roteiro, instrução de entrega, estado do envio e área de feedback. O conteúdo pedagógico vem antes de informações administrativas.

No Gabarito, a página de atividade seguirá a ordem: título e contexto, enunciado, resposta pronta, artefato/código e checklist de personalização. Esse arranjo preserva a expectativa de leitura, mas remove elementos de envio, avaliação e dados privados.

### Quiz

O quiz é apresentado como um item H5P dentro de uma página própria, com breadcrumb e requisito de conclusão. A interação é separada da lista da aula, o que deixa claro que se trata de uma atividade diferente do material principal.

No Gabarito, o `QuizBlock` será visualmente separado do cartão de atividade. A alternativa correta ficará inicialmente oculta e será revelada por um controle acessível; a justificativa aparece em seguida quando existir. Não haverá simulação de tentativa, nota ou requisito de conclusão.

## Pontos a melhorar no Gabarito

### Leitura e prioridade

O AVA concentra muitos itens, estados e ícones no mesmo plano visual. O Gabarito deve reduzir a densidade: uma aula por página, resposta em cartão destacado e quiz em seção independente. A resposta é a ação principal; navegação e metadados devem ficar secundários.

### Cópia sem ambiguidade

O AVA pede envio de texto, mas não oferece uma interação voltada a reutilizar trechos. O Gabarito terá `CopyButton` por atividade, com ícone, rótulo, feedback temporário “Copiado”, `aria-live` e alternativa por teclado. O botão nunca aparecerá em quizzes.

### Acessibilidade e mobile

O Gabarito deve superar o padrão observado com:

- estrutura de headings contínua e landmarks claros;
- navegação por teclado em árvore, breadcrumb, cópia e revelação de quiz;
- contraste AA nos modos claro e escuro;
- alvos de toque amplos e barra lateral recolhível em telas pequenas;
- ausência de dependência exclusiva de cor, ícone ou hover;
- respeito a `prefers-reduced-motion` em transições de expansão.

### Identidade própria

Não reutilizar logotipo, brasão, textos institucionais, fontes, paleta, ícones proprietários, ilustrações, imagens, CSS, capturas ou organização visual literal do AVA. O Gabarito usará paleta, tipografia, nomes de componentes e ícones próprios; a familiaridade virá somente da estrutura de informação.

## Implicações para o schema

A amostra confirma cardinalidade variável. Semanas observadas têm duas ou três aulas; aulas podem conter somente material, material mais tarefa, ou material mais vários quizzes. Portanto, o schema não deve pressupor um número fixo de aulas, atividades ou quizzes.

O conteúdo do Gabarito terá uma página por aula. `atividade` será obrigatória para as aulas incluídas no acervo; `quizzes` continuará como array opcional. Metadados de origem, notas, conclusão e URLs do AVA não serão migrados.

## Decisão de design

**Adotar a hierarquia do AVA como modelo mental; não adotar sua aparência como modelo visual.**

Isso preserva reconhecimento para quem estudou no ambiente original e, ao mesmo tempo, produz uma ferramenta de consulta mais clara, responsiva e independente.
