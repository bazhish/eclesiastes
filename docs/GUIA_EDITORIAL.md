# Guia editorial do Eclesiastes

## Papel do site

Eclesiastes é um material de consulta. Ele não afirma que uma atividade foi enviada, aceita, corrigida ou executada por uma pessoa específica. A versão atual exibe respostas reais organizadas a partir do Gabarito local.

## Fonte de verdade e migração

A fonte revisada fica fora do repositório, na pasta `Gabarito`. A migração lê os arquivos Markdown semanais de cada matéria, bimestre e semana.

`npm run migrate:content` nunca escreve na fonte. Ele gera MDX e `docs/source-index.json`. Use `ECLESIASTES_SOURCE_DIR` para indicar outra cópia da fonte.

## Regras de conteúdo

- Preserve a associação entre matéria, semana, aula e arquivo de origem.
- Não invente alternativas, resultados de execução, notas, autoria, credenciais ou dados pessoais.
- Cada bloco “Pause e Responda” é uma página independente, mesmo quando houver mais de um na mesma semana.
- Respostas copiáveis devem usar o componente reutilizável do sistema e preservar o texto original do Markdown.
- Uma mudança de fonte deve terminar com `npm run verify` sem erros.

## Publicação

Antes de publicar material novo, confirme que a fonte permite a divulgação, não contém dados sensíveis e que os ZIPs e links funcionam. O Pages publica em `https://bazhish.github.io/eclesiastes/`.
