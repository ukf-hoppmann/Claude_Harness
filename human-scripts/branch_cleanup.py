#!/usr/bin/env python3
"""Prueft Remote-Branches und gibt Loesch-Befehle zum Kopieren aus.

Dieses Skript LOESCHT NIE selbst. Es fuehrt nur lesende Git-Befehle aus
(plus `git fetch --prune` fuer die Remote-Tracking-Refs) und druckt am Ende
`git push`-Befehle, die du selbst pruefst und ausfuehrst.

Aufruf (aus dem Zielprojekt heraus, egal aus welchem Unterordner):

    python3 /pfad/zu/Claude_Harness/human-scripts/branch_cleanup.py

Das Projekt wird am aktuellen Verzeichnis erkannt (`git rev-parse
--show-toplevel`), nie am Ablageort des Skripts.

Ein Branch bekommt nur dann einen Befehl, wenn alles gilt:
  * er passt auf ein Coding-Muster (Standard: claude/*),
  * er ist NICHT geschuetzt (HEAD, main, master, Base-Branch, Default-Branch
    des Remotes und der ausgecheckte Branch sind immer geschuetzt),
  * sein Commit ist Vorfahre des Base-Branches (git merge-base --is-ancestor),
  * pro Push-Ziel: der Branch steht dort auf demselben Commit und dieser
    Commit ist auch im Base-Branch dieses Ziels enthalten.

Die Befehle nutzen --force-with-lease mit dem geprueften Commit: Hat der
Branch inzwischen einen anderen Stand, lehnt Git das Loeschen ab.

Konfiguration (optional): branch_cleanup.toml neben diesem Skript, siehe
branch_cleanup.toml.example. Kommandozeile ueberschreibt die Datei.
"""
from __future__ import annotations

import argparse
import fnmatch
import shlex
import subprocess
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

# Nie loeschbar, nicht per Konfiguration oder Argument abschaltbar.
HARD_PROTECTED = ("HEAD", "main", "master")
DEFAULT_PATTERNS = ["claude/*"]
DEFAULT_PROTECTED = ["develop", "release/*"]


class CleanupError(Exception):
    pass


def git(args: list[str], cwd: str | None = None) -> tuple[int, str, str]:
    p = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def git_ok(args: list[str], cwd: str | None = None) -> str:
    rc, out, err = git(args, cwd)
    if rc != 0:
        raise CleanupError(f"git {' '.join(args)} fehlgeschlagen: {err or out}")
    return out


@dataclass
class Settings:
    remote: str = "origin"
    base: str | None = None
    patterns: list[str] = field(default_factory=lambda: list(DEFAULT_PATTERNS))
    protected: list[str] = field(default_factory=lambda: list(DEFAULT_PROTECTED))


def _str_list(cfg: dict, key: str, path: Path) -> list[str] | None:
    if key not in cfg:
        return None
    v = cfg[key]
    if not isinstance(v, list) or not all(isinstance(x, str) and x for x in v):
        raise CleanupError(f"{path}: '{key}' muss eine Liste nichtleerer Strings sein")
    return v


def load_config(path: Path, explicit: bool) -> Settings:
    s = Settings()
    if not path.exists():
        if explicit:
            raise CleanupError(f"Konfigurationsdatei nicht gefunden: {path}")
        return s
    try:
        cfg = tomllib.loads(path.read_text(encoding="utf-8"))
    except (tomllib.TOMLDecodeError, OSError) as e:
        raise CleanupError(f"{path}: ungueltig: {e}") from e
    known = {"remote", "base", "coding_patterns", "protected"}
    unknown = set(cfg) - known
    if unknown:
        raise CleanupError(f"{path}: unbekannte Schluessel: {', '.join(sorted(unknown))}")
    for key in ("remote", "base"):
        if key in cfg and not (isinstance(cfg[key], str) and cfg[key]):
            raise CleanupError(f"{path}: '{key}' muss ein nichtleerer String sein")
    s.remote = cfg.get("remote", s.remote)
    s.base = cfg.get("base")
    pats = _str_list(cfg, "coding_patterns", path)
    if pats is not None:
        if not pats:
            raise CleanupError(f"{path}: 'coding_patterns' darf nicht leer sein")
        s.patterns = pats
    prot = _str_list(cfg, "protected", path)
    if prot is not None:
        s.protected = prot
    return s


