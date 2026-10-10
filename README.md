# RiceWM community packages

Public packages and catalog records for RiceWM: `.riceapp` applications,
desktop recipes, custom GNOME extensions, KDE widgets and combined bundles.

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

Use the repository's submission form for a new creation or a new version. Include
the public source repository, exact commit, package version, license and component
types. Never include credentials or private user content. Each new version must
go through the marketplace-owned automated checks and promotion process.

Existing approved versions remain available while an update is reviewed. Reusing
a published version with different bytes is prohibited. The serving authority
will be the verified marketplace catalog; raw repository content cannot grant
approval or user permissions.

`CATALOG.json` records the starter package inventory and actual SHA-256 digests.
It is explicitly unsigned development metadata. The app examples use the existing
Rice SDK; bundle descriptors exercise the proposed component admission contract.
They do not silently install or enable embedded desktop code.
