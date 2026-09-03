<div align="center">

<img src="public/icon-512.png" alt="Marca Eclesiastes: uma teia Ananse Ntentan" width="104" height="104" />

# Eclesiastes

**Conhecimento para consultar, adaptar e construir.**

Portal estático com estrutura de matérias, semanas e aulas do 3º bimestre de Desenvolvimento de Sistemas, preparado para receber novo conteúdo.

[![Astro](https://img.shields.io/badge/Astro-static-BC52EE?logo=astro&logoColor=white)](https://astro.build)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4-06B6D4?logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![MDX](https://img.shields.io/badge/MDX-content_collections-1B1F24?logo=mdx&logoColor=white)](https://docs.astro.build/en/guides/content-collections/)
![pt-BR](https://img.shields.io/badge/idioma-pt--BR-informational)
[![License: MIT](https://img.shields.io/badge/licença-MIT-yellow.svg)](./LICENSE)

[**Ver no ar**](https://bazhish.github.io/eclesiastes/) · [Guia editorial](./docs/GUIA_EDITORIAL.md) · [Sistema de design](./docs/SISTEMA_DE_DESIGN.md)

</div>

---

## Sobre

Eclesiastes organiza sete matérias do 3º bimestre em uma navegação por matéria, bimestre, semana e aula. O conteúdo antigo de respostas foi removido; as páginas permanecem com aviso de conteúdo pendente para facilitar uma nova publicação.

O símbolo central é uma interpretação original de **Ananse Ntentan**, uma teia associada à sabedoria, criatividade e à complexidade do conhecimento.

## Funcionalidades

- Navegação por matéria, bimestre, semana, roteiro e bloco “Pausa e Responda”.
- Cartões de matérias com favoritos locais, checkpoints de visita, tema claro/escuro e navegação responsiva por teclado.
- Páginas mantidas com o aviso “Essa resposta ainda não divulgada”.
- Estrutura pronta para reinserção futura de enunciados, respostas e arquivos quando o novo conteúdo for autorizado.
- 189 documentos rastreáveis: 118 roteiros e 71 blocos de pausa, todos sem respostas antigas nem arquivos de código inline.

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

A fonte de verdade padrão, quando houver novo conteúdo, é uma pasta local de gabarito. Em outro computador, defina `ECLESIASTES_SOURCE_DIR` com o caminho da pasta `gabarito` antes de migrar.

```powershell
$env:ECLESIASTES_SOURCE_DIR = 'D:\materiais\gabarito'
npm run migrate:content
npm run verify
```

O processo recria somente `src/content/aulas` e `docs/source-index.json`; nunca modifica a fonte revisada. A versão atual está higienizada e não mantém arquivos de código inline.

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
  source-index.json # rastreabilidade entre conteúdo pendente e rota publicada
```

## Licença

[MIT](./LICENSE).