@dataclass
class Row:
    name: str
    sha: str
    status: str  # SAFE | NOT MERGED | PROTECTED | IGNORED | ERROR
    ahead: int | None = None
    note: str = ""
    commands: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)


def repo_root() -> str:
    rc, out, err = git(["rev-parse", "--show-toplevel"])
    if rc != 0:
        raise CleanupError("Nicht in einem Git-Repository (kein Fallback auf ein anderes).")
    return out


def ls_remote_heads(url: str, root: str) -> dict[str, str]:
    out = git_ok(["ls-remote", "--heads", url], root)
    heads: dict[str, str] = {}
    for line in out.splitlines():
        sha, ref = line.split("\t", 1)
        heads[ref.removeprefix("refs/heads/")] = sha
    return heads


def is_ancestor(root: str, a: str, b: str) -> bool | None:
    rc, _, _ = git(["merge-base", "--is-ancestor", a, b], root)
    return True if rc == 0 else False if rc == 1 else None


def has_commit(root: str, sha: str) -> bool:
    return git(["cat-file", "-e", f"{sha}^{{commit}}"], root)[0] == 0


def analyze(root: str, s: Settings, do_fetch: bool) -> tuple[list[Row], list[str], str, list[str]]:
    warnings: list[str] = []
    remote = s.remote
    if git(["remote", "get-url", remote], root)[0] != 0:
        raise CleanupError(f"Remote '{remote}' existiert nicht.")
    fetch_url = git_ok(["remote", "get-url", remote], root)
    push_urls = git_ok(["remote", "get-url", "--push", "--all", remote], root).splitlines()
    push_urls = list(dict.fromkeys(push_urls))

    if do_fetch:
        git_ok(["fetch", "--prune", remote], root)

    rc, head_ref, _ = git(["symbolic-ref", "--short", f"refs/remotes/{remote}/HEAD"], root)
    remote_default = head_ref.removeprefix(f"{remote}/") if rc == 0 else None
    base = s.base or remote_default or "main"
    base_sha = git(["rev-parse", "--verify", f"refs/remotes/{remote}/{base}^{{commit}}"], root)
    if base_sha[0] != 0:
        raise CleanupError(f"Base-Branch '{remote}/{base}' nicht gefunden.")
    base_ref = f"refs/remotes/{remote}/{base}"

    rc, current, _ = git(["symbolic-ref", "--short", "-q", "HEAD"], root)
    protected_exact = set(HARD_PROTECTED) | {base}
    if remote_default:
        protected_exact.add(remote_default)
    if rc == 0 and current:
        protected_exact.add(current)

    def is_protected(name: str) -> bool:
        return name in protected_exact or any(fnmatch.fnmatchcase(name, p) for p in s.protected)

    # Push-Ziele: aktuelle Staende per ls-remote (frisch, unabhaengig vom Fetch).
    targets: dict[str, dict[str, str] | None] = {}
    for url in push_urls:
        try:
            heads = ls_remote_heads(url, root)
        except CleanupError as e:
            warnings.append(f"Push-Ziel {url} nicht erreichbar, es werden dort keine Befehle erzeugt ({e})")
            targets[url] = None
            continue
        targets[url] = heads
        tb = heads.get(base)
        if tb is None:
            warnings.append(f"Push-Ziel {url}: Base-Branch '{base}' fehlt, keine Befehle dafuer")
            targets[url] = None
        elif not has_commit(root, tb):
            # Objekte laden, ohne Refs oder FETCH_HEAD anzulegen.
            git(["fetch", "--no-write-fetch-head", url, f"refs/heads/{base}"], root)

    out = git_ok(["for-each-ref", "--format=%(refname)%09%(objectname)", f"refs/remotes/{remote}/"], root)
    rows: list[Row] = []
    prefix = f"refs/remotes/{remote}/"
    for line in out.splitlines():
        ref, sha = line.split("\t")
        name = ref.removeprefix(prefix)
        if name == "HEAD":
            continue
        row = Row(name, sha, "IGNORED")
        rows.append(row)
        if is_protected(name):
            row.status = "PROTECTED"
            continue
        if not any(fnmatch.fnmatchcase(name, p) for p in s.patterns):
            continue
        anc = is_ancestor(root, sha, base_ref)
        rc, cnt, _ = git(["rev-list", "--count", f"{base_ref}..{ref}"], root)
        row.ahead = int(cnt) if rc == 0 and cnt.isdigit() else None
        if anc is None:
            row.status, row.note = "ERROR", "Merge-Pruefung fehlgeschlagen"
            continue
        if not anc:
            row.status = "NOT MERGED"
            continue
        row.status = "SAFE"
        for url, heads in targets.items():
            if heads is None:
                row.skipped.append(f"{url}: Ziel nicht pruefbar")
                continue
            tip = heads.get(name)
            if tip is None:
                row.skipped.append(f"{url}: Branch dort nicht vorhanden")
            elif tip != sha:
                row.skipped.append(f"{url}: steht dort auf anderem Commit ({tip[:9]}), manuell pruefen")
            else:
                merged = is_ancestor(root, tip, heads[base])
                if merged is True:
                    row.commands.append(
                        "git push --force-with-lease="
                        + shlex.quote(f"refs/heads/{name}:{tip}")
                        + f" {shlex.quote(url)} "
                        + shlex.quote(f":refs/heads/{name}")
                    )
                elif merged is False:
                    row.skipped.append(f"{url}: dort nicht in '{base}' gemerged")
                else:
                    row.skipped.append(f"{url}: Merge-Pruefung dort fehlgeschlagen")
        if not row.commands:
            row.status, row.note = "SAFE*", "kein Befehl erzeugt"
    return rows, warnings, base, push_urls


