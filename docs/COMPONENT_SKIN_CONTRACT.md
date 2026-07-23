# COMPONENT SKIN CONTRACT

Version: 0.2.0-draft  
Status: Authoritative Draft

## Purpose

Define what the Host UI owns and what a Theme Pack may change.

中文说明：
这份契约用于解决“每生成一次主题，按钮、气泡和输入框都被重新设计”的问题。

## Fixed Host UI Responsibilities

The Host UI owns:

- semantic HTML and component hierarchy
- interaction behavior
- focus and keyboard behavior
- content layout
- responsive breakpoints
- minimum touch targets
- safe areas
- accessibility requirements
- message alignment rules
- component states and state transitions

A Theme Pack must not replace these responsibilities.

## Theme-Controlled Skin Slots

A Theme Pack may provide values or assets for approved slots.

### Global

- page background color or image
- text and muted text colors
- surface colors
- accent color
- border color
- approved font family fallback

### Incoming Bubble

- fill color
- text color
- border
- shadow within allowed range
- optional decorative SVG layer
- bubble-tail skin using the fixed tail anchor

### Outgoing Bubble

Same skin slots as Incoming Bubble, with independent values.

### Input

- surface color
- border color
- focus color
- placeholder color
- optional non-interactive decoration layer

### Primary Button

- fill
- text color
- border
- hover/pressed/focus tokens
- optional icon skin

### Avatar Frame

- frame asset
- inset and scale values within the approved range
- optional status decoration anchor

## Prohibited Theme Changes

A Theme Pack must not:

- change component DOM structure
- move controls to different regions
- change message alignment logic
- reduce touch targets
- hide required states
- introduce theme-specific business behavior
- bake chat content into decorative images
- require component source edits for installation

## Controlled Variability

Values such as radius, shadow, border width, and decorative inset may be theme-controlled only when the Host UI exposes them as bounded tokens.

The Engine must provide safe defaults when a Theme Pack omits an optional slot.

## Acceptance Rule

A theme passes the contract when it can be applied and removed without changing Host UI component source code.
