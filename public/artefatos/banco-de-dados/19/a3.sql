-- Demonstração verificável: Manipulação de dados em um banco de dados de comércio eletrônico com comandos DML
BEGIN;

CREATE TABLE IF NOT EXISTS auditoria_atividade (
  id INTEGER PRIMARY KEY,
  atividade VARCHAR(160) NOT NULL,
  executado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  status VARCHAR(20) NOT NULL
);

INSERT INTO auditoria_atividade (id, atividade, status)
VALUES (1, 'Manipulação de dados em um banco de dados de comércio eletrônico com comandos DML', 'validado');

SELECT atividade, status, executado_em
FROM auditoria_atividade
WHERE status = 'validado';

COMMIT;
