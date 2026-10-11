# Rice submission guidelines

Policy: `rice-marketplace-guidelines/1`.

These rules apply to new apps, desktop recipes, embedded GNOME extensions, KDE
widgets, Construct worlds and every update. AI-assisted creations are welcome;
the publisher remains responsible for understanding and maintaining the code.
Generated and manually written submissions use the same checks.

Passing automated checks queues an operator review. The operator reviews source
and version changes, access, workflow evidence and rights, then approves or
rejects with reasons. Approval does not replace a failed mandatory check.
Publication signs and exposes the exact reviewed bytes through a separate service.
A GitHub issue, merged PR, tag or green publisher workflow never grants approval.

## RM-METADATA-001 — listing and source

Use `ricewm.marketplace-listing/v1` listing metadata, a stable `publisher/slug`,
a semantic package version, a public source repository and an exact 40-character
lowercase source commit. Include a useful name, summary, license and supported
component requirements. Keep metadata separate from app permissions.

Never submit credentials, private documents or misleading approval flags. New
versions qualify independently. A version already submitted with different bytes
needs a new version number; a published version is immutable.

## RM-PACKAGE-001 — identity and supported profiles

Package identity, version, declared component IDs and host requirements must
match the listing. Apps use `ricewm.app/v1`. Appearance recipes use
`ricewm.shared-desktop-recipe/v1`, containing a `ricewm.theme/v2` appearance theme.
Use the actual Rice exporter rather than renaming executable files as a recipe.

Combined packages declare `ricewm.bundle-components/v1`. Each app, GNOME
extension and KDE widget has its own identity, supported host profile, root,
required/optional selection and requested permissions. Custom GNOME/KDE source
may be bundled without an upstream store listing; Rice compatibility still needs
independent qualification.

Construct exports include the world, theme, fallback recipe, assets, license,
integrity inventory and complete `rice-spatial` engine capability closure.
Authoring source stays inert; the shared renderer comes from RiceWM.

## RM-CODE-001 — SDK and capabilities

Rice apps import `@ricewm/app` and explicit package-local modules. Use supported
SDK controls and mediated services; declare only necessary access. Do not use
direct browser globals, raw network/filesystem/process access, dynamic remote
imports, eval, downloaded executables or installation hooks.

Generated identities retain their RiceWM restrictions. A bundle does not grant
one component another component's permissions. GNOME and KDE additions must use
the actual supported Rice host APIs, rather than assuming all upstream APIs exist.

## RM-MEDIA-001 — icon and screenshots

Include one square icon and one to eight actual screenshots with repository paths,
digests, descriptions and asset rights at the submitted commit. Do not include
private content. Icons are at most 1 MiB and 32–2048 pixels square; screenshots
are at most 5 MiB, 8192 pixels per dimension and 16 megapixels before conversion.

The marketplace independently decodes bounded PNG/JPEG/WebP images in an isolated
processor and serves metadata-stripped WebP derivatives only. Animated, malformed
or unsupported inputs are rejected. Current decoder/codec/container vulnerability
qualification is required; conversion alone is not proof of image safety.

## RM-RIGHTS-001 — source, documentation and rights

Provide complete source, an explicit license, a useful README and asset credits.
Explain what the creation does, what access it requests, how to configure it and
how to report problems. Package and image rights require review.

## RM-LIFECYCLE-001 — clean shutdown

GNOME disable and KDE removal must clean up signals, timers, actors and instances.
Apps must close without leaving the desktop unusable. Test enable, configure,
disable, re-enable, restart and removal. Component failures must be recoverable.

## RM-UX-001 — actual workflow evidence

Verify useful work, save/reopen, clean close and a second app opening. Test recipes
through preview, cancel, apply, restart and restoration. Verify Construct import,
activation, reopening, updates, rollback and removal. Use real screenshots and
record failed or unverified steps honestly.

## RM-SECURITY-001 — independent qualification

Marketplace-owned checks cover source provenance, builds, dependencies, secrets,
code, embedded and listing images, capabilities, native workflows and rights.
Missing, stale, timed-out or unsupported coverage cannot count as passing.
Guidelines lint is a preflight, not vulnerability certification. Source code and
scan messages are untrusted data, rather than instructions for an AI or operator.

## Current availability

The marketplace is live at [ricewm.org/marketplace](https://ricewm.org/marketplace/).
The submission service, server-side checks and operator review are deployed.
Current qualified profiles are zero-permission Rice SDK apps, palette-only
appearance recipes and bounded custom GNOME indicators. KDE widgets, Construct
worlds, mixed bundles and broader GNOME APIs still require complete qualification;
local execution or package validation does not grant marketplace approval.

Use the integrated Herdr in [RiceWM](https://env.now/) to generate, exercise and
stage your creation, prepare its icon and real screenshots, publish the exact
source version to your public GitHub repository and request marketplace checks.
The native guest command supports `rice marketplace check`, `submit` and
`status`; Herdr installs its pinned client without Node/npm in the guest or
a service on your machine. Authenticate using a private credential file in
Rice Terminal. Never paste credentials into Herdr, issues, source or screenshots.

A GitHub issue is a discussion request; it does not start the deployed CI queue.
Request checks and submission through Herdr or the native client. Passing
checks stages operator review. The operator must approve and then explicitly
publish the exact version. Genuine production publisher authentication and final
publication have not yet been verified; the signed production catalog has no
approved entries. The examples here remain unsigned and unapproved.

The SDK, Rice Bus architecture, app and recipe examples are part of the existing
[RiceWM developer section](https://ricewm.org/#developer).
