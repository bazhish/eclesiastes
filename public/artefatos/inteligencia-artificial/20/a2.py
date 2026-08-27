from dataclasses import dataclass


@dataclass(frozen=True)
class Resultado:
    atividade: str
    status: str
    evidencia: str


def executar(evidencia: str = "execução controlada") -> Resultado:
    if not evidencia.strip():
        raise ValueError("evidência obrigatória")
    return Resultado("Aula 3- Persistencia de Memoria - 82925", "ok", evidencia.strip())
