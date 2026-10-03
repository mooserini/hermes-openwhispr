---
name: openwhispr
description: Use when finding what [user] dictated or shared via voice.
version: 0.1.0
author: [user], Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [OpenWhispr, Dictation, Notes, Transcription, Voice]
    related_skills: []
---

# OpenWhispr Skill

Local-first voice history and shared notes for [user], with a paid cloud fallback. OpenWhispr is the user's consistent voice input everywhere; its transcriptions are the rolling breadcrumb trail of what they said, and its notes are the handoff surface between agents.

Does not include assistant replies. Does not replace Hermes STT config. Defaults to the free local desktop bridge; the Pro/Business cloud API is opt-in only and never touched without explicit consent.

## When to Use

- [user] says "find what I said", "what was that thing I dictated", or can't remember a dictated phrase.
- Reading recent dictations, searching past voice history, or grounding a task in what [user] actually said.
- Creating, reading, updating, or searching OpenWhispr notes as agent-to-agent handoffs.
- Transcribing a local audio file with the desktop model, optionally saving straight to a note.
- Managing dictionary words or snippets [user] dictates constantly.
- Don't use for: Hermes voice config itself, cloud transcription beta, or anything needing an API key without asking first.

## Prerequisites

- Node.js 20 or later.
- `@openwhispr/cli` installed globally (`terminal(command="npm install -g @openwhispr/cli")`).
- OpenWhispr desktop app running locally for any `--local` work. No login or API key needed for local.
- Remote/cloud is opt-in: Pro or Business plan, API key via `terminal(command="openwhispr auth login")` (stored in the CLI's own config, not Hermes `.env`), scopes `transcriptions:write`, `dictionary:read/write`, `snippets:read/write`. Never log in, set `api-base`, or send audio remote without explicit consent.

## How to Run

Frame every invocation through the `terminal` tool. Always prefer `--local` to force the free desktop bridge.

- Check health: `terminal(command="openwhispr doctor")` — local must report reachable on 127.0.0.1:8200; exit 0 means at least one backend is up.
- Backend select: `terminal(command="openwhispr config get")`; leave `backend: auto` so it prefers local when the app runs.
- Read trail: `terminal(command="openwhispr --local transcriptions list --limit 10")` then `terminal(command="openwhispr --local transcriptions get <id>")`.
- Read notes: `terminal(command="openwhispr --local notes list --limit 20")`, `terminal(command="openwhispr --local notes get <id> --format json|markdown")`, `terminal(command="openwhispr --local notes search <query> --limit 10")`.
- Write handoff note: `terminal(command="openwhispr --local notes create --content <text> --title <t> --folder <name>")` or `--content-file <path>` for long bodies.
- Dual backends: `--local` forces the desktop bridge (free, no cap, audio stays on-machine); `--remote` forces OpenWhispr Cloud (paid plan + key, 4 MB files split into 4-minute chunks client-side needing `ffmpeg` on PATH, cloud transcription beta with no SLA). Bare `openwhispr` with `backend: auto` prefers local when reachable. Check both with `terminal(command="openwhispr --remote transcriptions list --limit 5")` only after [user] opts into cloud.

## Quick Reference

```
openwhispr doctor
openwhispr config get
openwhispr --local notes list [--folder <id>] [--limit N] [--format json|table]
openwhispr --local notes get <id> [--transcript] [--format json|markdown]
openwhispr --local notes create --content <text> | --content-file <path> [--title <t>] [--folder <name>]
openwhispr --local notes update <id> [--content <t>] [--folder <id>] [--title <t>]
openwhispr --local notes delete <id> [--dry-run]
openwhispr --local notes search <query> [--limit N]
openwhispr --local folders list
openwhispr --local folders create --name <name>
openwhispr --local transcriptions list [--limit N]
openwhispr --local transcriptions get <id> [--format json|text]
openwhispr --local transcriptions delete <id> [--dry-run]
openwhispr --local transcribe <file> [--model <id>] [--language <code>] [--note] [--title <t>] [--folder <name>]
openwhispr --local dictionary list
openwhispr --local dictionary add <word...> / remove <word...>
openwhispr --local snippets list / add "<trigger>" "<replacement>" / remove "<trigger>"
```

Exit codes: 0 success, 1 bad args, 2 backend unreachable (app not running), 3 auth failure, 4 not found.

## Procedure

1. Verify local is up with `openwhispr doctor`. Done when local.reachable is true; if exit 2, tell [user] to launch the desktop app and retry — do not fall back to remote silently.
2. Find the breadcrumb: list recent transcriptions (limit 10-20), scan `text`/`timestamp` fields. Done when the matching utterance or a clear miss is established; quote id + timestamp when citing.
3. Promote only on purpose: transcriptions are raw history; `notes create` only when [user] wants a durable shared note. Done when the note id returns and `notes get` round-trips the same content.
4. Share between agents via notes: title + folder + full JSON body, never paraphrase ids. Done when the next agent can `notes get <id>` without asking [user] for context.
5. Transcribe locally with `transcribe <file>` using the app's current model; add `--note --title --folder` to file it in one step. Done when transcript text prints and optional note id exists.
6. Grow the dictionary from real misses: `dictionary add` the spelling [user] wants to read, not the phonetic miss. Done when `dictionary list` shows the entry; remind [user] Auto-learn (Settings -> Preferences -> Auto-learn from corrections) already watches fixes in the dictated app.

## Pitfalls

- Notes vs transcriptions: `notes list` is empty until something is explicitly saved; the history lives in `transcriptions list`. An empty notes result is not an error.
- Dictionary is a hint, not an override. Keep it to the ~50 words actually gotten wrong; 500 dilutes the model. Export before moving machines.
- `--model <id>` must already be downloaded in the desktop app; a wrong name makes the CLI list what's available — use that list verbatim.
- Remote files over 4 MB split into 4-minute chunks client-side and need `ffmpeg` on PATH; prefer local for long or private audio.
- No SRT/VTT from the CLI; use `--format json` and post-process segments for timestamps.
- `audio delete` is local-only and dictation-only; meeting transcripts have no audio file; `--remote` errors by design.
- Never write, update, or delete notes/transcriptions/dictionary without explicit consent; reads and searches are always safe.
- File fallback: OpenWhispr can auto-save notes and transcripts as files on disk, organized by folder, with a rebuild action. When [user] enables it, prefer `read_file`/`search_files` against their configured save location for bulk reads; use the CLI when freshness or metadata (ids, timestamps) matters.

## Verification

- `openwhispr doctor` exits 0 with local reachable.
- Cited utterance includes transcription id + UTC timestamp matching `transcriptions get`.
- Any created note round-trips via `notes get <id> --format json` with identical title/content.
- No remote calls made unless [user] asked; `config get` still shows empty apiKey for local-only flows.
