# Host UI Requirements

Version: 0.2.0  
Status: Approved for structural prototype  
Authority: Current implementation baseline

## Purpose

Define the first clean Host UI for AI Chat Theme Engine.

This Host UI will be implemented from scratch. The deleted V1.0, V1.2 and V1.3 demos are failure references only. Their HTML, CSS, JavaScript and layout structure must not be reconstructed or used as an implementation base.

中文说明：
旧三版只保留问题结论，不保留代码继承关系。新的 Host UI 是一套完整但克制的 AI 聊天应用外壳，而不是旧 Demo 的 V1.4。

## Product Scope

The first Host UI is a complete local AI chat application shell used to validate reusable visual themes across the whole product surface.

It includes:

- Desktop application shell
- Responsive mobile application shell
- Conversation sidebar
- Brand / application identity area
- New chat action
- Local conversation search/filter
- Scrollable conversation list
- Current conversation state
- Account / settings entry area
- Main chat header and Host-owned actions
- Message list
- Incoming and outgoing messages
- Avatar and message metadata
- Empty, loading and error states
- Multiline composer
- Primary send action
- Mobile sidebar drawer
- Menu and dialog overlay roots
- Reserved non-interactive theme decoration anchors
- Local mock data and local interactions

It does not include:

- Account authentication
- Cloud synchronization
- Real AI or backend API
- Persistent database storage
- File upload
- Voice input
- Multi-user chat
- Plugin system
- Theme Pack loader
- Theme switching
- Theme marketplace
- Full settings center
- Advanced global search

中文说明：
第一版要结构完整，但功能克制。它必须像一个真正的聊天应用，而不是只展示几条气泡；同时不能借机扩成完整商业产品。

## Core Product Rules

1. The Host owns structure, behavior, accessibility and responsive layout.
2. Themes may change approved visual values and assets only.
3. The Host must remain visually neutral.
4. Desktop uses a persistent sidebar and a main workspace.
5. Mobile uses a Host-owned sidebar drawer instead of compressing the desktop sidebar.
6. Sidebar and message list own their own scroll regions; normal application use must not rely on document scrolling.
7. Header and composer remain available while reading a long conversation.
8. Mobile viewport, software keyboard and safe areas are first-class requirements.
9. Theme decorations must never change layout or intercept input.
10. The Host must still work when all optional theme assets are missing.
11. Local mock data must demonstrate real application states without requiring a backend.
12. The first implementation must validate the application shell before Theme Pack work begins.

## Information Architecture

```text
Application Shell
├── Sidebar
│   ├── Brand / application identity
│   ├── New chat action
│   ├── Conversation search/filter
│   ├── Conversation list viewport
│   │   ├── Conversation item
│   │   ├── Active state
│   │   ├── Hover/focus state
│   │   └── Long-title truncation
│   └── Account / settings entry
├── Main Workspace
│   ├── Chat Header
│   │   ├── Mobile sidebar trigger
│   │   ├── Conversation identity
│   │   └── Host-owned actions
│   ├── Chat Content
│   │   ├── Empty state
│   │   ├── Loading state
│   │   ├── Error state
│   │   └── Message viewport
│   │       ├── Message group
│   │       ├── Incoming message
│   │       ├── Outgoing message
│   │       ├── Avatar
│   │       ├── Bubble content
│   │       └── Timestamp / delivery state
│   └── Composer
│       ├── Multiline text input
│       ├── Optional Host-owned actions
│       └── Primary send button
└── Overlay Layer
    ├── Mobile sidebar backdrop
    ├── Mobile sidebar drawer
    ├── Menus
    ├── Dialogs
    └── Theme decoration roots
```

## Required Behavior

### Application shell

- Fills the available dynamic viewport.
- Prevents normal document-level scrolling.
- Separates sidebar, main workspace and overlay layers clearly.
- Supports both light and dark neutral appearances for QA.
- Remains usable when optional decorative assets are absent.

### Sidebar

- Remains visible on desktop.
- Becomes a dismissible drawer on mobile.
- Opens from a clear header trigger on mobile.
- Closes through the close action, backdrop interaction and Escape key when appropriate.
- Traps focus while acting as a modal drawer.
- Restores focus to the opening control after closing.
- Contains an independently scrolling conversation list.
- Supports local filtering by conversation title.
- Supports creating a new local conversation.
- Supports selecting an existing conversation.
- Clearly indicates the active conversation.
- Handles long titles without horizontal overflow.
- Keeps account/settings entry available without overlapping the list.

### Conversation data

- Uses local mock data only.
- Includes enough conversations to validate sidebar scrolling.
- Includes short and long conversation titles.
- Includes an empty conversation.
- Includes a long conversation.
- Switching conversations updates the main workspace locally.
- Creating a new conversation produces a usable empty state.
- Persistence across page reload is not required in v0.2.

### Message viewport

- Scrolls independently from the document.
- Opens at the newest message for the selected conversation.
- Auto-scrolls after the local user sends a message when already near the bottom.
- Does not force the user to the bottom while they are reading older messages.
- Supports long conversations, long words, URLs, code-like text and multiline content without horizontal overflow.
- Resets or restores an appropriate scroll position when changing conversations.

### Composer

- Uses a multiline text input.
- Grows within a bounded height, then scrolls internally.
- Enter sends when composition rules permit.
- Shift+Enter creates a newline.
- Empty or whitespace-only input does not submit.
- Supports visible default, focus, disabled, loading and error states.
- Primary touch target is at least 44×44 CSS pixels on mobile.
- Sending a local message updates the active conversation and its sidebar preview/time locally.
- No simulated AI reply is required unless implemented as a clearly separated test fixture.

### Chat states

The Host must visibly demonstrate:

