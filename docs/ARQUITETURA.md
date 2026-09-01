# Arquitetura do Eclesiastes

Eclesiastes é um site Astro estático. As rotas são criadas a partir de uma coleção MDX e seguem `/<materia>/<bimestre>/<semana>/<aula>`.

`scripts/migrate_content.py` converte a fonte revisada em duas formas de conteúdo: roteiros `aN` e pausas `qN`. Diretórios `codigo/aula-N` são filtrados (197 arquivos textuais úteis; 46 entradas técnicas excluídas) e incorporados no campo `atividade.arquivos`, preservando caminho, linguagem e bytes textuais.

`validate-content.mjs` garante cobertura, unicidade de rotas/fontes, tipos explícitos e totais derivados da fonte (118 roteiros, 71 pausas, 141 questões, 189 documentos, 72 atividades com código e 197 arquivos inline). `validate-build.mjs` confirma páginas representativas e a ausência de superfícies removidas. O workflow de GitHub Actions executa `npm run verify` antes de publicar no GitHub Pages.
