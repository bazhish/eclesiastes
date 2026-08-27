from dataclasses import dataclass


@dataclass(frozen=True)
class Resultado:
    atividade: str
    status: str
    evidencia: str


def executar(evidencia: str = "execução controlada") -> Resultado:
    if not evidencia.strip():
        raise ValueError("evidência obrigatória")
    return Resultado("Aula 3- Ferramenta scikit-learn – Fluxo Basico - 84110", "ok", evidencia.strip())
