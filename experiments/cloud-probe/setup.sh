#!/bin/bash
# Probe for STORY-047, way B: set the Claude_Harness up once per cloud environment.
# Paste this into the "Setup script" field of a separate environment (not the Default one).
# It is a probe, not part of the plugin. Every step is logged to $PROBE_DIR/setup.log, and
# the script always exits 0, because a non-zero exit would stop the session from starting.

# --- Probe settings: change them here, nowhere else ---
MODE="manual"        # manual: copy the skills and write hooks into ~/.claude; plugin: try "claude plugin install"
HARNESS_REPO_URL="https://github.com/ukf-hoppmann/Claude_Harness.git"   # the repository to fetch
HARNESS_REF="main"
HARNESS_DIR="/opt/claude-harness"
PROBE_DIR="/root/harness-probe"
MARKETPLACE_NAME="claude-harness-dev"   # "name" in .claude-plugin/marketplace.json of the repository
PLUGIN_NAME="claude-harness"            # "name" in plugin/.claude-plugin/plugin.json

mkdir -p "$PROBE_DIR"
LOG="$PROBE_DIR/setup.log"
: > "$LOG"

log() { printf '%s %s\n' "$(date -u +%H:%M:%S)" "$*" >> "$LOG"; }

# run <label> <command...>: logs label, exit code, and the last lines of output; returns the exit code.
run() {
  local label="$1" out rc
  shift
  out="$("$@" 2>&1)"
  rc=$?
  log "[$label] exit=$rc"
  [ -n "$out" ] && printf '%s\n' "$out" | tail -n 8 | sed 's/^/    /' >> "$LOG"
  return $rc
}

export GIT_TERMINAL_PROMPT=0   # a clone that needs credentials must fail, not wait for input

log "== environment (mode=$MODE) =="
log "user=$(id -un) home=$HOME"
log "python3=$(python3 --version 2>&1) at-least-3.11=$(python3 -c 'import sys; print(sys.version_info >= (3, 11))' 2>&1)"
log "git=$(git --version 2>&1) jq=$(command -v jq || echo missing) timeout=$(command -v timeout || echo missing)"
log "claude=$(command -v claude || echo 'not found')"
command -v claude > /dev/null 2>&1 && run "claude --version" claude --version
log "CLAUDE_CODE_REMOTE=${CLAUDE_CODE_REMOTE:-unset} CLAUDE_PROJECT_DIR=${CLAUDE_PROJECT_DIR:-unset}"
log "existing ~/.claude: $(ls -A "$HOME/.claude" 2> /dev/null | tr '\n' ' ')"

log "== Q1: can the setup script fetch a repository that is not attached to the session? =="
run "git ls-remote" timeout 60 git ls-remote "$HARNESS_REPO_URL" "$HARNESS_REF"
if run "git clone" timeout 120 git clone --depth 1 --branch "$HARNESS_REF" "$HARNESS_REPO_URL" "$HARNESS_DIR"; then
  CLONED=yes
  log "cloned: $(git -C "$HARNESS_DIR" log -1 --format='%h %s' 2>&1)"
else
  CLONED=no
fi
# What a public repository allows even without a clone (the docs say: raw files yes, archives no).
RAW_BASE="$(printf '%s' "$HARNESS_REPO_URL" | sed -E 's#https://github.com/(.*)\.git#https://raw.githubusercontent.com/\1#')"
ARCHIVE_URL="$(printf '%s' "$HARNESS_REPO_URL" | sed -E 's#\.git$##')/archive/refs/heads/$HARNESS_REF.tar.gz"
log "raw file http=$(curl -sS -m 30 -o /dev/null -w '%{http_code}' "$RAW_BASE/$HARNESS_REF/plugin/.claude-plugin/plugin.json" 2>&1)"
log "archive http=$(curl -sSL -m 30 -o /dev/null -w '%{http_code}' "$ARCHIVE_URL" 2>&1)"

if [ "$CLONED" = yes ] && [ "$MODE" = manual ]; then
  log "== Q2/Q3: user-level skills and hooks in ~/.claude of the VM =="
  PLUGIN="$HARNESS_DIR/plugin"

  # Copies, not symlinks (a symlinked skill folder may not be followed). The plugin name space is lost.
  mkdir -p "$HOME/.claude/skills"
  for d in "$PLUGIN"/skills/*/; do
    cp -r "$d" "$HOME/.claude/skills/$(basename "$d")"
  done
  log "skills copied: $(ls "$HOME/.claude/skills" | tr '\n' ' ')"
  log "skill files that still contain the placeholder CLAUDE_PLUGIN_ROOT: $(grep -rl 'CLAUDE_PLUGIN_ROOT' "$HOME/.claude/skills" | wc -l)"

  SETTINGS="$HOME/.claude/settings.json"
  if [ -f "$SETTINGS" ]; then
    log "settings.json existed before; content:"
    sed 's/^/    /' "$SETTINGS" >> "$LOG"
  fi
  # Two kinds of hooks: plain markers (prove that user-level hooks fire at all) and the real Harness hook.
  python3 - "$SETTINGS" "$PLUGIN" "$PROBE_DIR" >> "$LOG" 2>&1 << 'PY'
import json
import pathlib
import sys

settings, plugin, probe = (pathlib.Path(a) for a in sys.argv[1:4])
data = json.loads(settings.read_text()) if settings.exists() else {}
hooks = data.setdefault("hooks", {})

def marker(event):
    return (
        f'echo "$(date -u +%FT%TZ) {event} hook fired: CLAUDE_CODE_REMOTE=$CLAUDE_CODE_REMOTE '
        f'CLAUDE_PROJECT_DIR=$CLAUDE_PROJECT_DIR PWD=$PWD" >> {probe}/hook.log'
    )

harness = (
    f"CLAUDE_PLUGIN_ROOT={plugin} python3 {plugin}/scripts/session_start.py "
    f"| tee -a {probe}/session_start.out"
)
hooks.setdefault("SessionStart", []).append({
    "matcher": "startup|resume",
    "hooks": [
        {"type": "command", "command": marker("SessionStart"), "timeout": 10},
        {"type": "command", "command": harness, "timeout": 30},
    ],
})
hooks.setdefault("Stop", []).append({
    "hooks": [{"type": "command", "command": marker("Stop"), "timeout": 10}],
})
settings.parent.mkdir(parents=True, exist_ok=True)
settings.write_text(json.dumps(data, indent=2) + "\n")
print("settings.json written")
PY
  log "settings.json now:"
  sed 's/^/    /' "$SETTINGS" >> "$LOG"
fi

if [ "$CLONED" = yes ] && [ "$MODE" = plugin ]; then
  log "== Q4: install the plugin with the claude CLI inside the setup script =="
  if command -v claude > /dev/null 2>&1; then
    run "plugin marketplace add" timeout 90 claude plugin marketplace add "$HARNESS_DIR"
    run "plugin install" timeout 90 claude plugin install "$PLUGIN_NAME@$MARKETPLACE_NAME" --scope user
    run "plugin list" timeout 60 claude plugin list
  else
    log "claude CLI not available in the setup script; nothing to try"
  fi
fi

if [ "$CLONED" = no ]; then
  log "clone failed: the Harness cannot be set up from this script; see the ls-remote and clone lines above"
fi

touch "$PROBE_DIR/setup-done"
log "== done =="
exit 0
