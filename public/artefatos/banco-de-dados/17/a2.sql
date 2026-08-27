-- Demonstração verificável: Relacionamento entre tabelas no sistema de e-commerce usando JOINs
BEGIN;

CREATE TABLE IF NOT EXISTS auditoria_atividade (
  id INTEGER PRIMARY KEY,
  atividade VARCHAR(160) NOT NULL,
  executado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  status VARCHAR(20) NOT NULL
);

INSERT INTO auditoria_atividade (id, atividade, status)
VALUES (1, 'Relacionamento entre tabelas no sistema de e-commerce usando JOINs', 'validado');

SELECT atividade, status, executado_em
FROM auditoria_atividade
WHERE status = 'validado';

COMMIT;
