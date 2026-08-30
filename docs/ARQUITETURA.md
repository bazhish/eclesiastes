# Arquitetura do Eclesiastes

Eclesiastes é um site Astro estático. As rotas são criadas a partir de uma coleção MDX e seguem `/<materia>/<bimestre>/<semana>/<aula>`.

`scripts/migrate_content.py` converte a fonte revisada em duas formas de conteúdo: roteiros `aN` e pausas `qN`. O migrador também arquiva cada diretório de código associado em um ZIP sob `public/artefatos` e registra fonte, rota e presença de artefato em `docs/source-index.json`.

`validate-content.mjs` garante cobertura, unicidade de rotas/fontes, totais derivados da fonte e presença dos ZIPs. `validate-build.mjs` confirma páginas e artefatos representativos depois do build. O workflow de GitHub Actions executa `npm run verify` antes de publicar no GitHub Pages.
