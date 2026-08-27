# Gabarito 3B

Aplicação estática para consulta das atividades práticas e dos gabaritos “Pause e Responda” do 3º bimestre de Desenvolvimento de Sistemas. O projeto usa Astro, Markdown/MDX, TypeScript e Tailwind CSS.

## O que está incluído

- 118 atividades práticas, cada uma com resposta de referência e artefato técnico quando a fonte o possui.
- 47 blocos “Pause e Responda”, somando 141 questões.
- Navegação por matéria, semana e aula; busca e filtros; tema claro/escuro; cópia de respostas; download de artefatos.
- Conteúdo estático e portável: não há banco de dados, conta, rastreamento ou conexão com o AVA.

## Uso local

```powershell
npm install
npm run dev
```

Abra o endereço local informado. Para conferir conteúdo, tipos e páginas geradas:

```powershell
npm run verify
```

## Conteúdo e fonte

`R3B` é a fonte preservada das respostas revisadas. A coleção publicada pela aplicação fica em `src/content/aulas`; seus arquivos usam nomes curtos como `a1.mdx` e `q.mdx`. Para atualizar a coleção após uma revisão em `R3B`, execute:

```powershell
npm run migrate:content
```

O processo não altera `R3B`. As regras de conteúdo e revisão estão em [`docs/GUIA_EDITORIAL.md`](docs/GUIA_EDITORIAL.md).

## Publicação

O projeto ainda não está publicado. Antes de configurar GitHub Pages ou Cloudflare Pages, é necessário escolher explicitamente se o site será público ou privado e revisar as fontes, os artefatos e qualquer dado sensível.

## Licença

Distribuído sob a licença MIT. Veja [`LICENSE`](LICENSE).
