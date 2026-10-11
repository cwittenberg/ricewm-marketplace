# GNOME indicator starter

This custom GNOME 50 extension is packaged directly as a .riceapp; it does not require GNOME Extensions Store publication. Its owned panel label and popup menu activate the original source-defined text callback. Disable destroys the indicator and clears its reference.

This starter targets RiceWM’s bounded local indicator qualification profile. Unknown GNOME/GI APIs and authority require additional qualification; this package does not declare network, filesystem, DBus, timers or settings.

The screenshot captures only this extension’s actual owned native indicator and popup surfaces, using RiceWM’s compositor and text painter; the desktop and other applications are excluded. The icon retains the original RiceWM contributors starter icon. Both were normalized by the audited server Rust decoder; source files contain no raw image decoder or CI implementation. Full authorship/rights and publication still require operator review.

SPDX-License-Identifier: MIT

Copyright (c) 2026 RiceWM contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


```json
{
  "schema": "ricewm.marketplace-media-credits/v1",
  "credits": [
    {
      "path": "packages/cwittenberg/gnome-indicator-starter/1.0.0/media/icon.webp",
      "creator": "RiceWM contributors",
      "license": "MIT",
      "origin": "original",
      "notice": "packages/cwittenberg/gnome-indicator-starter/1.0.0/LICENSE"
    },
    {
      "path": "packages/cwittenberg/gnome-indicator-starter/1.0.0/media/screenshot.webp",
      "creator": "RiceWM contributors",
      "license": "MIT",
      "origin": "original",
      "notice": "packages/cwittenberg/gnome-indicator-starter/1.0.0/LICENSE"
    }
  ]
}
```
