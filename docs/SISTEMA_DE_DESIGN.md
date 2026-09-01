# Sistema de design do Eclesiastes

## Direção

O Eclesiastes é uma ferramenta de consulta acadêmica serena e precisa. A navegação continua familiar — matéria, bimestre, semana e aula — mas a identidade própria nasce da teia Ananse Ntentan: conexões visíveis, hierarquia clara e conhecimento construído por camadas.

## Marca e cor

- Marca: SVG original, geométrico e vetorial; elementos decorativos usam a mesma ideia de rede sem reproduzir uma arte existente.
- Claro: fundo marfim, texto índigo profundo, ações índigo e detalhes cobre.
- Escuro: índigo noturno, texto marfim e cobre claro.
- `accent` e `copper` mantêm contraste AA nas ações e não são o único indicador de estado.

## Tipografia e espaço

- Corpo: `Inter`, `ui-sans-serif`, `system-ui`, `sans-serif`, 16 px e entrelinha 1.65.
- Títulos: Georgia/Cambria como família de leitura, escala fluida e entrelinha curta.
- Espaçamento: 4, 8, 12, 16, 24, 32, 48 e 64 px.
- Cartões: raio de 12 px, borda como separação padrão e sombra discreta.

## Acessibilidade e movimento

- Foco perceptível de 3 px em cobre, com offset de 3 px.
- Landmarks semânticos e nomes acessíveis para controles, cópia e marca decorativa.
- Cópia anuncia sucesso ou instrução alternativa em região `aria-live`.
- `prefers-reduced-motion: reduce` remove transições e rolagem animada.
- A navegação mobile continua operável por teclado e informa seu estado com `aria-expanded`.
