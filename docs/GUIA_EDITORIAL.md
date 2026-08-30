# Guia editorial do Eclesiastes

## Papel do site

Eclesiastes é um material de consulta. Ele não afirma que uma atividade foi enviada, aceita, corrigida ou executada por uma pessoa específica. Respostas de referência ajudam no estudo; a evidência própria continua sendo responsabilidade de quem realiza a atividade.

## Fonte de verdade e migração

A fonte revisada fica fora do repositório, na pasta `gabarito`. A migração lê somente os arquivos `Gabarito - Roteiro Prático Aula N.md`, `Gabarito - Pausa e Responda Aula N.md` e seus diretórios `codigo/aula-N`.

`npm run migrate:content` nunca escreve na fonte. Ele gera MDX, ZIPs de artefatos e `docs/source-index.json`. Use `ECLESIASTES_SOURCE_DIR` para indicar outra cópia da fonte.

## Regras de conteúdo

- Preserve o texto revisado e a associação entre matéria, semana, aula e arquivo de origem.
- Não invente alternativas, resultados de execução, notas, autoria, credenciais ou dados pessoais.
- Cada arquivo “Pausa e Responda” é uma página independente, mesmo quando houver mais de um na mesma semana.
- Artefatos só podem ser publicados quando vierem de um diretório `codigo/aula-N` correspondente ao roteiro.
- Uma mudança de fonte deve terminar com `npm run verify` sem erros.

## Publicação

Antes de publicar material novo, confirme que a fonte permite a divulgação, não contém dados sensíveis e que os ZIPs e links funcionam. O Pages publica em `https://bazhish.github.io/eclesiastes/`.
