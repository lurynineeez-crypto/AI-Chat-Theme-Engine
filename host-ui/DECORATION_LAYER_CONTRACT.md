# Host UI decoration layer contract

Status: structural baseline
Scope: Host-owned decoration slots only

This contract defines where a future visual skin may render non-interactive
decoration. It does not authorize Theme Pack loading, arbitrary markup,
JavaScript, layout changes, or pseudo-element ownership.

## Required component structure

Decorated Host components use three explicit layers:

```text
Component stacking context
├── Outside decoration boundary  z-index: 0
│   └── Outside decoration slot
├── Inside decoration boundary   z-index: 1
│   └── Inside decoration slot
└── Content layer                z-index: 2
```

Every boundary and slot is absolutely positioned, `aria-hidden="true"`, and
uses `pointer-events: none`. Decoration therefore contributes no intrinsic
size and cannot change component layout measurements.

The content layer always renders above both decoration layers.

## Clipping and overflow

The inside boundary matches the component border box, inherits its radius, and
uses `overflow: hidden`. Inside decoration cannot paint beyond the component.

The outside boundary expands by a Host-owned, component-specific allowance and
uses `overflow: hidden` at that expanded boundary. Outside decoration may cross
the visual component edge, but anything beyond the allowance is clipped.

| Host component | Maximum outside overflow |
| --- | ---: |
| Incoming or outgoing bubble | 12px on each side |
| Avatar frame | 8px on each side |
| Composer | 8px on each side |
| Chat header | 8px on each side |
| Brand area | 8px on each side |
| Empty state | 12px on each side |
| Sidebar / mobile drawer | 0px; clipped to the shell or drawer |

These allowances are Host layout constraints, not theme tokens. Theme code
must not override them. Ancestor shell and viewport clipping still applies.

## Durable hooks

Each slot is addressed directly through a stable `data-theme-hook`:

- `incoming-bubble-decoration-inside`
- `incoming-bubble-decoration-outside`
- `outgoing-bubble-decoration-inside`
- `outgoing-bubble-decoration-outside`
- `avatar-frame-decoration-inside`
- `avatar-frame-decoration-outside`
- `composer-decoration-inside`
- `composer-decoration-outside`
- `chat-header-decoration-inside`
- `chat-header-decoration-outside`
- `sidebar-decoration-inside`
- `sidebar-decoration-outside`
- `brand-decoration-inside`
- `brand-decoration-outside`
- `empty-state-decoration-inside`
- `empty-state-decoration-outside`
- `application-decoration-inside`
- `global-overlay-decoration-inside`

Themes must not depend on descendant order, generic class names, or ownership
of `::before` and `::after`.

## Missing decoration behavior

Slots are empty by default. An empty or missing visual asset:

- occupies no layout space
- changes no padding, gap, width, or height
- does not alter scrolling
- does not change focus or pointer behavior
- does not create accessible content

## Validation fixtures

Temporary colored geometry can be enabled only together with development mode:

```text
?dev=1&decorations=bubble-inside
?dev=1&decorations=bubble-outside
?dev=1&decorations=avatar-outside
```

These fixtures validate the layer contract and are absent from the production
URL. They are not theme examples or production visual assets.
