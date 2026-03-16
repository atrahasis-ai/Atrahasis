from __future__ import annotations

from pathlib import Path


def spec_id_directory_prefixes(spec_id: str) -> tuple[str, ...]:
    normalized = spec_id.strip().upper()
    if not normalized:
        raise ValueError("spec_id is required")

    prefix = normalized[:1]
    suffix = normalized[1:]
    if not prefix.isalpha() or not suffix.isdigit():
        return (normalized,)

    number = int(suffix)
    short = f"{prefix}{number}"
    padded = f"{prefix}{number:02d}" if number < 10 else short

    ordered: list[str] = []
    for candidate in (normalized, short, padded):
        if candidate not in ordered:
            ordered.append(candidate)
    return tuple(ordered)


def resolve_spec_path(repo_root: Path, spec_id: str) -> Path:
    """Resolve a spec id like C42 to its actual titled master spec path."""
    prefixes = spec_id_directory_prefixes(spec_id)
    normalized = prefixes[0]

    specs_root = repo_root / "docs" / "specifications"
    for prefix in prefixes:
        direct_candidate = specs_root / prefix / "MASTER_TECH_SPEC.md"
        if direct_candidate.exists():
            return direct_candidate

    directory_candidates: list[Path] = []
    for prefix in prefixes:
        for item in specs_root.glob(f"{prefix}*"):
            if not item.is_dir():
                continue
            name = item.name.upper()
            if name == prefix or name.startswith(prefix + " ") or name.startswith(prefix + " -"):
                if item not in directory_candidates:
                    directory_candidates.append(item)

    if not directory_candidates:
        raise FileNotFoundError(f"Unable to resolve spec directory for {normalized}")

    file_candidates: list[Path] = []
    for directory in sorted(directory_candidates):
        master = directory / "MASTER_TECH_SPEC.md"
        if master.exists():
            file_candidates.append(master)
            continue
        for candidate in sorted(directory.glob("*MASTER*TECH_SPEC*.md")):
            if candidate.is_file():
                file_candidates.append(candidate)

    if not file_candidates:
        raise FileNotFoundError(f"Unable to resolve master tech spec for {normalized}")
    if len(file_candidates) > 1:
        unique = {path.resolve() for path in file_candidates}
        if len(unique) > 1:
            joined = ", ".join(str(path.relative_to(repo_root)).replace("\\", "/") for path in file_candidates)
            raise FileExistsError(f"Multiple master tech specs found for {normalized}: {joined}")
    return file_candidates[0]


def resolve_spec_ref(repo_root: Path, spec_id: str) -> str:
    path = resolve_spec_path(repo_root, spec_id)
    return str(path.relative_to(repo_root)).replace("\\", "/")
