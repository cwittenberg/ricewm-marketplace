# RiceWM community packages

Public packages and catalog records for RiceWM: `.riceapp` applications,
desktop recipes, custom GNOME extensions, KDE widgets and combined bundles.
Portable spatial desktops, including Construct worlds, can also be submitted
with their contained world, models, theme, license and authoring sources. They
declare the Rice spatial engine API and required host capabilities. The shared
renderer is supplied by RiceWM; authoring source files are never install hooks.

This repository contains distributable creations. Marketplace UI, services,
scanners and RiceWM host implementation are maintained privately in `webexe`.
Publishers may maintain their original source repositories; releases mirrored
here remain tied to one source commit and immutable package digest.

## Current state

The initial packages are **development examples, not Rice approved releases**.
They are intended for compatibility and admission testing. No CI or runtime
security approval is implied by their presence, a GitHub star or a successful
download. Custom extension/widget code does not require an upstream store listing,
but it must pass qualification for the supported Rice host before approval.

## Submit and update

Use integrated Herdr in [RiceWM](https://env.now/) or the native guest marketplace
client to prepare, check and submit a new creation or version. The deployed
service acquires your public repository at one exact commit, independently checks
the package and stages operator review. Herdr installs the pinned native client;
Node/npm in the guest and services on your machine are unnecessary.

Include the public source repository, exact commit, package version, license and
component types. Supply authentication only through a private Rice Terminal
credential file. Never put credentials or private user content in AI prompts,
issues, source or screenshots. The GitHub issue form is for discussion; opening
an issue does not enqueue automated qualification.

Every version goes through marketplace-owned checks, final operator review and
separate publication. Passing checks never publishes automatically. The operator
can reject with actionable reasons, but cannot bypass failed checks. The signed
production catalog currently has no approved entries, and authenticated production
submission/publication has not yet been verified.

Read [the submission guidelines](SUBMISSION_GUIDELINES.md) before submitting.
Generated and manually written code follow the same rules.

Existing approved versions remain available while an update is reviewed. Reusing
a published version with different bytes is prohibited. The serving authority
will be the verified marketplace catalog; raw repository content cannot grant
approval or user permissions.

`CATALOG.json` records the starter package inventory and actual SHA-256 digests.
It is explicitly unsigned development metadata. The app examples use the existing
Rice SDK; bundle descriptors exercise the proposed component admission contract.
They do not silently install or enable embedded desktop code.

## Icons and screenshots

Submit one square icon and one to eight screenshots with descriptions, asset
rights, repository paths and SHA-256 digests. Prefer metadata-stripped WebP.
Media must exist at the exact submitted source commit. The marketplace must
independently decode and normalize images in isolation, apply byte/pixel limits
and scan current decoder/codec/container dependencies before approval. Conversion
alone is not proof of image safety. No such CI approval is currently granted by
this development registry. Never submit screenshots containing private data.
