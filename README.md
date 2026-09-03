<div align="center">

<img src="public/icon-512.png" alt="Marca Eclesiastes: uma teia Ananse Ntentan" width="112" height="112" />

# Eclesiastes

**Portal de consulta para Desenvolvimento de Sistemas.**

Interface estática inspirada no fluxo do AVA, com respostas do 3º bimestre organizadas por matéria, semana e tipo de atividade.

[![Astro](https://img.shields.io/badge/Astro-static-BC52EE?logo=astro&logoColor=white)](https://astro.build)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4-06B6D4?logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![MDX](https://img.shields.io/badge/MDX-content_collections-1B1F24?logo=mdx&logoColor=white)](https://docs.astro.build/en/guides/content-collections/)
[![GitHub Pages](https://img.shields.io/badge/GitHub_Pages-publicado-2EA44F?logo=githubpages&logoColor=white)](https://bazhish.github.io/eclesiastes/)
![pt-BR](https://img.shields.io/badge/idioma-pt--BR-informational)
[![License: MIT](https://img.shields.io/badge/licença-MIT-yellow.svg)](./LICENSE)

[**Ver no ar**](https://bazhish.github.io/eclesiastes/) · [Guia editorial](./docs/GUIA_EDITORIAL.md) · [Sistema de design](./docs/SISTEMA_DE_DESIGN.md)

</div>

---

## Sobre

Eclesiastes organiza sete matérias do 3º bimestre em uma navegação por matéria, bimestre, semana e recurso. A experiência preserva a lógica de consulta do AVA, mas com identidade visual própria: superfícies claras, modo escuro, navegação lateral contextual e blocos de resposta prontos para cópia.

O símbolo central é uma interpretação original de **Ananse Ntentan**, uma teia associada à sabedoria, criatividade e à complexidade do conhecimento.

## Estado atual

| Item | Total |
|---|---:|
| Matérias | 7 |
| Semanas com gabarito | 47 |
| Documentos publicados | 269 |
| Roteiros e atividades práticas | 111 |
| Blocos Pause e Responda | 71 |
| Questões organizadas | 99 |
| Registros de Aula | 40 |
| Observações | 47 |

## Funcionalidades

- Navegação por matéria, bimestre, semana, aula, atividade, registro e bloco “Pause e Responda”.
- Catálogo de matérias, checkpoints locais de visita, tema claro/escuro e navegação responsiva por teclado.
- Respostas em componente reutilizável com botão de copiar, ícone de duas folhas e suporte a texto longo, tabelas e blocos de código.
- Conteúdo rastreável por `docs/source-index.json`, mantendo vínculo entre rota publicada e Markdown original do Gabarito.
- Migração local que recria apenas o conteúdo derivado do site, sem modificar a pasta de origem.

## Stack

| Camada | Tecnologia |
|---|---|
| Aplicação | [Astro](https://astro.build) estático |
| Estilos | [Tailwind CSS 4](https://tailwindcss.com) e tokens CSS |
| Conteúdo | MDX e Content Collections com validação Zod |
| Migração | Python padrão, sem alterar a fonte |
| Hospedagem | GitHub Pages via GitHub Actions |

## Rodando localmente

Pré-requisitos: Node.js 24+ e Python 3.12+.

```powershell
npm ci
npm run dev
```

O site abre no endereço local indicado pelo Astro. Para executar a validação completa:

```powershell
npm run verify
```

## Atualizando o conteúdo

A fonte de verdade padrão é a pasta local `C:\Users\MAX\Desktop\Gabarito`. Em outro computador, defina `ECLESIASTES_SOURCE_DIR` com o caminho da pasta de gabaritos antes de migrar.

```powershell
$env:ECLESIASTES_SOURCE_DIR = 'D:\materiais\gabarito'
npm run migrate:content
npm run verify
```

O processo recria somente `src/content/aulas` e `docs/source-index.json`; nunca modifica a fonte revisada. O conteúdo das respostas deve permanecer igual ao Markdown original.

## Estrutura

```text
src/
  components/       # navegação, cartões, cópia e layout
  content/aulas/    # MDX gerado pela migração
  pages/            # rotas estáticas por matéria/bimestre/semana/aula
  styles/           # tokens e interface
scripts/
  migrate_content.py
  validate-content.mjs
  validate-build.mjs
public/
  brand.svg         # marca Ananse Ntentan original
docs/
  source-index.json # rastreabilidade entre Gabarito e rota publicada
```

## Licença

[MIT](./LICENSE).
