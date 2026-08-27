'use strict';

function validarEntrada(valor) {
  if (typeof valor !== 'string' || !valor.trim()) throw new TypeError('entrada obrigatória');
  return valor.trim();
}

function executar(entrada = 'evidência registrada') {
  return { atividade: 'Integrações poderosas – API e SDK', entrada: validarEntrada(entrada), status: 'ok' };
}

module.exports = { executar, validarEntrada };
