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

Konfiguration (optional): Tabelle [branch_cleanup] in
<Projekt-Root>/.claude-harness/config.toml, siehe docs/techdocs/configuration.md
im Claude_Harness-Repo. Kommandozeile ueberschreibt die Datei.
"""
from __future__ import annotations

import argparse
import fnmatch
import os
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


CONFIG_RELATIVE = Path(".claude-harness") / "config.toml"


def load_config(root: str) -> Settings:
    """Liest [branch_cleanup] aus der Harness-Konfiguration des Projekts; ohne Datei oder Tabelle gelten die Standards."""
    s = Settings()
    path = Path(root) / CONFIG_RELATIVE
    if not path.exists():
        return s
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (tomllib.TOMLDecodeError, OSError) as e:
        raise CleanupError(f"{path}: ungueltig: {e}") from e
    cfg = data.get("branch_cleanup", {})
    if not isinstance(cfg, dict):
        raise CleanupError(f"{path}: [branch_cleanup] muss eine Tabelle sein")
    unknown = set(cfg) - {"remote", "base", "coding_patterns", "protected"}
    if unknown:
        raise CleanupError(f"{path}: unbekannte Schluessel in [branch_cleanup]: {', '.join(sorted(unknown))}")
    for key in ("remote", "base"):
        if key in cfg and not (isinstance(cfg[key], str) and cfg[key].strip()):
            raise CleanupError(f"{path}: branch_cleanup.{key} muss ein nichtleerer String sein")
    s.remote = cfg.get("remote", s.remote)
    s.base = cfg.get("base")
    for key, attr in (("coding_patterns", "patterns"), ("protected", "protected")):
        if key in cfg:
            v = cfg[key]
            if not isinstance(v, list) or not all(isinstance(x, str) and x.strip() for x in v):
                raise CleanupError(f"{path}: branch_cleanup.{key} muss eine Liste nichtleerer Strings sein")
            if key == "coding_patterns" and not v:
                raise CleanupError(f"{path}: branch_cleanup.coding_patterns darf nicht leer sein")
            setattr(s, attr, v)
    return s


@dataclass
class Row:
    name: str
    sha: str
    status: str  # SAFE | NOT MERGED | PROTECTED | IGNORED | ERROR
    ahead: int | None = None
    note: str = ""
    commands: list[str] = field(default_factory=list)
    deletes: list[tuple[str, str]] = field(default_factory=list)  # (push url, geprueftes sha)
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
                    row.deletes.append((url, tip))
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


STATUS_COLOR = {"SAFE": "1;32", "SAFE*": "1;33", "NOT MERGED": "33", "PROTECTED": "36", "ERROR": "1;31"}


def report(rows: list[Row], warnings: list[str], base: str, remote: str, push_urls: list[str],
           color: bool = False) -> str:
    def c(text: str, code: str) -> str:
        return f"\033[{code}m{text}\033[0m" if color else text

    L: list[str] = []
    L.append(f"{c('Remote:', '1')} {c(remote, '36')}   {c('Base:', '1')} {c(base, '36')}")
    L.append(f"{c('Push-Ziele:', '1')} " + ", ".join(c(u, '36') for u in push_urls))
    for w in warnings:
        L.append(c(f"WARNUNG: {w}", "1;31"))
    L.append("")
    shown = [r for r in rows if r.status != "IGNORED"]
    if shown:
        w = max(len(r.name) for r in shown)
        L.append(c(f"{'Branch'.ljust(w)}  {'Status':<11} Ahead  Hinweis", "1;4"))
        for r in sorted(shown, key=lambda r: (r.status, r.name)):
            ahead = "-" if r.ahead is None else str(r.ahead)
            code = STATUS_COLOR.get(r.status, "0")
            L.append(f"{c(r.name.ljust(w), code)}  {c(f'{r.status:<11}', code)} {ahead:>5}  {r.note}")
    ignored = len(rows) - len(shown)
    L.append("")
    L.append(f"{len(rows)} Branches, {ignored} ohne Coding-Muster (nicht angezeigt).")
    L.append("SAFE* = gemerged, aber auf keinem Push-Ziel sicher loeschbar (siehe HINWEIS).")
    cmd_rows = [r for r in rows if r.commands]
    for r in rows:
        for sk in r.skipped:
            L.append(c(f"HINWEIS {r.name}: {sk}", "33"))
    L.append("")
    if not cmd_rows:
        L.append(c("Keine Loesch-Befehle: nichts ist sicher loeschbar.", "1;33"))
    else:
        L.append(c("# Pruefe die Liste und fuehre nur aus, was du wirklich loeschen willst.", "33"))
        L.append(c("# --force-with-lease loescht nur, wenn der Branch noch auf dem geprueften Commit steht.", "33"))
        L.append("")
        L.append(c("=== Einzeln ===", "1;35"))
        for r in cmd_rows:
            L.append("")
            L.append(c(f"# {r.name} ({r.sha[:9]})", "1;36"))
            L.extend(c(cmd, "1;32") for cmd in r.commands)
        L.append("")
        L.append(c("=== Alle auf einmal (ein Befehl je Push-Ziel, jeder Branch mit eigenem Lease) ===", "1;35"))
        by_url: dict[str, list[tuple[str, str]]] = {}
        for r in cmd_rows:
            for url, sha in r.deletes:
                by_url.setdefault(url, []).append((r.name, sha))
        for url, items in by_url.items():
            leases = " ".join("--force-with-lease=" + shlex.quote(f"refs/heads/{n}:{s}") for n, s in items)
            refs = " ".join(shlex.quote(f":refs/heads/{n}") for n, _ in items)
            L.append(c(f"git push {leases} {shlex.quote(url)} {refs}", "1;32"))
    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Prueft Remote-Branches, gibt Loesch-Befehle aus (loescht nie selbst).")
    ap.add_argument("--remote", help="Remote-Name (Standard: origin)")
    ap.add_argument("--base", help="Base-Branch (Standard: Default-Branch des Remotes)")
    ap.add_argument("--pattern", action="append", help="Coding-Muster (wiederholbar, ersetzt die Konfiguration)")
    ap.add_argument("--protect", action="append", default=[], help="Zusaetzlich geschuetztes Muster (wiederholbar)")
    ap.add_argument("--color", choices=["auto", "always", "never"], default="auto",
                    help="Farben (Standard auto: nur im Terminal, nie mit NO_COLOR)")
    ap.add_argument("--no-fetch", action="store_true", help="kein git fetch --prune vor der Analyse")
    args = ap.parse_args(argv)
    try:
        root = repo_root()
        s = load_config(root)
        if args.remote:
            s.remote = args.remote
        if args.base:
            s.base = args.base
        if args.pattern:
            s.patterns = args.pattern
        s.protected += args.protect
        rows, warnings, base, push_urls = analyze(root, s, not args.no_fetch)
        print(f"Repository: {root}")
        color = args.color == "always" or (
            args.color == "auto" and sys.stdout.isatty() and "NO_COLOR" not in os.environ)
        print(report(rows, warnings, base, s.remote, push_urls, color))
    except CleanupError as e:
        print(f"FEHLER: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
