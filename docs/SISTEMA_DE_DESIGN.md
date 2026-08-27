# Sistema de design do Gabarito

## Direção

O Gabarito deve parecer uma ferramenta de consulta acadêmica própria: sereno, preciso e fácil de percorrer por longos períodos. A estrutura remete ao modelo mental do AVA, mas a aparência não imita seus cabeçalhos, cores, logotipo, ícones ou cartões.

Princípios: hierarquia antes de decoração; a resposta é a ação principal; estados precisam ser compreensíveis sem depender de cor; modo escuro deve ser uma variação de tokens, não uma segunda interface.

## Tokens

### Cor

| Papel | Claro | Escuro | Uso |
|---|---|---|---|
| `canvas` | `#F6F8FC` | `#0F1521` | fundo da aplicação |
| `surface` | `#FFFFFF` | `#182131` | cartões e áreas de leitura |
| `surface-subtle` | `#EEF2F8` | `#222D40` | navegação e áreas secundárias |
| `text` | `#172033` | `#F2F5FA` | texto principal |
| `text-muted` | `#52607A` | `#B6C2D8` | metadados e apoio |
| `border` | `#D8E0EC` | `#344258` | contornos e divisores |
| `accent` | `#3159B7` | `#8EAEFF` | links, foco e ação principal |
| `accent-strong` | `#243F87` | `#BED0FF` | hover e ênfase |
| `success` | `#1F7A4D` | `#66D69A` | feedback de cópia |
| `warning` | `#9A5D00` | `#FFCD70` | conteúdo a personalizar |

`accent` sobre `surface` e texto claro sobre `accent` precisam manter contraste mínimo AA. Cor não é o único sinal para sucesso, aviso, item atual ou alternativa correta: cada estado recebe também texto, ícone com nome acessível ou borda.

### Tipografia

- Família: `Inter`, `ui-sans-serif`, `system-ui`, `sans-serif`.
- Texto: 16 px, entrelinha 1.6.
- Títulos: 32/40 px para página, 22/30 px para seções, 18/26 px para cartões.
- Código: `ui-monospace`, `SFMono-Regular`, `Consolas`, `monospace`, 14 px, entrelinha 1.6.
- Peso: 400 para leitura, 600 para hierarquia e controles; evitar peso 700 fora de títulos de página.

### Espaço, borda e movimento

- Escala: 4, 8, 12, 16, 24, 32, 48 e 64 px.
- Raio: 10 px em cartões e 8 px em controles; não usar pílulas para blocos de conteúdo.
- Sombra: uma camada leve somente em cartões elevados; borda é a separação padrão.
- Movimento: 160 ms para microinterações e 220 ms para expansão. Com `prefers-reduced-motion: reduce`, nenhuma expansão deve deslocar a tela de forma animada.

## Componentes

### `Sidebar/TreeNav`

Árvore de matérias, semanas e aulas com o item atual destacado por fundo sutil, borda lateral e texto. Matérias e semanas expansíveis usam botões, não links vazios.

| Estado | Comportamento |
|---|---|
| Fechado | mostra somente o nível atual |
| Aberto | expõe o próximo nível e atualiza `aria-expanded` |
| Atual | `aria-current="page"`, fundo e borda de acento |
| Mobile | painel modal lateral com foco contido e botão “Fechar navegação” |

Teclado: `Tab` percorre controles; `Enter` e `Space` expandem; `Escape` fecha o painel mobile. A primeira versão não adotará navegação por setas de treeview até haver suporte completo a ARIA tree; botões comuns são mais claros e robustos.

### `Breadcrumb`

Lista navegável de contexto. Apenas os ancestrais são links; o item atual usa `aria-current="page"`. Em telas pequenas, o primeiro ancestral e o item atual permanecem visíveis; o miolo pode ser truncado visualmente, nunca removido da leitura assistiva.

### `AtividadeCard`

Cartão de leitura com quatro áreas fixas: enunciado, resposta, artefato técnico e checklist. A resposta usa superfície contrastante e rótulo “Resposta para consulta”; o cartão não se apresenta como envio ao AVA nem exibe nota.

### `CopyButton`

Botão secundário, ícone de cópia mais rótulo visível. No sucesso, mantém largura e muda para “Copiado”; um `aria-live="polite"` anuncia “Resposta copiada para a área de transferência”. Se a Clipboard API falhar, exibe instrução para selecionar o texto e copiar manualmente. Nunca depende de hover ou mouse.

### `QuizBlock`

Bloco com pergunta e botão “Mostrar resposta”. Como as fontes preservadas registram pergunta e gabarito, mas não as alternativas completas, o componente não inventa opções: revela uma “Resposta de referência”, não copiável, com borda de sucesso e justificativa quando disponível.

### Busca e filtro

Campo de busca com label visível, botão de limpar e resultado em texto: “12 aulas encontradas”. Filtro de matéria e semana usa controles nativos. Resultado vazio descreve como remover filtros; não usa apenas ícone.

## Layout responsivo

| Largura | Composição |
|---|---|
| Até 767 px | cabeçalho compacto, árvore em painel lateral, uma coluna |
| 768–1023 px | árvore recolhível, conteúdo com largura confortável |
| 1024 px ou mais | árvore fixa à esquerda, conteúdo de até 860 px e painel opcional de contexto |

Linhas de resposta devem ter largura máxima de aproximadamente 75 caracteres. Código pode rolar horizontalmente dentro do próprio bloco, sem causar rolagem horizontal da página.

## Matriz de acessibilidade

| Requisito | Decisão |
|---|---|
| Foco | `:focus-visible` de 3 px em cor de acento e offset de 2 px |
| Semântica | landmarks para cabeçalho, navegação, conteúdo e rodapé; headings sem saltos |
| Teclado | todos os controles operáveis sem mouse |
| Leitor de tela | estados de cópia, expansão e resposta revelada anunciados |
| Contraste | tokens verificados como AA para texto e controles principais |
| Movimento | respeita preferência reduzida |
| Tema | preferência persistida localmente e opção “usar sistema” |

## Não fazer

- Não reproduzir cores, marcas, ícones, imagens, textos institucionais ou layout literal do AVA.
- Não usar cor verde isoladamente para afirmar que uma alternativa está correta.
- Não esconder o único botão de cópia em hover.
- Não manter o conteúdo do quiz em um modal que interrompa a navegação por teclado.
- Não apresentar respostas como se fossem comprovadamente enviadas, aprovadas ou avaliadas.
