# Sprite style guide (version 1)

Art direction: cozy medieval-fantasy pixel art. Each dish should feel like a prop from a candlelit wizard's library or a night-market potion stall. Sprites should feel like items you could pick up in a cozy fantasy RPG, sitting on a tavern table by candlelight.

- Canvas: 64x64 with transparent background. Export to 256x256 via 4x nearest-neighbor scaling.
- View: three-quarter top-down, centered, with the base resting on row 56.
- Lighting: warm amber candlelight from the top-left; cool navy/plum shadows face away. Use 3-4 tones per material.
- Outline: 1px warm-purple outline around the silhouette. Soft cool shadow ellipse under the base.
- Palette: fixed in `style/palette.hex`; never change it without a style version bump.
- Serveware: plate, bowl, board, pan, or glass. No modern objects or text.
- Wishlist placeholder: a covered dish with a domed cloche on a plate and a tiny parchment tag.
