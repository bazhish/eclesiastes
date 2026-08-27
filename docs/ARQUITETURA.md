# ADR-001: site estático orientado a conteúdo para o Gabarito

**Status:** Aceito  
**Data:** 27/08/2026  
**Decisor:** responsável pelo acervo e pelo deploy

## Contexto

O Gabarito é uma aplicação de consulta às respostas do 3º bimestre. O acervo revisado contém 118 atividades práticas, 47 arquivos de quiz e 141 questões. O conteúdo é local, versionável e não requer atualização em tempo real. A referência de UX confirma uma navegação de quatro níveis: matéria, bimestre, semana e aula.

A cardinalidade não é fixa: há semanas com duas, três ou quatro atividades, aulas com quiz sem atividade prática associada e atividades sem quiz. O site não deve inventar uma resposta para cobrir essas lacunas.

## Decisão

Usar **Astro SSG**, **MDX**, **TypeScript**, **Tailwind CSS** e **Astro Content Collections com Zod**. Cada entrada de conteúdo representa uma aula disponível para consulta e gera uma rota estática. O conteúdo é validado durante o build e nenhuma resposta é buscada em tempo de execução.

A configuração usa a API atual de collections com `glob()` em `src/content.config.ts`, em vez do caminho legado `src/content/config.ts`. Esse formato é o recomendado pela documentação atual do Astro para collections locais com loader em build time. [Documentação oficial de Content Collections do Astro](https://docs.astro.build/en/reference/modules/astro-content/)

## Alternativas consideradas

### Astro + MDX + Content Collections

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa para conteúdo local |
| Custo operacional | Nenhum em execução estática |
| Validação de conteúdo | Forte, com Zod no build |
| Autoria e revisão | Arquivos versionáveis e legíveis |
| Adequação ao acervo | Alta |

**Vantagens:** build rápido, rotas estáticas, tipagem, MDX para anotações e nenhum banco de dados.  
**Limitações:** edição exige alteração de arquivo e novo build.

### CMS headless

| Dimensão | Avaliação |
|---|---|
| Complexidade | Média ou alta |
| Custo operacional | Serviço, credenciais e manutenção |
| Validação de conteúdo | Depende do CMS |
| Adequação ao acervo atual | Baixa |

**Vantagens:** interface de edição para pessoas não técnicas.  
**Limitações:** adiciona autenticação, exposição de conteúdo e operação que o produto não precisa agora.

### JSON manual sem collection

| Dimensão | Avaliação |
|---|---|
| Complexidade inicial | Baixa |
| Validação e tipagem | Fraca sem infraestrutura extra |
| Conteúdo rico | Menos confortável |
| Adequação ao acervo | Média |

**Vantagens:** formato simples.  
**Limitações:** perde MDX, validação integrada e uma boa experiência de manutenção.

## Modelo de conteúdo

```text
src/
  content.config.ts
  content/
    aulas/
      programacao-back-end/
        bimestre-3/
          semana-15/
            aula-2-criacao-de-apis-seguras.mdx
```

Uma entrada usa frontmatter validado e corpo MDX:

```yaml
---
materia: Programação Back-End
materiaSlug: programacao-back-end
bimestre: 3
semana: 15
ordem: 2
aula: a2
titulo: Criação de APIs seguras
atividade:
  enunciado: Desenvolver uma API segura para o cenário proposto.
  resposta: >-
    Autenticação identifica o solicitante; autorização limita ações por papel...
  artefato:
    linguagem: javascript
    conteudo: |
      export function validarToken(token) { /* ... */ }
quizzes:
  - pergunta: Qual é a função principal de um servidor web?
    resposta: Responder a solicitações HTTP.
    justificativa: Um servidor web recebe e responde a requisições HTTP.
---

Observação em MDX quando a explicação complementar for necessária.
```

### Exceção documentada: aula sem atividade prática

O briefing inicial pressupõe uma atividade por aula, mas o acervo real contém quizzes e materiais sem registro prático correspondente. Por isso, `atividade` é opcional no schema; a validação exige que a aula tenha ao menos uma atividade ou um quiz. A interface mostra “Sem resposta prática cadastrada” apenas nesses casos e nunca fabrica conteúdo.

## Rotas e navegação

Rotas estáticas seguem:

```text
/[materia]/[bimestre]/[semana]/[aula]
```

Exemplo:

```text
/programacao-back-end/3/semana-15/a2
```

`getStaticPaths()` obtém as entradas da collection, ordena por matéria, semana e ordem, e cria os parâmetros a partir do frontmatter. A árvore lateral e o breadcrumb são derivados do mesmo conjunto ordenado; não haverá uma segunda fonte de verdade para a navegação.

A busca e o filtro são opcionais e serão pré-gerados em um índice leve no build. A filtragem roda no cliente sem serviço externo, sem registrar consultas e sem expor metadados do AVA.

## Renderização e interatividade

Astro renderiza todas as páginas no build. Apenas `CopyButton`, expansão da árvore, modo de cor, busca e revelação de resposta de quiz usam JavaScript no cliente.

Astro View Transitions será adotado somente para navegações internas depois de a versão instalada ser verificada no projeto. O site precisa continuar navegável e legível sem JavaScript; transição é aprimoramento, não requisito funcional.

## Migração

1. Ler cada resposta Markdown revisada em `R3B/materias`.
2. Converter matéria, semana, título, enunciado/respostas e artefato para frontmatter/MDX.
3. Converter cada `pause-e-responda.md` em uma aula de gabarito. As fontes preservadas trazem pergunta e resposta correta, mas não as alternativas completas; a interface revela esse gabarito sem inventar opções.
4. Gerar uma entrada por aula com conteúdo disponível; não migrar URLs, notas, conclusão, comentários ou qualquer dado do AVA.
5. Executar `astro check` e `astro build`; qualquer frontmatter inválido bloqueia a migração.

O script de migração será idempotente e gravará somente sob `Gabarito/src/content/aulas`. Os arquivos de origem permanecem intactos.

## Consequências

- Conteúdo inválido impede o build, em vez de gerar páginas parciais.
- A rota, breadcrumb e árvore permanecem consistentes porque derivam da mesma collection.
- O produto funciona em hospedagem estática e não requer banco, login ou API.
- Uma futura edição por interface exigirá reavaliar CMS, autenticação e visibilidade do conteúdo.
- `site`, `base`, repositório remoto e deploy só serão configurados depois da decisão explícita sobre visibilidade.

## Próximas ações

1. Implementar a base visual e os componentes acessíveis definidos na Fase 4.
2. Escrever e validar o script de migração contra o acervo revisado.
3. Criar testes de cópia, quiz e rota depois que o aplicativo existir.
4. Confirmar visibilidade do repositório antes de configurar GitHub Pages.
