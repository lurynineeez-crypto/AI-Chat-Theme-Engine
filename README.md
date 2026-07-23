# AI Chat Theme Engine

> Turn a consistent visual theme into an installable AI chat Theme Pack.

AI Chat Theme Engine is a production pipeline and lightweight runtime for creating, packaging, loading, and validating reusable AI chat themes.

中文说明：
本项目首先服务于真实的聊天主题生产与交付。当前目标不是建立通用开放标准或主题市场，而是让一套主题能够稳定地从设计母版进入真实聊天界面。

## Current Product Scope

- Create a consistent Theme DNA.
- Produce a Flat Asset Master.
- Produce a Mobile Landing Master that strictly inherits the Asset Master.
- Map theme language onto a fixed Host UI.
- Package production assets as a Theme Pack.
- Load the Theme Pack without rewriting component code.

## Core Rules

1. Theme changes visual language, not component behavior.
2. Component structure belongs to the Host UI.
3. Flat Design is the source of truth.
4. Premium Design is optional, not a release requirement.
5. Real implementations come before abstractions.
6. A Theme Pack is the product; the runtime is supporting infrastructure.

## Authoritative Documentation

Read the current v0.2 documents in this order:

1. `docs/START_HERE.md`
2. `docs/PRODUCT_SCOPE.md`
3. `docs/THEME_WORKFLOW.md`
4. `docs/COMPONENT_SKIN_CONTRACT.md`
5. `docs/THEME_PACK_SPEC.md`
6. `docs/MVP.md`

The numbered v0.1 folders are legacy foundation drafts and are not authoritative for implementation.

## Current Milestone

Validate one real theme, **Wish in the Wind**, against one fixed chat interface.

Success means the same HTML structure and component behavior can be reskinned through a Theme Pack without editing component source code.
