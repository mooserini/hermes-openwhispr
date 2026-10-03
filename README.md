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

Under the hood it's bundled C++ runtimes, not a Python stack:
whisper.cpp for the Whisper family, sherpa-onnx for Orukeet, Parakeet,
Nemotron, and Cohere — no interpreter or runtime to install. Metal
acceleration is built in on Apple Silicon with automatic CPU fallback,
CUDA/Vulkan are one-click on other platforms, and the default local
model is ~672MB with the most accurate offline option at ~2.7GB. Small
binaries, honest sizes, GPU when it's there, CPU when it isn't.

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

Read top to bottom — each picture follows the claim it proves, with its
context right beside it so nothing needs backtracing. Personal details
redacted with blur before publishing. This repo uses `[user]` wherever a
personal name, handle, email, or path would go — substitute your own when
following along.

### CLI install, Local Free vs Cloud Pro, MCP upsell

![](docs/screenshots/01-cli-access.png)

`npm install -g @openwhispr/cli`, then `openwhispr --local notes list`
with no login — or Cloud Pro and MCP for Claude, ChatGPT, and Cursor.

### Per-feature model picker: five tiers, your call each time

![](docs/screenshots/02-language-models.png)

Dictation Cleanup, Voice Assistant, Translation, Note Formatting, Chat —
each picks independently from OpenWhispr Cloud, Cloud Providers (own
key), Local on-device private, Self-Hosted, or Enterprise.

### Auto-learn from corrections: the self-improving dictionary

![](docs/screenshots/03-auto-learn.png)

Fix a word in the target app and it's in your dictionary. No maintenance.

### Clipboard flow plus save-notes-as-files (save path redacted)

![](docs/screenshots/04-save-to-disk.png)

Auto-paste, keep-in-clipboard, and on-disk Markdown organized by folder
with a rebuild action — a second breadcrumb trail agents can read directly.

### Optional calendars and Pro API keys (account email redacted)

![](docs/screenshots/05-calendar-api.png)

Google, Microsoft, Apple — all optional. Meeting titles and attendees
auto-fill into notes.

### Dictation engine picker: 3 inputs, 4 tiers, 4 local vendors

![](docs/screenshots/06-speech-to-text.png)

Dictation, Note Recording, Audio Upload. Oruk, OpenAI, NVIDIA, Cohere —
Cohere Transcribe 2B active on-device here — plus live-transcription preview.

### Dictation Cleanup picker: 6 vendors, per-model downloads

![](docs/screenshots/07-dictation-cleanup-models.png)

Qwen, Mistral, Meta Llama, OpenAI, Gemma, Liquid AI, with honest sizes
(Gemma 4 31B at 19.6GB). Pin a different model per task or run
everything on one — local, cloud, self-hosted, or enterprise, decided
per feature, not per app.

## The point in one paragraph

No weird integrations, no regressions, no new dependencies: your
personal context shows up in every space you interact in, with every
agent you talk to — and underneath it all, a first-class, go-to
speech-to-text option that happens to remember everything you said.

## A win for both sides — and everyone in between

- **OpenWhispr** meets a crowd of local-first users who would never
  otherwise try it. Free local gets them in; the paid cloud, MCP
  connectors, and API are one step away when they want more — plus an
  agent bootstrap flow that mints scoped keys with a single email code.
- **Hermes and Nous Research** get the option of a local default that
  remembers: every user carrying a rolling record of what they said,
  reachable from any surface, on top of transcription they already trust.
- **Users** stop choosing between a bill and a memory. Start free and
  private; pay only if the cloud earns it; never lose what you said.
  Tie in email, keep notes, transcribe audio — small pieces, and
  together nearly a powerhouse.

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

## Attribution

- **OpenWhispr** makes the dictation app, the CLI (`@openwhispr/cli`),
  the cloud API, and the docs at docs.openwhispr.com this plugin leans
  on. All screenshots are of their application; all product names and
  marks are theirs. This plugin is an independent community pitch, and
  OpenWhispr should know it's being recommended to Nous Research as an
  option — with appreciation, and without claiming their endorsement.
- **Hermes Agent by Nous Research** is the platform this plugin extends,
  through public plugin surfaces only. This is a proposal for their
  consideration, not a directive — adoption as a first-class option is
  theirs to decide.
- This plugin itself is community work, published under MIT, with no
  affiliation to either party.

## Layout

```
hermes-openwhispr/
├── plugin.yaml
├── __init__.py                      # inert register(), skill-carrier
├── README.md
├── skills/productivity/openwhispr/SKILL.md
├── docs/screenshots/01-07*.png
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
