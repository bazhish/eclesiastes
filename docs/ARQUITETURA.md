# Arquitetura do Eclesiastes

Eclesiastes é um site Astro estático. As rotas são criadas a partir de uma coleção MDX e seguem `/<materia>/<bimestre>/<semana>/<aula>`.

`scripts/migrate_content.py` converte uma fonte revisada em duas formas de conteúdo: roteiros `aN` e pausas `qN`. A versão atual mantém a estrutura publicada, mas os conteúdos de resposta foram substituídos pelo aviso de divulgação pendente e não há arquivos incorporados no campo `atividade.arquivos`.

`validate-content.mjs` garante cobertura, unicidade de rotas/fontes, tipos explícitos e totais do conteúdo atual (118 roteiros, 71 pausas, 71 avisos de resposta, 189 documentos e nenhum arquivo inline). `validate-build.mjs` confirma páginas representativas e a ausência de superfícies removidas. O workflow de GitHub Actions executa `npm run verify` antes de publicar no GitHub Pages.
