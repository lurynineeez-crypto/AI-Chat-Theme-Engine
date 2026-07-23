# Host UI Requirements

Version: 0.1.0  
Status: Draft  
Authority: Current implementation baseline

## Purpose

Define the first clean Host UI for AI Chat Theme Engine.

This Host UI will be implemented from scratch. The deleted V1.0, V1.2 and V1.3 demos are not code references and must not be reconstructed.

中文说明：
旧三版只证明了哪些做法会失败。新 Host UI 不继承旧 HTML、CSS、JavaScript 或布局结构。

## Product Scope

The first Host UI is a single-conversation chat surface used to validate reusable visual themes.

It includes:

- Chat header
- Message list
- Incoming and outgoing messages
- Avatar and message metadata
- Multiline composer
- Primary send action
- Runtime state hooks
- Responsive desktop and mobile behavior
- Reserved non-interactive theme decoration anchors

It does not include:

- Conversation sidebar
- Account system
- Settings center
- Backend or model API
- Persistence or synchronization
- Theme Pack loader
- Theme marketplace
- Plugin system

中文说明：
第一版只做一张真正可用、结构稳定的单会话页面。先把聊天核心做好，不扩成完整应用。

## Core Product Rules

1. The Host owns structure, behavior, accessibility and responsive layout.
2. Themes may change approved visual values and assets only.
3. The Host must remain visually neutral.
4. The message list is the only normal vertical scroll region.
5. Header and composer remain available while reading a long conversation.
6. Mobile viewport, software keyboard and safe areas are first-class requirements.
7. Theme decorations must never change layout or intercept input.
8. The Host must still work when all optional theme assets are missing.

## Information Architecture

```text
Host UI
├── Header
│   ├── Conversation identity
│   └── Host-owned actions
├── Message viewport
│   ├── Message group
│   ├── Incoming message
│   ├── Outgoing message
│   ├── Avatar
│   ├── Bubble content
│   └── Timestamp / delivery state
├── Composer
│   ├── Multiline text input
│   ├── Optional Host-owned actions
│   └── Primary send button
└── Decoration roots
    ├── Page overlay
    ├── Incoming bubble decoration
    ├── Outgoing bubble decoration
    ├── Avatar frame anchor
    └── Composer decoration
```

## Required Behavior

### Message viewport

- Scrolls independently from the document.
- Opens at the newest message.
- Auto-scrolls after the local user sends a message when already near the bottom.
- Does not force the user to the bottom while they are reading older messages.
- Supports long conversations, long words, URLs and multiline content without horizontal overflow.

### Composer

- Uses a multiline text input.
- Grows within a bounded height, then scrolls internally.
- Enter sends when composition rules permit.
- Shift+Enter creates a newline.
- Empty or whitespace-only input does not submit.
- Supports visible default, focus, disabled, loading and error states.
- Primary touch target is at least 44×44 CSS pixels on mobile.

### Responsive layout

- Works at minimum at 1200×900 and 390×844.
- Uses dynamic viewport sizing where appropriate.
- Supports `env(safe-area-inset-*)`.
- Does not rely on fixed device heights.
- Keeps header and composer visible during normal use.
- Does not create document-level horizontal scrolling.

### Accessibility

- Logical keyboard focus order.
- Visible focus indication.
- Accessible labels for icon-only actions.
- Sufficient neutral-theme contrast.
- Reduced-motion support.
- Decorative layers remain outside meaningful accessibility content.

## Immutable Host Contract

Themes must not change:

- Semantic hierarchy or DOM order
- Message ordering and incoming/outgoing alignment
- Component positions
- Message width bounds
- Scroll behavior or bottom anchoring
- Composer behavior
- Breakpoints and safe-area behavior
- Touch target dimensions
- Focus order or accessible names
- Runtime states and business logic
- Z-index bands owned by the Host
- Network behavior or event handling

## Future Theme Skin Slots

The Host should reserve stable, bounded slots for later theme work:

- Page background and non-interactive page overlay
- Header surface
- Incoming bubble fill, border, radius, shadow and decoration anchors
- Outgoing bubble fill, border, radius, shadow and decoration anchors
- Input surface, border, focus ring, radius and decoration anchor
- Primary button visual tokens
- Avatar frame anchor
- Approved icon skins and tints
- Text, muted, accent, border, status and focus colors
- Bounded typography tokens
- Limited bubble padding and decoration inset tokens

These slots are reserved during Host implementation, but Theme Pack loading is not part of this stage.

## Neutral Baseline

The first implementation must not contain a recognizable commercial Theme.

Do not include:

- Nine-tail fox visual language
- Dandelion visual language
- Decorative particles or premium glow
- Theme-specific background art
- Tail SVGs or ornamental avatar frames

Use a clean, restrained neutral appearance only.

## Acceptance Criteria

The Host UI is ready for review when:

- It is implemented from scratch in a clean project location.
- The page works on desktop and mobile.
- Only the message viewport scrolls during normal use.
- Header and composer remain visible.
- Sending and multiline input work locally.
- Long content does not break layout.
- Disabled, loading and error hooks are visible and testable.
- Decoration anchors exist but do not alter layout.
- All theme-specific visual assets are absent.
- Screenshots and a short validation report are available.

## Stop Condition

After the neutral Host UI passes review, stop.

Do not implement Theme Packs, a Loader or Wish in the Wind until the Host UI itself is approved.
