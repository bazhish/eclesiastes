"""Generate Eclesiastes pages from the reviewed weekly Markdown in Gabarito.

The source directory is read-only. This script only rewrites generated MDX files
inside the project and updates the audit index.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import unicodedata
from collections import defaultdict
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = Path(r"C:\Users\MAX\Desktop\Gabarito")
SOURCE = Path(os.environ.get("ECLESIASTES_SOURCE_DIR", DEFAULT_SOURCE)).expanduser()
CONTENT = PROJECT / "src" / "content" / "aulas"
INDEX = PROJECT / "docs" / "source-index.json"

WEEK_RE = re.compile(r"Semana\s*(\d+)", re.IGNORECASE)
H2_RE = re.compile(r"^##\s+(.+?)\s*$")
H3_RE = re.compile(r"^###\s+(.+?)\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
PAUSE_LESSON_RE = re.compile(r"\bS\d+\s*A(\d+)", re.IGNORECASE)
PAUSE_TITLE_LESSON_RE = re.compile(r"Pause e Responda\s*[-–—]\s*Aula\s*(\d+)", re.IGNORECASE)
ACTIVITY_LESSON_RE = re.compile(r"^(?:Atividade Prática\s*[-–—]\s*)?Aula\s*(\d+)\b", re.IGNORECASE)


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", value)).strip("-")


def read_markdown(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def source_path(path: Path) -> str:
    return f"gabarito/{path.relative_to(SOURCE).as_posix()}"


def number_from(value: str, pattern: re.Pattern[str], label: str) -> int:
    match = pattern.search(value)
    if not match:
        raise RuntimeError(f"Não foi possível localizar {label} em: {value}")
    return int(match.group(1))


def reset_generated_directory(path: Path) -> None:
    resolved = path.resolve()
    if resolved != CONTENT.resolve() or PROJECT.resolve() not in resolved.parents:
        raise RuntimeError(f"Diretório gerado inválido: {path}")
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def semantic_h2_kind(title: str) -> str | None:
    lower = title.lower()
    if re.match(r"^Semana\s+\d+\b", title, re.IGNORECASE):
        return "semana"
    if lower.startswith("pause e responda"):
        return "pausa"
    if lower.startswith("atividades práticas"):
        return "atividade-generica"
    if ACTIVITY_LESSON_RE.match(title):
        return "atividade"
    if lower == "registro de aula":
        return "registro"
    if lower == "observações":
        return "observacao"
    return None


def match_with_offsets(match: re.Match[str], line_offset: int) -> re.Match[str]:
    class OffsetMatch:
        def __init__(self, original: re.Match[str], offset: int) -> None:
            self.original = original
            self.offset = offset

        def group(self, *args):
            return self.original.group(*args)

        def start(self, group: int = 0) -> int:
            return self.offset + self.original.start(group)

        def end(self, group: int = 0) -> int:
            return self.offset + self.original.end(group)

    return OffsetMatch(match, line_offset)  # type: ignore[return-value]


def heading_matches(markdown: str, pattern: re.Pattern[str]) -> list[re.Match[str]]:
    matches: list[re.Match[str]] = []
    offset = 0
    fenced = False
    for line in markdown.splitlines(keepends=True):
        if FENCE_RE.match(line):
            fenced = not fenced
        if not fenced:
            match = pattern.match(line.rstrip("\n"))
            if match:
                matches.append(match_with_offsets(match, offset))
        offset += len(line)
    return matches


def line_end_after(markdown: str, position: int) -> int:
    end = markdown.find("\n", position)
    return len(markdown) if end == -1 else end + 1


def clean_block(content: str) -> str:
    return content.strip("\n")


def semantic_sections(markdown: str) -> list[dict[str, str | int]]:
    candidates = []
    for match in heading_matches(markdown, H2_RE):
        title = match.group(1).strip()
        kind = semantic_h2_kind(title)
        if kind:
            candidates.append({"title": title, "kind": kind, "start": match.start(), "body_start": line_end_after(markdown, match.start())})

    sections = []
    for index, item in enumerate(candidates):
        end = candidates[index + 1]["start"] if index + 1 < len(candidates) else len(markdown)
        sections.append({**item, "content": clean_block(markdown[int(item["body_start"]): int(end)])})
    return sections


def week_topic(markdown: str, fallback: str) -> str:
    for match in heading_matches(markdown, H2_RE):
        title = match.group(1).strip()
        if re.match(r"^Semana\s+\d+\b", title, re.IGNORECASE):
            return re.sub(r"^Semana\s+\d+\s*[-–—]\s*", "", title, flags=re.IGNORECASE).strip()
    first = re.search(r"^#\s+(.+?)\s*$", markdown, re.MULTILINE)
    if first:
        title = re.sub(r"^Semana\s+\d+\s*[-–—]\s*", "", first.group(1), flags=re.IGNORECASE).strip()
        return title.split(":", 1)[1].strip() if ":" in title else title
    return fallback


def existing_lesson_map() -> dict[tuple[str, int], dict[str, list[int]]]:
    mapping: dict[tuple[str, int], dict[str, list[int]]] = defaultdict(lambda: {"a": [], "q": []})
    if not CONTENT.exists():
        return mapping
    for path in CONTENT.rglob("*.mdx"):
        text = path.read_text(encoding="utf-8")
        match = re.match(r"^---\r?\n([\s\S]+?)\r?\n---", text)
        if not match:
            continue
        data = json.loads(match.group(1))
        lesson = re.match(r"([aq])(\d+)$", data.get("aula", ""))
        if lesson:
            mapping[(data["materiaSlug"], int(data["semana"]))][lesson.group(1)].append(int(lesson.group(2)))
    for item in mapping.values():
        item["a"] = sorted(set(item["a"]))
        item["q"] = sorted(set(item["q"]))
    return mapping


def split_pause_blocks(section: dict[str, str | int], old_q_lessons: list[int]) -> dict[int, list[dict[str, str]]]:
    title = str(section["title"])
    content = str(section["content"])
    explicit_title_lesson = PAUSE_TITLE_LESSON_RE.search(title)
    h3_matches = heading_matches(content, H3_RE)
    grouped: dict[int, list[dict[str, str]]] = defaultdict(list)

    coded = []
    for index, match in enumerate(h3_matches):
        h3_title = match.group(1).strip()
        lesson_match = PAUSE_LESSON_RE.search(h3_title)
        if not lesson_match:
            continue
        end = h3_matches[index + 1].start() if index + 1 < len(h3_matches) else len(content)
        coded.append((int(lesson_match.group(1)), h3_title, clean_block(content[match.start():end])))

    if coded:
        for lesson, h3_title, block in coded:
            grouped[lesson].append({"titulo": h3_title, "conteudo": block})
        return grouped

    lesson = int(explicit_title_lesson.group(1)) if explicit_title_lesson else (old_q_lessons[0] if old_q_lessons else 1)
    grouped[lesson].append({"titulo": title, "conteudo": content})
    return grouped


def split_week_h3_pause(section: dict[str, str | int], old_q_lessons: list[int]) -> dict[int, list[dict[str, str]]]:
    content = str(section["content"])
    for match in heading_matches(content, H3_RE):
        title = match.group(1).strip()
        title_lesson = PAUSE_TITLE_LESSON_RE.search(title)
        if not title_lesson and not title.lower().startswith("pause e responda"):
            continue
        lesson = int(title_lesson.group(1)) if title_lesson else (old_q_lessons[0] if old_q_lessons else 1)
        block = clean_block(content[match.start():])
        return {lesson: [{"titulo": title, "conteudo": block}]}
    return {}


def activity_lesson(title: str, old_a_lessons: list[int]) -> int:
    match = ACTIVITY_LESSON_RE.match(title)
    if match:
        return int(match.group(1))
    return old_a_lessons[0] if old_a_lessons else 1


def make_activity(title: str, content: str, source: str) -> dict:
    return {
        "titulo": title,
        "enunciado": content,
        "resposta": content,
        "conteudo": content,
        "fonte": source,
        "arquivos": [],
    }


def write_mdx(data: dict, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(f"---\n{json.dumps(data, ensure_ascii=False)}\n---\n", encoding="utf-8")


def add_record(records: list[dict], data: dict, output: Path, source_file: Path, source_ref: str, extra: dict | None = None) -> None:
    record = {
        "tipo": data["tipo"],
        "fonte": source_ref,
        "arquivoFonte": source_path(source_file),
        "pagina": output.relative_to(PROJECT).as_posix(),
        "rota": f"/{data['materiaSlug']}/{data['bimestre']}/semana-{data['semana']}/{data['aula']}",
    }
    if extra:
        record.update(extra)
    records.append(record)


def main() -> None:
    if not SOURCE.is_dir():
        raise RuntimeError(f"Fonte não encontrada: {SOURCE}. Defina ECLESIASTES_SOURCE_DIR se necessário.")

    old_lessons = existing_lesson_map()
    reset_generated_directory(CONTENT)
    records: list[dict] = []
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
            markdown_files = sorted(week_dir.glob("*.md"))
            if len(markdown_files) != 1:
                raise RuntimeError(f"Esperado um único Markdown em {week_dir}; encontrados {len(markdown_files)}")

            source_file = markdown_files[0]
            markdown = read_markdown(source_file)
            topic = week_topic(markdown, f"Semana {week}")
            sections = semantic_sections(markdown)
            destination_root = CONTENT / subject_slug / f"semana-{week}"
            lesson_defaults = old_lessons.get((subject_slug, week), {"a": [], "q": []})

            for section in sections:
                kind = str(section["kind"])
                title = str(section["title"])
                content = str(section["content"])
                if kind == "semana":
                    pause_groups = split_week_h3_pause(section, lesson_defaults["q"])
                    for lesson, blocks in sorted(pause_groups.items()):
                        source_ref = f"{source_path(source_file)}#pause-e-responda-aula-{lesson}"
                        quizzes = [
                            {
                                "pergunta": block["titulo"],
                                "resposta": block["conteudo"],
                                "titulo": block["titulo"],
                                "conteudo": block["conteudo"],
                                "fonte": f"{source_ref}-{index + 1}",
                            }
                            for index, block in enumerate(blocks)
                        ]
                        data = {
                            "materia": subject,
                            "materiaSlug": subject_slug,
                            "bimestre": 3,
                            "semana": week,
                            "ordem": lesson * 10 + 5,
                            "aula": f"q{lesson}",
                            "titulo": f"{topic} · Pause e Responda · Aula {lesson}",
                            "tipo": "pausa",
                            "quizzes": quizzes,
                        }
                        output = destination_root / f"q{lesson}.mdx"
                        write_mdx(data, output)
                        add_record(records, data, output, source_file, source_ref, {"questoes": len(quizzes)})
                        counts["pausas"] += 1
                        counts["questoes"] += len(quizzes)
                        counts["documentos"] += 1
                    continue

                if kind == "pausa":
                    pause_groups = split_pause_blocks(section, lesson_defaults["q"])
                    for lesson, blocks in sorted(pause_groups.items()):
                        source_ref = f"{source_path(source_file)}#pause-e-responda-aula-{lesson}"
                        quizzes = [
                            {
                                "pergunta": block["titulo"],
                                "resposta": block["conteudo"],
                                "titulo": block["titulo"],
                                "conteudo": block["conteudo"],
                                "fonte": f"{source_ref}-{index + 1}",
                            }
                            for index, block in enumerate(blocks)
                        ]
                        data = {
                            "materia": subject,
                            "materiaSlug": subject_slug,
                            "bimestre": 3,
                            "semana": week,
                            "ordem": lesson * 10 + 5,
                            "aula": f"q{lesson}",
                            "titulo": f"{topic} · Pause e Responda · Aula {lesson}",
                            "tipo": "pausa",
                            "quizzes": quizzes,
                        }
                        output = destination_root / f"q{lesson}.mdx"
                        write_mdx(data, output)
                        add_record(records, data, output, source_file, source_ref, {"questoes": len(quizzes)})
                        counts["pausas"] += 1
                        counts["questoes"] += len(quizzes)
                        counts["documentos"] += 1
                    continue

                if kind in {"atividade", "atividade-generica"}:
                    lesson = activity_lesson(title, lesson_defaults["a"])
                    source_ref = f"{source_path(source_file)}#{slugify(title)}"
                    data = {
                        "materia": subject,
                        "materiaSlug": subject_slug,
                        "bimestre": 3,
                        "semana": week,
                        "ordem": lesson * 10,
                        "aula": f"a{lesson}",
                        "titulo": f"{topic} · Aula {lesson}",
                        "atividade": make_activity(title, content, source_ref),
                        "tipo": "roteiro",
                        "quizzes": [],
                    }
                    output = destination_root / f"a{lesson}.mdx"
                    write_mdx(data, output)
                    add_record(records, data, output, source_file, source_ref, {"conteudoSha256": hashlib.sha256(content.encode("utf-8")).hexdigest(), "arquivosCodigo": 0})
                    counts["roteiros"] += 1
                    counts["documentos"] += 1
                    continue

                if kind in {"registro", "observacao"}:
                    route_prefix = "r" if kind == "registro" else "o"
                    label = "Registro de Aula" if kind == "registro" else "Observações"
                    source_ref = f"{source_path(source_file)}#{slugify(label)}"
                    data = {
                        "materia": subject,
                        "materiaSlug": subject_slug,
                        "bimestre": 3,
                        "semana": week,
                        "ordem": 900 if kind == "registro" else 950,
                        "aula": f"{route_prefix}1",
                        "titulo": f"{topic} · {label}",
                        "atividade": make_activity(label, content, source_ref),
                        "tipo": kind,
                        "quizzes": [],
                    }
                    output = destination_root / f"{route_prefix}1.mdx"
                    write_mdx(data, output)
                    add_record(records, data, output, source_file, source_ref, {"conteudoSha256": hashlib.sha256(content.encode("utf-8")).hexdigest(), "arquivosCodigo": 0})
                    counts["registros" if kind == "registro" else "observacoes"] += 1
                    counts["documentos"] += 1

    INDEX.parent.mkdir(parents=True, exist_ok=True)
    INDEX.write_text(
        json.dumps(
            {
                "fonte": str(SOURCE),
                "contagens": {
                    **dict(counts),
                    "atividadesComCodigo": 0,
                    "arquivosCodigo": 0,
                    "entradasTecnicasExcluidas": 0,
                    "entradasExcluidas": 0,
                },
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
        f"registros: {counts['registros']}; observações: {counts['observacoes']}."
    )


if __name__ == "__main__":
    main()
