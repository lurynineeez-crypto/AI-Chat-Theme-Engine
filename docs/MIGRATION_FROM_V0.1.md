# Migration from v0.1 Foundation Draft

Version: 0.2.0-draft

## Why the Direction Changed

The v0.1 foundation correctly identified Theme/UI separation and Flat First, but it expanded too early into a generic framework, open standard, modular manifest architecture, and marketplace vision.

The repository also accumulated many short documents that looked complete but did not contain enough implementation decisions for Codex.

## v0.2 Corrections

- Theme Pack is restored as the primary product.
- The runtime is supporting infrastructure.
- The MVP validates a real component reskin, not metadata display.
- Mobile Landing Master is restored to the production workflow.
- Premium Design becomes optional.
- A single `theme.json` is the default for the first real implementation.
- Manifest + Modules is retained only as a future candidate.
- Current documentation is consolidated under `docs/`.

## Legacy Documents

The following directories are retained temporarily for history only:

- `01_Project_Starter_Kit/`
- `02_Project_Specification/`

They are not authoritative for new implementation work.

Do not delete them until the v0.2 documentation and first real Theme Pack have been reviewed together.
