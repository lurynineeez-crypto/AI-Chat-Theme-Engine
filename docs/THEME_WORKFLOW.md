# THEME WORKFLOW

Version: 0.2.0-draft  
Status: Authoritative Draft

## Purpose

Define the validated production workflow for creating a Theme Pack.

中文说明：
本流程来自企鹅、植物、中国风、EDM、九尾狐和《风中的愿望》的真实试验，不是凭空设计的理论流程。

## Production Flow

```text
Theme Keywords
↓
Three Creative Directions
↓
Select One Direction
↓
Theme DNA
↓
Flat Asset Master
↓
Flat Mobile Landing Master
↓
Component Skin Mapping
↓
Production Asset Extraction
↓
Theme Pack
↓
Real Interface QA
```

Premium Design is an optional branch after the Flat system is approved. A Flat Theme Pack may be released without a Premium version.

## Stage 1 — Theme Keywords

Define the subject, emotional tone, target style, product tier, and hard negative constraints.

## Stage 2 — Three Creative Directions

Generate three meaningfully different visual directions. Do not merely change colors.

## Stage 3 — Theme DNA

Lock:

- world and mood
- one primary visual
- core elements
- palette
- shape language
- decorative language
- motion language
- negative constraints
- whitespace rules

## Stage 4 — Flat Asset Master

Create the source-of-truth design board for the theme language.

It must show reusable visual grammar rather than a finished poster or a one-off chat screenshot.

## Stage 5 — Flat Mobile Landing Master

Translate the Asset Master into a real phone chat interface.

This master must strictly inherit the same palette, shapes, visual hierarchy, primary visual, and decorative language. It may adapt placement for usability, but must not invent a second theme.

## Stage 6 — Component Skin Mapping

Map the approved theme language onto fixed Host UI slots:

- background
- incoming bubble
- outgoing bubble
- input
- primary button
- avatar frame
- optional decorative slots

## Stage 7 — Production Asset Extraction

Export only implementation-ready assets with stable names, correct transparency, clear dimensions, and no baked-in UI text unless explicitly required.

## Stage 8 — Theme Pack

Package configuration, assets, previews, documentation, and version information.

## Stage 9 — Real Interface QA

Compare the implementation against the Mobile Landing Master.

Reject the result when:

- components drift from the fixed Host UI
- the theme no longer resembles the Asset Master
- decorations block content or touch targets
- mobile safe areas fail
- assets are inconsistent across screens

## Non-Negotiable Rules

1. One theme, one primary visual.
2. Flat is the source of truth.
3. Mobile Landing Master must inherit the Asset Master.
4. Theme assets fill predefined slots; they do not redesign component behavior.
5. No new standard is added until a real theme requires it.
