# ASSET_SPEC.md

Version: 0.1.1
Status: Draft

## Purpose

Define how Theme assets are organized and maintained.

中文说明：
规范主题资源，保证可拆分、可维护、可复用。

## Principles

Assets should be:

- Reusable
- Clearly named
- Separated by responsibility
- Independent from application code

## Suggested Structure

```
assets/
├── background/
├── illustration/
├── icons/
└── decorations/
```

## Rules

Do not mix source files and production assets.
Do not use unclear names such as final.png.

中文说明：
资源命名必须长期可维护。
