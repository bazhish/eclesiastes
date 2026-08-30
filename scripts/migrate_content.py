"""Generate the Eclesiastes content collection from the reviewed Gabarito.

The source is deliberately read-only. Generated MDX, downloadable ZIP artifacts
and the audit index stay inside this repository.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import unicodedata
import zipfile
from collections import defaultdict
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = PROJECT.parent.parent / "Desenvolvimento de Sistemas - Gabarito" / "gabarito"
SOURCE = Path(os.environ.get("ECLESIASTES_SOURCE_DIR", DEFAULT_SOURCE)).expanduser()
CONTENT = PROJECT / "src" / "content" / "aulas"
PUBLIC_ARTIFACTS = PROJECT / "public" / "artefatos"
INDEX = PROJECT / "docs" / "source-index.json"

WEEK_RE = re.compile(r"Semana\s*(\d+)", re.IGNORECASE)
LESSON_RE = re.compile(
    r"^Gabarito\s*[-—]\s*(?P<kind>Roteiro Prático|Pausa e Responda)\s*Aula\s*(?P<lesson>\d+)\.md$",
    re.IGNORECASE,
)
ANSWER_HEADING_RE = re.compile(r"^###\s*Resposta\s*$", re.IGNORECASE)
GENERIC_QUESTION_HEADING_RE = re.compile(r"^##\s*(?:Questão\s*\d+|\d+\.\s*Enunciado)\s*$", re.IGNORECASE)


def normalize(value: str) -> str:
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in value.replace("\r", "").split("\n")]
    compact: list[str] = []
    for line in lines:
        if line or (compact and compact[-1]):
            compact.append(line)
    return "\n".join(compact).strip()


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", value)).strip("-")


def source_path(path: Path) -> str:
    return f"gabarito/{path.relative_to(SOURCE).as_posix()}"


def number_from(value: str, pattern: re.Pattern[str], label: str) -> int:
    match = pattern.search(value)
    if not match:
        raise RuntimeError(f"Não foi possível localizar {label} em: {value}")
    return int(match.group(1))


def read_markdown(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").strip() + "\n"


def without_h1(markdown: str) -> str:
    return re.sub(r"^#\s+[^\n]+\n+", "", markdown, count=1).strip()


def section(markdown: str, headings: tuple[str, ...]) -> str:
    """Return an H2 section body, accepting the source's editorial variants."""
    names = "|".join(re.escape(name) for name in headings)
    match = re.search(rf"^##\s*(?:{names})\s*$", markdown, re.IGNORECASE | re.MULTILINE)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^##\s+", markdown[start:], re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(markdown)
    return markdown[start:end].strip()


def topic_from_week(path: Path, week: int) -> str:
    label = re.sub(rf"^Semana\s*{week}\s*-\s*", "", path.name, flags=re.IGNORECASE).strip()
    return label or f"Semana {week}"


def parse_practical(markdown: str) -> tuple[str, str, str]:
    full_content = without_h1(markdown)
    enunciado = section(markdown, ("Enunciado", "Situação-problema", "Contexto"))
    resposta = section(markdown, ("Resposta", "Respostas", "Tarefas e respostas", "Respostas da etapa 2", "Código entregue"))
    if not enunciado:
        enunciado = full_content
    if not resposta:
        resposta = full_content
    return normalize(enunciado), normalize(resposta), full_content


def parse_quiz(markdown: str, source: str) -> list[dict[str, str]]:
    """Parse all answer pairs while retaining source wording and topic context."""
    lines = markdown.splitlines()
    answers = [index for index, line in enumerate(lines) if ANSWER_HEADING_RE.match(line)]
    quizzes: list[dict[str, str]] = []
    previous_answer_end = 0

    for answer_index in answers:
        heading_indexes = [index for index in range(previous_answer_end, answer_index) if lines[index].startswith("## ")]
        question_start = heading_indexes[-1] if heading_indexes else previous_answer_end
        question_lines = lines[question_start:answer_index]
        if question_lines and GENERIC_QUESTION_HEADING_RE.match(question_lines[0]):
            question_lines = question_lines[1:]
        question = normalize("\n".join(question_lines))

        next_h2 = next((index for index in range(answer_index + 1, len(lines)) if lines[index].startswith("## ")), len(lines))
        answer = normalize("\n".join(lines[answer_index + 1:next_h2]))
        if not question or not answer:
            raise RuntimeError(f"Questão ou resposta ausente em {source}")
        quizzes.append({"pergunta": question, "resposta": answer, "fonte": source})
        previous_answer_end = next_h2

    if not quizzes:
        raise RuntimeError(f"Nenhuma resposta identificada em {source}")
    return quizzes