- Empty conversation state
- Populated conversation state
- Loading state
- Recoverable error state
- Disabled composer state
- Long-content state

These states may be switched through a development harness or deterministic local fixtures.

### Responsive layout

- Works at minimum at 1440×900, 1200×900 and 390×844.
- Uses dynamic viewport sizing where appropriate.
- Supports `env(safe-area-inset-*)`.
- Does not rely on fixed device heights.
- Keeps header and composer visible during normal use.
- Does not create document-level horizontal scrolling.
- Uses a persistent desktop sidebar and a modal/drawer sidebar on mobile.
- Does not shrink the desktop sidebar into an unusable narrow rail unless a future requirement explicitly adds that mode.

### Accessibility

- Logical keyboard focus order.
- Visible focus indication.
- Accessible labels for icon-only actions.
- Sufficient neutral-theme contrast.
- Reduced-motion support.
- Drawer focus management and Escape behavior.
- Decorative layers remain outside meaningful accessibility content.
- Interactive targets meet mobile minimum sizes.
- Status information is not communicated by color alone.

## Stable Host Components

The first structural prototype must establish durable hooks for:

- Application shell
- Sidebar
- Brand area
- New chat button
- Conversation search
- Conversation list
- Conversation item
- Account/settings area
- Main workspace
- Chat header
- Header actions
- Mobile sidebar trigger
- Message viewport
- Message group
- Incoming message
- Outgoing message
- Bubble
- Avatar
- Timestamp / delivery state
- Empty state
- Loading state
- Error state
- Composer
- Text input
- Primary send button
- Overlay root
- Mobile drawer and backdrop

Theme authors must not depend on fragile descendant selectors.

## Immutable Host Contract

Themes must not change:

- Semantic hierarchy or DOM order
- Sidebar behavior or mobile drawer behavior
- Conversation ordering and selection logic
- Message ordering and incoming/outgoing alignment
- Component positions
- Sidebar width bounds and message width bounds
- Scroll ownership or bottom anchoring
- Composer behavior
- Breakpoints and safe-area behavior
- Touch target dimensions
- Focus order or accessible names
- Drawer focus management
- Runtime states and business logic
- Z-index bands owned by the Host
- Network behavior or event handling
- Local data semantics

## Future Theme Skin Slots

The Host should reserve stable, bounded slots for later theme work:

### Global application

- Application background
- Main workspace background
- Non-interactive global overlay
- Global text, muted, accent, border, status and focus colors
- Bounded typography tokens

### Sidebar

- Sidebar surface
- Brand area surface and approved brand decoration anchor
- New chat button skin
- Search input skin
- Conversation item default, hover, focus and active skins
- Sidebar divider and shadow tokens
- Account/settings area skin
- Mobile drawer surface and backdrop visual token
- Approved sidebar decorative overlay anchors

### Chat header

- Header surface
- Header text and muted colors
- Header divider/shadow
- Approved icon skins and tints
- Non-interactive header decoration anchor

### Messages

- Incoming bubble fill, border, radius, shadow and fixed decoration anchors
- Outgoing bubble fill, border, radius, shadow and fixed decoration anchors
- Avatar frame anchor
- Timestamp and delivery-state colors
- Limited bubble padding tokens within Host-defined bounds

### Composer

- Composer surface
- Input surface, border, focus ring, radius and decoration anchor
- Primary button visual tokens
- Approved composer action icon skins
- Non-interactive composer decoration anchor

### States and overlays

- Empty-state illustration slot
- Loading-state visual tokens
- Error-state visual tokens
- Menu and dialog surface tokens
- Approved non-interactive overlay assets

These slots are reserved during Host implementation, but Theme Pack loading is not part of this stage.

## Decoration Layer Rules

- The Host owns all decoration anchor elements.
- Themes may supply bounded values and assets only.
- Themes may not inject arbitrary HTML or JavaScript.
- Decorative layers use `pointer-events: none`.
- Decorative layers stay outside accessible content.
- Decorative layers obey fixed clipping and z-index bands.
- Missing optional assets must fail safely without changing layout.
- Arbitrary ownership of component `::before` and `::after` pseudo-elements is not the public theme contract.

## Neutral Baseline

The first implementation must not contain a recognizable commercial Theme.

Do not include:

- Nine-tail fox visual language
- Dandelion visual language
- Decorative particles or premium glow
- Theme-specific background art
- Tail SVGs or ornamental avatar frames

Use a clean, restrained neutral appearance only. Visual polish must remain secondary to layout and behavior validation.

## Implementation Order

1. Structural application shell
2. Desktop sidebar and main workspace
3. Mobile drawer behavior
4. Conversation selection and local data
5. Message viewport and composer behavior
6. Empty/loading/error/disabled fixtures
7. Accessibility and responsive validation
8. Stable theme anchors and bounded visual tokens
9. Neutral visual cleanup
10. Review and stop

## Acceptance Criteria

The Host UI is ready for review when:

- It is implemented from scratch in a clean project location.
- It contains a complete application shell with sidebar and main workspace.
- Desktop sidebar and mobile drawer both work.
- Local new-chat, search/filter and conversation selection work.
- The page works on desktop and mobile.
- Sidebar list and message viewport scroll independently where needed.
- Normal application use does not require document scrolling.
- Header and composer remain visible.
- Sending and multiline input work locally.
- Long titles and long message content do not break layout.
- Empty, loading, error and disabled states are visible and testable.
- Decoration anchors exist but do not alter layout.
- All theme-specific visual assets are absent.
- Keyboard focus and mobile drawer behavior are validated.
- Screenshots and a short validation report are available.

## Stop Condition

After the neutral full-application Host UI passes review, stop.

Do not implement Theme Packs, a Loader, theme switching or Wish in the Wind until the Host UI itself is approved.