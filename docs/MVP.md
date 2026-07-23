# MVP

Version: 0.2.0-draft  
Status: Authoritative Draft

## Validation Question

Can one fixed chat interface apply and remove a Theme Pack without changing component source code?

中文说明：
MVP 不再只验证“JavaScript 能读取 JSON”，而要验证我们的核心产品主张：同一套组件可以被主题包稳定换肤。

## Inputs

### Host UI

Select one stable implementation from the three existing chat interface versions.

It must include:

- message list
- incoming and outgoing bubbles
- input area
- primary action button
- avatar region
- desktop and mobile layouts

### Reference Theme

`Wish in the Wind`.

The approved Flat Asset Master and Mobile Landing Master are the visual source of truth.

## Required Theme Mapping

- page background
- incoming bubble
- outgoing bubble
- input
- primary button
- avatar frame

## Required Behavior

1. Load `themes/wish-in-the-wind/theme.json`.
2. Validate required identity and compatibility fields.
3. Resolve referenced asset paths.
4. Apply tokens and component skins.
5. Preserve Host UI structure and interactions.
6. Allow returning to the default theme without a reload.

## Definition of Done

The MVP is complete when:

- the same HTML/component structure is used before and after theming
- no Host UI component source file is edited to install the theme
- all required mapping slots are applied from `theme.json`
- missing optional slots fall back safely
- invalid paths produce an understandable error
- mobile and desktop layouts remain usable
- implementation visually matches the Mobile Landing Master
- default and Wish in the Wind themes can be switched for comparison

## Explicitly Out of Scope

- Marketplace
- remote downloads
- plugin API
- multiple third-party Host UIs
- automatic installation
- complex animation runtime
- sound packs
- Premium rendering requirements
- mandatory Manifest + Modules architecture

## Deliverables

```text
examples/theme-loader-demo/
themes/wish-in-the-wind/
docs/implementation-notes.md
```

The Sprint ends after this proof works and is reviewed. New abstractions are evaluated only after the implementation evidence exists.
