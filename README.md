<div align="center">

<img src="public/icon-512.png" alt="Marca Eclesiastes: uma teia Ananse Ntentan" width="104" height="104" />

# Eclesiastes

**Conhecimento para consultar, adaptar e construir.**

Portal estático de roteiros práticos, respostas de referência e arquivos de código inline do 3º bimestre de Desenvolvimento de Sistemas.

[![Astro](https://img.shields.io/badge/Astro-static-BC52EE?logo=astro&logoColor=white)](https://astro.build)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4-06B6D4?logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![MDX](https://img.shields.io/badge/MDX-content_collections-1B1F24?logo=mdx&logoColor=white)](https://docs.astro.build/en/guides/content-collections/)
![pt-BR](https://img.shields.io/badge/idioma-pt--BR-informational)
[![License: MIT](https://img.shields.io/badge/licença-MIT-yellow.svg)](./LICENSE)

[**Ver no ar**](https://bazhish.github.io/eclesiastes/) · [Guia editorial](./docs/GUIA_EDITORIAL.md) · [Sistema de design](./docs/SISTEMA_DE_DESIGN.md)

</div>

---

## Sobre

Eclesiastes organiza material revisado de sete matérias do 3º bimestre em uma navegação por matéria, bimestre, semana e aula. O site é uma ferramenta de consulta: não simula entregas, notas ou evidências que precisem ser produzidas por cada estudante.

O símbolo central é uma interpretação original de **Ananse Ntentan**, uma teia associada à sabedoria, criatividade e à complexidade do conhecimento.

## Funcionalidades

- Navegação por matéria, bimestre, semana, roteiro e bloco “Pausa e Responda”.
- Cartões de matérias com favoritos locais, checkpoints de visita, tema claro/escuro e navegação responsiva por teclado.
- Cópia de respostas e do conteúdo revisado, com retorno acessível.
- Código incorporado nas atividades, com linguagem, caminho e cópia exata do texto exibido.
- 189 documentos rastreáveis: 118 roteiros, 71 blocos de pausa e 141 respostas de referência; 72 atividades têm código, totalizando 197 arquivos inline (46 entradas técnicas filtradas).

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

A fonte de verdade padrão é a pasta local `C:\Users\MAX\Desktop\Desenvolvimento de Sistemas - Gabarito\gabarito`. Em outro computador, defina `ECLESIASTES_SOURCE_DIR` com o caminho da pasta `gabarito` antes de migrar.

```powershell
$env:ECLESIASTES_SOURCE_DIR = 'D:\materiais\gabarito'
npm run migrate:content
npm run verify
```

O processo recria somente `src/content/aulas` e `docs/source-index.json`; nunca modifica a fonte revisada. Quando a fonte externa está disponível, os diretórios `codigo/aula-N` são filtrados e incorporados diretamente ao MDX.

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
  source-index.json # rastreabilidade entre fonte e rota publicada
```

## Licença

[MIT](./LICENSE). O conteúdo acadêmico continua sujeito às regras de uso da fonte que o originou.
