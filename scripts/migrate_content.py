"""Migrate the concise R3B study records into short, static Astro content paths.

The source repository is read-only for this migration. It creates one MDX record
per activity and one record for the weekly "Pause e Responda" answer key.
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT.parent / "R3B" / "materias"
CONTENT = PROJECT / "src" / "content" / "aulas"
PUBLIC_ARTIFACTS = PROJECT / "public" / "artefatos"


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def plain_markdown(value: str) -> str:
    value = re.sub(r"^#{1,6}\s+", "", value, flags=re.MULTILINE)
    value = re.sub(r"\*\*(.*?)\*\*", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"^[-*]\s+", "• ", value, flags=re.MULTILINE)
    return value.strip()


def section(text: str, start: str, end: str | None = None) -> str:
    pattern = rf"^## {re.escape(start)}\s*$([\s\S]*?)(?=^## {re.escape(end)}\s*$|\Z)" if end else rf"^## {re.escape(start)}\s*$([\s\S]*)"
    match = re.search(pattern, text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def activity_data(path: Path, subject_slug: str, week: int, order: int) -> dict:
    text = path.read_text(encoding="utf-8")
    title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    source_match = re.search(r"Roteiro analisado:\s*(.+)$", text, re.MULTILINE)
    artifact_match = re.search(r"\[[^\]]+\]\(codigo/([^)]+)\)", text)
    artifact = None
    if artifact_match:
        original = path.parent / "codigo" / artifact_match.group(1)
        if original.is_file():
            short_name = f"a{order}{original.suffix.lower()}"
            relative_public = Path(subject_slug) / str(week) / short_name
            destination = PUBLIC_ARTIFACTS / relative_public
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(original, destination)
            language = {".js": "javascript", ".jsx": "jsx", ".py": "python", ".sql": "sql", ".html": "html", ".css": "css", ".ts": "typescript", ".sh": "bash"}.get(original.suffix.lower(), "text")
            artifact = {"linguagem": language, "conteudo": original.read_text(encoding="utf-8"), "url": f"/artefatos/{relative_public.as_posix()}"}
    return {
        "bimestre": 3,
        "semana": week,
        "ordem": order,
        "aula": f"a{order}",
        "titulo": title_match.group(1).strip() if title_match else path.stem,
        "atividade": {
            "enunciado": clean(f"Roteiro analisado: {source_match.group(1) if source_match else path.name}. {plain_markdown(section(text, 'Solução proposta', 'Perguntas do roteiro e respostas'))}"),
            "resposta": plain_markdown(section(text, "Perguntas do roteiro e respostas", "Artefato técnico")) or "Consulte o roteiro da atividade e registre sua própria evidência de execução.",
            **({"artefato": artifact} if artifact else {}),
        },
        "quizzes": [],
    }


def quiz_data(path: Path, week: int, order: int) -> dict:
    text = path.read_text(encoding="utf-8")
    subject_match = re.search(r"^# Pause e Responda — (.+?) — Semana", text, re.MULTILINE)
    quizzes = []
    for block in re.split(r"^##\s+.+$", text, flags=re.MULTILINE)[1:]:
        question = re.search(r"\*\*Pergunta:\*\*\s*(.+?)(?=\n\s*\*\*|\Z)", block, re.DOTALL)
        answer = re.search(r"\*\*Resposta correta:\*\*\s*(.+?)(?=\n\s*---|\Z)", block, re.DOTALL)
        if question and answer:
            quizzes.append({"pergunta": clean(question.group(1)), "resposta": clean(answer.group(1))})
    if not quizzes:
        raise RuntimeError(f"Nenhuma questão encontrada em {path}")
    return {"bimestre": 3, "semana": week, "ordem": order, "aula": "q", "titulo": "Pause e Responda", "quizzes": quizzes, "_materia_nome": subject_match.group(1) if subject_match else path.parent.parent.name}


def write_mdx(data: dict, destination: Path, subject_name: str, subject_slug: str) -> None:
    data["materia"] = subject_name
    data["materiaSlug"] = subject_slug
    data.pop("_materia_nome", None)
    destination.parent.mkdir(parents=True, exist_ok=True)
    body = "## Registro de consulta\n\nEste conteúdo foi migrado dos registros do 3º bimestre. Use-o para estudar, revisar e adaptar a atividade ao próprio contexto.\n"
    destination.write_text(f"---\n{json.dumps(data, ensure_ascii=False)}\n---\n\n{body}", encoding="utf-8")


def main() -> None:
    if not SOURCE.is_dir():
        raise RuntimeError(f"Fonte não encontrada: {SOURCE}")
    activity_count = quiz_count = question_count = 0
    for subject_dir in sorted(path for path in SOURCE.iterdir() if path.is_dir()):
        subject_slug = subject_dir.name
        for week_dir in sorted(subject_dir.glob("semana-*"), key=lambda path: int(path.name.split("-")[1])):
            week = int(week_dir.name.split("-")[1])
            activities = sorted(path for path in week_dir.glob("*.md") if path.name not in {"README.md", "pause-e-responda.md"})
            subject_name = None
            for order, activity in enumerate(activities, 1):
                record = activity_data(activity, subject_slug, week, order)
                header = re.search(r"^> Matéria:\s*(.+?)\s*$", activity.read_text(encoding="utf-8"), re.MULTILINE)
                subject_name = header.group(1).strip() if header else subject_slug
                write_mdx(record, CONTENT / subject_slug / f"semana-{week}" / f"a{order}.mdx", subject_name, subject_slug)
                activity_count += 1
            pause = week_dir / "pause-e-responda.md"
            if pause.is_file():
                record = quiz_data(pause, week, len(activities) + 1)
                subject_name = subject_name or record["_materia_nome"]
                question_count += len(record["quizzes"])
                write_mdx(record, CONTENT / subject_slug / f"semana-{week}" / "q.mdx", subject_name, subject_slug)
                quiz_count += 1
    print(f"Atividades: {activity_count}; gabaritos: {quiz_count}; questões: {question_count}")


if __name__ == "__main__":
    main()
