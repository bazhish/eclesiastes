from dataclasses import dataclass


@dataclass(frozen=True)
class Resultado:
    atividade: str
    status: str
    evidencia: str


def executar(evidencia: str = "execução controlada") -> Resultado:
    if not evidencia.strip():
        raise ValueError("evidência obrigatória")
    return Resultado("Desenvolvimento de módulo de triagem: regras vs. LLM", "ok", evidencia.strip())
