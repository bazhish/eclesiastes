'use strict';

function validarEntrada(valor) {
  if (typeof valor !== 'string' || !valor.trim()) throw new TypeError('entrada obrigatória');
  return valor.trim();
}

function executar(entrada = 'evidência registrada') {
  return { atividade: 'Implementação de CORS (cross-origin resource sharing - compartilhamento de recursos entre origens)', entrada: validarEntrada(entrada), status: 'ok' };
}

module.exports = { executar, validarEntrada };
