import os
import re


ALLOWED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".go",
    ".rb",
    ".php",
    ".cs",
    ".cpp",
    ".c",
    ".h",
    ".rs",
    ".kt",
    ".swift",
    ".html",
    ".css",
    ".scss",
    ".json",
    ".toml",
    ".yaml",
    ".yml",
    ".xml",
    ".ini",
    ".cfg",
    ".md",
    ".txt",
}

SKIPPED_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    "venv",
    ".venv",
    "env",
    "dist",
    "build",
    "target",
    ".next",
    ".nuxt",
    "coverage",
}

SKIPPED_FILES = {
    ".env",
}

STOP_WORDS = {
    "about",
    "after",
    "again",
    "also",
    "and",
    "any",
    "are",
    "because",
    "been",
    "before",
    "but",
    "can",
    "cannot",
    "could",
    "did",
    "does",
    "doing",
    "done",
    "for",
    "from",
    "get",
    "gets",
    "had",
    "has",
    "have",
    "how",
    "into",
    "its",
    "not",
    "now",
    "only",
    "our",
    "out",
    "please",
    "repo",
    "repository",
    "should",
    "that",
    "the",
    "their",
    "then",
    "there",
    "this",
    "too",
    "was",
    "when",
    "where",
    "which",
    "while",
    "will",
    "with",
    "would",
    "you",
    "your",
}


def _format_path(path):
    return path.replace(os.sep, "/")


def _tokenize(text):
    tokens = re.findall(r"[a-zA-Z0-9_][a-zA-Z0-9_-]{2,}", text.lower())

    return {
        token
        for token in tokens
        if token not in STOP_WORDS
    }


def _read_text_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="utf-8", errors="replace") as file:
            return file.read()


def _score_file(relative_path, code, issue_terms):
    if not issue_terms:
        return 0

    path_text = relative_path.lower()
    code_text = code.lower()
    score = 0

    for term in issue_terms:
        if term in path_text:
            score += 15

        matches = code_text.count(term)
        if matches:
            score += min(matches, 20)

    return score


def _merge_ranges(ranges):
    if not ranges:
        return []

    ranges = sorted(ranges)
    merged = [ranges[0]]

    for start, end in ranges[1:]:
        previous_start, previous_end = merged[-1]

        if start <= previous_end + 1:
            merged[-1] = (
                previous_start,
                max(previous_end, end)
            )
        else:
            merged.append((start, end))

    return merged


def _build_snippet(code, issue_terms, context_lines, max_snippet_chars):
    lines = code.splitlines()

    if not lines:
        return ""

    matching_indexes = []

    for index, line in enumerate(lines):
        line_text = line.lower()

        if any(term in line_text for term in issue_terms):
            matching_indexes.append(index)

    if matching_indexes:
        ranges = _merge_ranges([
            (
                max(0, index - context_lines),
                min(len(lines), index + context_lines + 1)
            )
            for index in matching_indexes
        ])
    else:
        ranges = [
            (
                0,
                min(len(lines), context_lines * 2 + 1)
            )
        ]

    snippet_lines = []

    for start, end in ranges:
        if snippet_lines:
            snippet_lines.append("...")

        for index in range(start, end):
            snippet_lines.append(f"{index + 1}: {lines[index]}")

        if len("\n".join(snippet_lines)) >= max_snippet_chars:
            break

    snippet = "\n".join(snippet_lines)

    if len(snippet) > max_snippet_chars:
        snippet = (
            snippet[:max_snippet_chars]
            + "\n[TRUNCATED: snippet exceeded context limit]"
        )

    return snippet


def read_project_files(
    repo_path,
    issue_text="",
    max_relevant_files=12,
    context_lines=8,
    max_snippet_chars=12000,
    max_total_chars=60000
):
    print("\n===== SCANNING REPOSITORY FILES =====\n")
    print(f"Repository path: {repo_path}")

    if not repo_path or not os.path.isdir(repo_path):
        raise ValueError(f"Repository path does not exist: {repo_path}")

    repo_root = os.path.abspath(repo_path)
    issue_terms = _tokenize(issue_text)
    discovered_files = []
    file_records = []

    for root, dirs, files in os.walk(repo_root):
        dirs[:] = sorted([
            directory
            for directory in dirs
            if directory not in SKIPPED_DIRS
        ])

        for file_name in sorted(files):
            if file_name in SKIPPED_FILES:
                continue

            extension = os.path.splitext(file_name)[1].lower()
            if extension not in ALLOWED_EXTENSIONS:
                continue

            full_path = os.path.join(root, file_name)
            relative_path = _format_path(
                os.path.relpath(full_path, repo_root)
            )
            discovered_files.append(relative_path)

            try:
                code = _read_text_file(full_path)
            except Exception as exc:
                print(f"Error reading {relative_path}: {exc}")
                continue

            score = _score_file(
                relative_path,
                code,
                issue_terms
            )

            file_records.append({
                "path": relative_path,
                "code": code,
                "score": score,
            })

    discovered_files = sorted(discovered_files)
    discovered_files_text = "\n".join(
        f"- {file_path}"
        for file_path in discovered_files
    )

    if not discovered_files_text:
        discovered_files_text = "- No supported source files found"

    relevant_records = [
        record
        for record in file_records
        if record["score"] > 0
    ]
    relevant_records = sorted(
        relevant_records,
        key=lambda record: (-record["score"], record["path"])
    )
    relevant_records = relevant_records[:max_relevant_files]

    total_chars = 0
    snippet_sections = []

    for record in relevant_records:
        snippet = _build_snippet(
            record["code"],
            issue_terms,
            context_lines,
            max_snippet_chars
        )

        section = f"""
FILE: {record["path"]}
RELEVANCE SCORE: {record["score"]}
SNIPPET:
{snippet}
========================================
"""

        if total_chars + len(section) > max_total_chars:
            snippet_sections.append(
                "\n[TRUNCATED: relevant snippets exceeded total context limit]\n"
            )
            break

        snippet_sections.append(section)
        total_chars += len(section)
        print(f"Relevant File: {record['path']}")

    if snippet_sections:
        snippets_text = "".join(snippet_sections)
    else:
        snippets_text = "Not found in repository context."

    issue_terms_text = ", ".join(sorted(issue_terms))
    if not issue_terms_text:
        issue_terms_text = "Not found in repository context."

    return f"""
REPOSITORY ROOT:
{repo_root}

ACTUAL REPOSITORY FILES:
{discovered_files_text}

ISSUE TERMS USED FOR DYNAMIC MATCHING:
{issue_terms_text}

GROUNDING RULES FOR AGENTS:
- Use only the issue description and the repository context below.
- Mention only files listed under ACTUAL REPOSITORY FILES.
- Treat RELEVANT REPOSITORY SNIPPETS as the only code evidence.
- Treat issue text as the reported symptom, not proof that repository files, functions, frameworks, libraries, APIs, services, databases, routes, middleware, controllers, serializers, dependencies, or architecture exist.
- If code, files, symbols, frameworks, libraries, routes, APIs, services, or architecture are not visible below, say exactly "Not found in repository context."
- If the snippets are insufficient for accurate analysis, say exactly "Insufficient repository context for accurate analysis."

RELEVANT REPOSITORY SNIPPETS:
{snippets_text}
"""
