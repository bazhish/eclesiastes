# Arquitetura do Eclesiastes

Eclesiastes é um site Astro estático. As rotas são criadas a partir de uma coleção MDX e seguem `/<materia>/<bimestre>/<semana>/<aula>`.

`scripts/migrate_content.py` converte os Markdown do Gabarito em documentos de conteúdo: roteiros `aN`, pausas `qN`, registros `rN` e observações `oN`. A versão atual publica respostas reais copiáveis e mantém a pasta de origem somente para leitura.

`validate-content.mjs` garante cobertura, unicidade de rotas/fontes, tipos explícitos e totais do conteúdo atual (111 roteiros, 71 pausas, 99 questões, 40 registros, 47 observações e 269 documentos). `validate-build.mjs` confirma páginas representativas e a ausência de superfícies removidas. O workflow de GitHub Actions executa `npm run verify` antes de publicar no GitHub Pages.
