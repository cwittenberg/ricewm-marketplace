# RiceWM marketplace submissions

This repository contains public plugin sources, media and submission contracts.
Marketplace implementation, scanning workers and operator controls remain private
in Webexe. Publishers can keep code in their own public GitHub repositories.

Marketplace: https://ricewm.org/marketplace/. SDK examples, recipe structure and
submission guidelines: https://ricewm.org/#developer.

## Package files

Each version has its own directory:

```text
packages/<publisher>/<slug>/<version>/
  marketplace.json   Listing and artifact paths
  build.json         Exact source-to-package mapping
  media.json         Icon, screenshots and retained credits
  LICENSE           Complete license notice
  README.md         Usage and source/asset credits
  media/            Server-normalized WebP icon and screenshots
  src/              Retained app, extension, widget or recipe sources
  dist/             Exact exported .riceapp or recipe artifact
```

The publisher namespace must match the repository owner. Contracts also support
source files directly in the version directory. Follow the exact paths returned
by Herdr staging and source preparation.

## Submit

Herdr can generate and exercise SDK apps, custom GNOME extensions, Qt widgets and
palette recipes, then stage their source and artifacts for submission. Full
Construct and mixed bundles can also be staged. KDE, Construct and mixed-bundle
marketplace qualification remains incomplete; staging does not approve them.

The guest-native `rice marketplace` command exposes source preparation,
publication, checks, submission and status. Neither path requires Node/npm in the
guest or a service on the user's host machine. Configure GitHub credentials
privately in the guest; never paste them into Herdr or commit them.

Alternatively, choose **Actions → Rice marketplace submission → Run workflow**:

1. Select the branch containing the new version.
2. Enter its `packages/<publisher>/<slug>/<version>` directory.
3. Choose `check` for preflight, or `submit` for full server qualification and
   operator review.

The workflow sends an immutable commit and bounded source credentials to the
marketplace. It runs no contributor build scripts and publishes nothing itself.
Checks and media processing run server-side. A passing submission still needs an
operator's explicit approval and publication decision.

## Updates and retries

Every submitted version binds its source commit and exact package bytes. Change
the version for changed source, even if the exported artifact happens to match.
For renewed evidence against the same source, rerun the original Actions job;
that preserves its commit. Starting a new workflow from a later branch head
selects a different commit.

Editing workflows does not automatically resubmit existing versions or use the
publisher's submission allowance. The service limits admissions to four per
publisher per hour. Retain a pending receipt and poll instead of resubmitting.

Raw repository contents, a merged PR and a green workflow do not constitute
marketplace approval. Discovery and installation use the signed approved catalog.
Never commit access tokens, signing keys, private findings or user documents.
