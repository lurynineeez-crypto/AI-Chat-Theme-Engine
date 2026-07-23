# PRODUCT SCOPE

Version: 0.2.0-draft  
Status: Authoritative Draft

## Product Definition

AI Chat Theme Engine is a production pipeline and lightweight runtime for turning one coherent visual theme into an installable AI chat Theme Pack.

中文说明：
当前产品首先解决“主题如何稳定落地并交付”的问题，而不是先建立一个宏大的通用前端框架。

## Primary Product

The primary deliverable is the **Theme Pack**.

A Theme Pack should be:

- visually consistent
- installable
- versioned
- maintainable
- independent from one-off screenshots
- usable by a fixed Host UI without component rewrites

## Supporting Infrastructure

The loader and runtime exist only to prove that Theme Packs can be applied reliably.

They are supporting infrastructure, not the current commercial product.

## Current Users

- Theme creator / product owner
- AI design assistant
- Codex or another implementation assistant
- End user installing a theme into a compatible chat frontend

## In Scope for v0.2

- Theme creative exploration
- Theme DNA
- Flat Asset Master
- Mobile Landing Master
- Component skin mapping
- Production asset packaging
- One-file `theme.json`
- One fixed Host UI
- One reference theme
- Theme loading and visual switching proof

## Out of Scope for v0.2

- Universal cross-application standard
- Theme Marketplace
- Plugin ecosystem
- User accounts
- Cloud sync
- Automatic online installation
- Manifest + Modules as a mandatory architecture
- Complex animation or sound systems

## North Star

A user should be able to install a Theme Pack and change the visual identity of the chat interface without changing its component behavior or page structure.
