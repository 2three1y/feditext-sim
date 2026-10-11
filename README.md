# feditext-sim

Builds [Feditext](https://github.com/feditext/feditext) — a free, open-source iOS Mastodon client by the Feditext contributors (a continuation of Metabolist's Metatext), licensed GPL-3.0 — for the **iOS Simulator** on GitHub Actions, so it can be run on a cloud simulator (e.g. Appetize.io) without a Mac.

This repository contains no Feditext source: the workflow clones the branch you pick at build time, compiles an unsigned Debug build for the simulator, zips `Feditext.app`, and uploads it as a workflow artifact (plus a temporary download link written to `ci-out/`).

All credit and copyright for Feditext belong to the Feditext and Metabolist authors. See `LICENSE` (GPL-3.0) and the upstream repository.

## Usage

Actions → "Feditext simulator build" → Run workflow → pick a Feditext branch (default `app-store-testflight`, the one that ships to TestFlight/App Store).

Branches of interest upstream: `app-store-testflight`, `link-menu`, `status-filters`, `develop`.

A branch for our own experiments on top of Feditext (for example an "Expand thread / Collapse thread" rotor action) can be added here later; it would carry the full GPL-3.0 source and stay GPL-3.0.
