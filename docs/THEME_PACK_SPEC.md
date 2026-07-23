# THEME PACK SPECIFICATION

Version: 0.2.0-draft  
Status: Authoritative Draft

## Purpose

Define the smallest Theme Pack needed to validate the product.

中文说明：
v0.2 不强制 Manifest + Modules。先用一套真实主题证明单文件配置能否满足需求，再根据实际复杂度决定是否拆分。

## Required Structure

```text
themes/<theme-id>/
├── theme.json
├── README.md
├── preview/
│   ├── mobile.png
│   └── desktop.png
└── assets/
    ├── background/
    ├── decorations/
    ├── avatar/
    └── icons/
```

Only include directories that contain real files. Empty placeholder folders are not required.

## Required `theme.json` Fields

```json
{
  "id": "wish-in-the-wind",
  "name": "Wish in the Wind",
  "version": "0.1.0",
  "status": "draft",
  "compatibility": {
    "host": "ai-chat-theme-demo",
    "minimumVersion": "0.1.0"
  },
  "tokens": {},
  "components": {},
  "assets": {}
}
```

### Identity

- `id`: stable lowercase kebab-case identifier
- `name`: display name
- `version`: semantic version
- `status`: `draft`, `preview`, or `released`

### Compatibility

Declares the Host UI and minimum compatible version.

### Tokens

Global colors and bounded style values exposed by the Host UI.

### Components

Skin values for the slots defined in `COMPONENT_SKIN_CONTRACT.md`.

### Assets

Relative paths from the Theme Pack root. Absolute paths are prohibited.

## Packaging Rules

- A Theme Pack contains no application source code.
- Asset names must be stable and descriptive.
- Production assets and source design files must not be mixed.
- Missing optional fields use Host UI defaults.
- Missing required fields fail validation.
- Unknown fields should be ignored with a warning during the draft phase.

## Reference Package Is Separate

Design masters, Theme DNA, mapping notes, and extraction instructions belong to the Reference Package, not the installable Theme Pack.

They may live beside the theme during development but must not be required at runtime.

## When to Consider Modules

Do not split `theme.json` until a real implementation demonstrates at least one concrete need, such as repeated merge conflicts, independent lazy loading, or configuration size that materially harms maintenance.
