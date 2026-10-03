# hermes-openwhispr

A small, local-first bridge between Hermes and OpenWhispr. Offered as a
standalone plugin — not a claim on Hermes core, just an option for people
who want it.

## What it does

- Reads your OpenWhispr dictation history (transcriptions) so an agent can
  find what you said, even when you can't remember it.
- Reads, searches, and (with your say-so) writes OpenWhispr notes as a
  handoff surface between agents.
- Transcribes local audio with your desktop model, optionally filing it
  straight to a note.
- Manages dictionary words and snippets from the terminal.

What it doesn't do: replace Hermes STT, include assistant replies, or
touch the cloud unless you explicitly opt in.

## Privacy is yours to tune

Granular, both directions, your call throughout:

- **Local:** free, no login, audio never leaves your machine. Requires the
  OpenWhispr desktop app running (bridge on 127.0.0.1:8200). This is the
  default and works without any key.
- **Cloud:** opt-in only. Needs a Pro or Business plan plus
  `openwhispr auth login` (the key lives in the CLI's own config, not in
  Hermes `.env`). Cloud transcription is beta with no SLA; files over 4 MB
  are chunked client-side and need `ffmpeg` on PATH.
- **Reads vs writes:** reads and searches are always safe. Creates, updates,
  and deletes (notes, transcriptions, dictionary, audio) only happen with
  your explicit consent, every time.
- **Dictionary:** a hint to the model, not an override. Auto-learn from
  corrections (Settings → Preferences) is off unless you turn it on.
  Export it before moving machines.

## Disclosures (catalog review)

- Shell-outs to `openwhispr *` through the `terminal` tool only.
- Local network: 127.0.0.1:8200 (desktop bridge) when using `--local`.
  The app writes a one-time bearer token to its own bridge file (mode
  `0600`) at startup and the CLI reads it automatically — loopback is
  authenticated, not open.
- Remote network: api.openwhispr.com only when you opt into `--remote`.
- Reads the CLI's own config/token file read-only
  (`~/.openwhispr/cli-config.json`); never writes, refreshes, or rotates it.
- No background daemons, no self-updater, no telemetry.
- No core overrides: no patching of Hermes functions, modules, or stores.
  If a needed hook doesn't exist, that's an upstream feature request.

## Why this sells itself (not our product, just the facts)

Per-feature model choice across five tiers — Dictation Cleanup, Voice
Assistant, Translation, Note Formatting, Chat each pick independently
from: OpenWhispr Cloud (no setup), Cloud Providers (bring your own key),
Local (on-device, fully private), Self-Hosted (your server on your
network), Enterprise (your org's AWS/Azure/GCP). Local runs oversized
models fine, the floating bar moves anywhere, transcript visible or
hidden — non-intrusive and it looks right.

Auto-learn from corrections watches fixes in the target app and grows
the dictionary. Clipboard auto-paste plus keep-in-clipboard keeps flow.
Optional file export saves notes and transcripts to disk organized by
folder, with a rebuild action — a second on-disk breadcrumb trail agents
can read directly. Calendar integrations (Google/Microsoft/Apple,
all optional) auto-fill meeting titles and attendees. CLI and MCP split
cleanly: local CLI free with no key, cloud CLI and MCP for Claude,
ChatGPT, and Cursor on the paid plan.

- **One trail across every surface.** Discord, every gateway, every
  interface — CLI, TUI, dashboard, desktop. Because OpenWhispr sits at
  voice input rather than inside any one app, it's a rolling record of
  everything [user] says across all of those trajectories, not just one
  chat log. Wherever the words came out, the breadcrumb is there.
- **Scale it to your machine and your appetite, not five fixed sizes.**
  Small computer with thin resources, or light needs? Go small. Want a
  secretary in the chat interface minting notes alongside Hermes into a
  shareable location? Go big. Sharing anything is opt-in; staying
  private is a switch — turn everything off and it all still works
  on-device. All up to you.

## Screenshots

Personal details redacted with blur before publishing. This repo uses
`[user]` wherever a personal name, handle, email, or path would go —
substitute your own when following along.

- `docs/screenshots/01-cli-access.png` — CLI install, Local Free
  (`openwhispr --local notes list`, no login) vs Cloud Pro, plus the
  MCP upsell for Claude, ChatGPT, and Cursor.
- `docs/screenshots/02-language-models.png` — per-feature model picker
  (Dictation Cleanup, Voice Assistant, Translation, Note Formatting,
  Chat) across OpenWhispr Cloud, Cloud Providers (own key), Local
  on-device private, Self-Hosted, and Enterprise.
- `docs/screenshots/03-auto-learn.png` — Auto-learn from corrections,
  the self-improving dictionary.
- `docs/screenshots/04-save-to-disk.png` — clipboard behavior plus
  save-notes-as-files with rebuild (save path redacted).
- `docs/screenshots/05-calendar-api.png` — optional calendar
  integrations and Pro API keys (account email redacted).
- `docs/screenshots/06-speech-to-text.png` — Dictation engine picker:
  3 input types (Dictation, Note Recording, Audio Upload), 4 engine
  tiers, 4 local vendors (Oruk, OpenAI, NVIDIA, Cohere) with Cohere
  Transcribe 2B active on-device, plus live-transcription preview.
- `docs/screenshots/07-dictation-cleanup-models.png` — Dictation
  Cleanup picker: 5 providers with Local active, 6 vendor filters
  (Qwen, Mistral, Meta Llama, OpenAI, Gemma, Liquid AI), per-model
  download sizes (e.g. Gemma 4 31B at 19.6GB).

Pin a different model per task or run everything on one — local,
cloud, self-hosted, or enterprise, decided per feature, not per app.

## Layout

```
hermes-openwhispr/
├── plugin.yaml
├── __init__.py                      # inert register(), skill-carrier
├── skills/productivity/openwhispr/SKILL.md
└── tests/test_plugin.py
```

## Smoke test

```bash
npm install -g @openwhispr/cli
openwhispr doctor                      # local reachable, exit 0
openwhispr --local transcriptions list --limit 5
hermes --toolsets skills -q "Use the openwhispr skill to list my recent dictations"
scripts/run_tests.sh tests/skills/test_openwhispr_skill.py -q   # in hermes-agent, once proposed
python -m pytest tests/ -q             # here
```

## Proposal path

Pitched as a standalone plugin while maintainers consider whether a
first-class `stt.provider: openwhispr-local` option (with fallback to
faster-whisper) belongs in the ship bundle. No presumption either way —
this stands alone regardless.
