# Host UI structural prototype

A deliberately neutral, local-only Host UI built with semantic HTML, CSS, and
plain ES modules. It has no runtime dependencies, backend, persistence, Theme
Pack loader, or theme-switching system.

## Run

From the repository root:

```powershell
python -m http.server 4173 --directory host-ui
```

Then open <http://127.0.0.1:4173>.

The page must be served over HTTP because its JavaScript is loaded as an ES
module.

## Development fixtures

The production Host renders without QA controls. Open
<http://127.0.0.1:4173/?dev=1> to expose the separate development harness
outside the Host application shell. It can select the conversation, empty,
loading, recoverable-error, and disabled-composer fixtures or toggle the
neutral QA appearance.

The long conversation and long-title fixtures are available in the sidebar.

All data and interactions are in memory and reset on page reload.

## Validate

With the local server running on port `4173`, run:

```powershell
python host-ui/tests/validate_host_ui.py
```

The validation script uses Python Playwright and headless Chromium. It covers
the required desktop and mobile sizes, local interactions, overflow ownership,
fixture states, drawer focus behavior, touch targets, and reduced motion. It
writes review screenshots to `host-ui/validation/`.