def write_mdx(data: dict, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(f"---\n{json.dumps(data, ensure_ascii=False)}\n---\n", encoding="utf-8")


def reset_generated_directory(path: Path) -> None:
    resolved = path.resolve()
    allowed = {CONTENT.resolve(), PUBLIC_ARTIFACTS.resolve()}
    if resolved not in allowed or PROJECT.resolve() not in resolved.parents:
        raise RuntimeError(f"Diretório gerado inválido: {path}")
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def archive_artifact(directory: Path, subject_slug: str, week: int, lesson: int) -> dict[str, str | int]:
    files = sorted(path for path in directory.rglob("*") if path.is_file())
    if not files:
        raise RuntimeError(f"Artefato vazio: {directory}")
    destination = PUBLIC_ARTIFACTS / subject_slug / f"semana-{week}" / f"a{lesson}.zip"
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
        for file in files:
            archive.write(file, file.relative_to(directory).as_posix())
    return {
        "nome": f"Artefatos da Aula {lesson}",
        "href": f"artefatos/{subject_slug}/semana-{week}/a{lesson}.zip",
        "arquivos": len(files),
    }


def main() -> None:
    if not SOURCE.is_dir():
        raise RuntimeError(
            "Fonte não encontrada: "
            f"{SOURCE}. Defina ECLESIASTES_SOURCE_DIR com o caminho da pasta gabarito."
        )

    reset_generated_directory(CONTENT)
    reset_generated_directory(PUBLIC_ARTIFACTS)
    records: list[dict[str, str | int | bool]] = []
    expected_artifacts: set[str] = set()
    archived_artifacts: set[str] = set()
    counts = defaultdict(int)

    for subject_dir in sorted(path for path in SOURCE.iterdir() if path.is_dir()):
        subject = subject_dir.name
        subject_slug = slugify(subject)
        term_dirs = [path for path in subject_dir.iterdir() if path.is_dir() and path.name.startswith("3")]
        if len(term_dirs) != 1:
            raise RuntimeError(f"Bimestre 3 ambíguo para {subject}: {term_dirs}")

        week_dirs = sorted(
            (path for path in term_dirs[0].iterdir() if path.is_dir() and WEEK_RE.search(path.name)),
            key=lambda path: number_from(path.name, WEEK_RE, "Semana"),
        )
        for week_dir in week_dirs:
            week = number_from(week_dir.name, WEEK_RE, "Semana")
            topic = topic_from_week(week_dir, week)
            documents: list[tuple[Path, re.Match[str]]] = []
            for path in week_dir.glob("Gabarito - *.md"):
                match = LESSON_RE.match(path.name)
                if not match:
                    raise RuntimeError(f"Documento de gabarito fora do padrão: {path}")
                documents.append((path, match))

            for path, match in sorted(documents, key=lambda item: (int(item[1]["lesson"]), item[1]["kind"])):
                kind = match["kind"].casefold()
                lesson = int(match["lesson"])
                markdown = read_markdown(path)
                source = source_path(path)
                destination_root = CONTENT / subject_slug / f"semana-{week}"

                if kind == "roteiro prático":
                    artifact_dir = week_dir / "codigo" / f"aula-{lesson}"
                    artifact = None
                    if artifact_dir.is_dir():
                        key = source_path(artifact_dir)
                        expected_artifacts.add(key)
                        artifact = archive_artifact(artifact_dir, subject_slug, week, lesson)
                        archived_artifacts.add(key)
                    enunciado, resposta, conteudo = parse_practical(markdown)
                    data = {
                        "materia": subject,
                        "materiaSlug": subject_slug,
                        "bimestre": 3,
                        "semana": week,
                        "ordem": lesson * 10,
                        "aula": f"a{lesson}",
                        "titulo": f"{topic} · Aula {lesson}",
                        "atividade": {
                            "enunciado": enunciado,
                            "resposta": resposta,
                            "conteudo": conteudo,
                            "fonte": source,
                            **({"artefato": artifact} if artifact else {}),
                        },
                        "quizzes": [],
                    }
                    output = destination_root / f"a{lesson}.mdx"
                    write_mdx(data, output)
                    records.append({
                        "tipo": "roteiro",
                        "fonte": source,
                        "pagina": output.relative_to(PROJECT).as_posix(),
                        "rota": f"/{subject_slug}/3/semana-{week}/a{lesson}",
                        "artefato": bool(artifact),
                    })
                    counts["roteiros"] += 1
                    counts["documentos"] += 1
                else:
                    quizzes = parse_quiz(markdown, source)
                    data = {
                        "materia": subject,
                        "materiaSlug": subject_slug,
                        "bimestre": 3,
                        "semana": week,
                        "ordem": lesson * 10 + 5,
                        "aula": f"q{lesson}",
                        "titulo": f"{topic} · Pausa e Responda · Aula {lesson}",
                        "quizzes": quizzes,
                    }
                    output = destination_root / f"q{lesson}.mdx"
                    write_mdx(data, output)
                    records.append({
                        "tipo": "pausa",
                        "fonte": source,
                        "pagina": output.relative_to(PROJECT).as_posix(),
                        "rota": f"/{subject_slug}/3/semana-{week}/q{lesson}",
                        "questoes": len(quizzes),
                    })
                    counts["pausas"] += 1
                    counts["questoes"] += len(quizzes)
                    counts["documentos"] += 1

    all_artifact_dirs = {
        source_path(path)
        for path in SOURCE.rglob("aula-*")
        if path.is_dir() and path.parent.name == "codigo"
    }
    if all_artifact_dirs != expected_artifacts or expected_artifacts != archived_artifacts:
        missing = sorted(all_artifact_dirs - archived_artifacts)
        unexpected = sorted(archived_artifacts - all_artifact_dirs)
        raise RuntimeError(f"Mapeamento de artefatos inconsistente. Ausentes: {missing}; inesperados: {unexpected}")

    INDEX.parent.mkdir(parents=True, exist_ok=True)
    INDEX.write_text(
        json.dumps(
            {
                "fonte": str(SOURCE),
                "contagens": dict(counts),
                "registros": records,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        f"Documentos: {counts['documentos']}; roteiros: {counts['roteiros']}; "
        f"pausas: {counts['pausas']}; questões: {counts['questoes']}; "
        f"artefatos: {len(archived_artifacts)}"
    )


if __name__ == "__main__":
    main()
