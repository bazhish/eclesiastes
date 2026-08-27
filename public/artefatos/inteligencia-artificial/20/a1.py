from dataclasses import dataclass


@dataclass(frozen=True)
class Resultado:
    atividade: str
    status: str
    evidencia: str


def executar(evidencia: str = "execução controlada") -> Resultado:
    if not evidencia.strip():
        raise ValueError("evidência obrigatória")
    return Resultado("Aula 2- Bancos de Vetores - 82920", "ok", evidencia.strip())