def report(rows: list[Row], warnings: list[str], base: str, remote: str, push_urls: list[str]) -> str:
    L: list[str] = []
    L.append(f"Remote: {remote}   Base: {base}")
    L.append("Push-Ziele: " + ", ".join(push_urls))
    for w in warnings:
        L.append(f"WARNUNG: {w}")
    L.append("")
    shown = [r for r in rows if r.status != "IGNORED"]
    if shown:
        w = max(len(r.name) for r in shown)
        L.append(f"{'Branch'.ljust(w)}  {'Status':<11} Ahead  Hinweis")
        for r in sorted(shown, key=lambda r: (r.status, r.name)):
            ahead = "-" if r.ahead is None else str(r.ahead)
            L.append(f"{r.name.ljust(w)}  {r.status:<11} {ahead:>5}  {r.note}")
    ignored = len(rows) - len(shown)
    L.append("")
    L.append(f"{len(rows)} Branches, {ignored} ohne Coding-Muster (nicht angezeigt).")
    L.append("SAFE* = gemerged, aber auf keinem Push-Ziel sicher loeschbar (siehe HINWEIS).")
    cmd_rows = [r for r in rows if r.commands]
    for r in rows:
        for sk in r.skipped:
            L.append(f"HINWEIS {r.name}: {sk}")
    L.append("")
    if not cmd_rows:
        L.append("Keine Loesch-Befehle: nichts ist sicher loeschbar.")
    else:
        L.append("# Pruefe die Liste und fuehre nur aus, was du wirklich loeschen willst.")
        L.append("# --force-with-lease loescht nur, wenn der Branch noch auf dem geprueften Commit steht.")
        for r in cmd_rows:
            L.append("")
            L.append(f"# {r.name} ({r.sha[:9]})")
            L.extend(r.commands)
    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Prueft Remote-Branches, gibt Loesch-Befehle aus (loescht nie selbst).")
    ap.add_argument("--remote", help="Remote-Name (Standard: origin)")
    ap.add_argument("--base", help="Base-Branch (Standard: Default-Branch des Remotes)")
    ap.add_argument("--pattern", action="append", help="Coding-Muster (wiederholbar, ersetzt die Konfiguration)")
    ap.add_argument("--protect", action="append", default=[], help="Zusaetzlich geschuetztes Muster (wiederholbar)")
    ap.add_argument("--config", help="Pfad zur Konfigurationsdatei")
    ap.add_argument("--no-fetch", action="store_true", help="kein git fetch --prune vor der Analyse")
    args = ap.parse_args(argv)
    try:
        cfg_path = Path(args.config) if args.config else Path(__file__).with_name("branch_cleanup.toml")
        s = load_config(cfg_path, explicit=bool(args.config))
        if args.remote:
            s.remote = args.remote
        if args.base:
            s.base = args.base
        if args.pattern:
            s.patterns = args.pattern
        s.protected += args.protect
        root = repo_root()
        rows, warnings, base, push_urls = analyze(root, s, not args.no_fetch)
        print(f"Repository: {root}")
        print(report(rows, warnings, base, s.remote, push_urls))
    except CleanupError as e:
        print(f"FEHLER: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
