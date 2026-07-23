# START HERE

Version: 0.2.0-draft  
Status: Authoritative Draft

## Purpose

This is the entry point for the current project direction.

中文说明：
新加入的 ChatGPT、Codex、设计师或开发者应先读本文件。不要把旧的编号文档目录当作当前实现规范。

## Read Order

1. `PRODUCT_SCOPE.md`
2. `THEME_WORKFLOW.md`
3. `COMPONENT_SKIN_CONTRACT.md`
4. `THEME_PACK_SPEC.md`
5. `MVP.md`
6. `decisions/ADR-001-flat-first.md`

## Project in One Sentence

AI Chat Theme Engine turns a consistent visual theme into an installable Theme Pack for a fixed chat interface.

## Current Stage

The project is validating one real Theme Pack against one fixed Host UI.

Current reference theme: `Wish in the Wind`.

## Do Not Build Yet

- Marketplace
- Cross-application open standard
- Plugin ecosystem
- Cloud installation
- Complex modular manifests
- Premium-only rendering pipeline

## Core Decision Rule

When a new abstraction is proposed, first ask:

> Which real implementation problem requires it now?

If there is no concrete answer, record the idea and do not add it to v0.2.
