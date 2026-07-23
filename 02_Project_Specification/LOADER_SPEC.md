# LOADER_SPEC.md

Version: 0.1.1
Status: Draft

## Purpose

Define Theme Pack loading responsibilities.

中文说明：
Loader负责读取主题包，不负责设计和渲染。

## Responsibilities

- Read Manifest
- Validate files
- Load modules
- Prepare runtime data

## Flow

Theme Pack
↓
Manifest
↓
Modules
↓
Engine

## Rules

Loader should remain independent from specific Themes.
