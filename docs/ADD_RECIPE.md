# Add-Recipe Workflow

You maintain my cookbook repo. When I send a dish photo and/or say "new recipe" (or "edit <recipe>"), follow these steps in order. New recipes get `status: "made"` and `madeAt` set to today. For dishes I haven't made yet, use the Wishlist section further down instead. Follow `schema/recipe.schema.json` and `style/SPRITE_STYLE.md` exactly. Never invent recipe facts. If something is missing, ask me or leave the optional field null.

**Dates.** "Today" always means my local date in US Eastern time (`America/New_York`), never the container's UTC date. Get it with `TZ=America/New_York date +%F`. The tools (`new_recipe.py`, `promote.py`) already use Eastern time via `tools/dates.py`.

**Reminders.** The iOS app sends the daily reminder. Claude never schedules check-ins, reminders or recurring tasks for this cookbook.

**Samples.** `recipes/sample-*` are placeholder examples. They're tagged `sample`, and their descriptions start with `[Sample]`. Leave them alone unless I ask. Don't use them as neighbors when judging style. Mark them "(sample)" in any list you show me.

## Step 1: Intake (one message)

Look at the photo and anything I wrote. Then send me one message with:

* Your guess at the dish name, a proposed `id`, and a draft 1–3 sentence description, for me to confirm or fix. The `id` must equal what `tools/new_recipe.py` will produce from the title: lowercase, with runs of non-alphanumerics turned into `-`. Change the title if you need a different id.
* A short checklist of only the things still missing. Use this order:
   1. Ingredients (required). Ask me to paste them as free text, any format, one per line. Group headings like "Sauce:" are fine.
   2. Steps (required). Free text or a numbered list.
   3. Servings, prep minutes, cook minutes (optional).
   4. Tips and notes (optional, free text, any length).
   5. Source (optional: a person, book or URL).
   6. Tags. Suggest 3–5 (course, main protein, cuisine, method) for me to accept or edit.
   7. Whether to keep the original photo in the repo (default yes).

Don't ask for anything I've already told you. If I reply "skip" to an optional field, set it to null.

## Step 2: Normalize

* Keep each ingredient line exactly as I wrote it in `line`. Fix only obvious typos, and tell me which ones.
* Make `name` lowercase, singular, with no quantity, unit, brand or prep words. Examples: "2 cloves garlic, minced" → `garlic`; "1 (14 oz) can San Marzano tomatoes" → `tomato`; "kosher salt" → `salt`. Before inventing a new name, check `cookbook.json` for one that already exists and reuse it (e.g. always `scallion`, never sometimes `green onion`).
* Turn a line ending in ":" into the `group` for the lines below it.
* Split steps into one action-sized paragraph each. Strip numbering.
* Keep my tips and notes text as written (Markdown is fine).
* Set `createdAt` and `updatedAt` to today (Eastern). On edits, change only `updatedAt`.

## Step 3: Draw the sprite

You draw the sprite yourself as 64×64 pixel art, using my photo as a reference for what the dish is. The look comes from my app: cozy medieval-fantasy pixel art, like an item on a candlelit tavern table or a potion-shop shelf. Before drawing, read `style/SPRITE_STYLE.md` and `style/palette.hex`, look at the app screenshots in `style/reference/`, and open 2–3 existing `recipes/*/sprite.py` files (non-sample ones once they exist) to match their style. The key traits: warm candlelight from the top-left with cool navy or plum shadows, 3–4 tone shading, a warm rim light, cream glints on anything glossy, and rustic serveware (earthenware, wood, cast iron, thick glass).

1. Study the photo and note: the serveware (`plate`, `bowl`, `board`, `pan`, `glass` or `none`), the main shapes and their colors, and the 2–4 details that make the dish recognizable (e.g. basil leaves, char marks, a sauce swirl). Simplify: at 64×64, a few clear shapes read better than lots of detail.
2. If there's a photo and I said to keep it, save it with `python tools/resize_photo.py <photo> recipes/<id>` and set `"photo": "photo.jpg"`. If the photo I attached isn't available as a file in the session, tell me and set `photo` to null rather than skipping silently.
3. Write `recipes/<id>/sprite.py` with the `spritekit` API: serveware first, then the main food shapes, then shading with top-left light, then the small details. Use only palette colors by name. Don't draw an outer outline or ground shadow; the renderer adds those (shadow underneath, 1px outline around the silhouette). Keep drawing inside the 2px margin.
4. Render it with `python tools/render_sprite.py recipes/<id> --preview`. This writes `.preview/<id>_preview.png`: the sprite on parchment, on dark wood, and at half size next to up to 3 neighboring sprites on the app's navy. Look at it yourself and check four things: Is it clearly the dish? Does it look like it belongs in the reference screenshots (warm light, cool shadows, glints)? Does it read on both the parchment and the dark-wood panels? Does it match the neighboring sprites? Revise until all four are true (up to 3 rounds before showing me).
5. Show me the preview by sending the `.preview/<id>_preview.png` file. If I ask for changes ("more cheese", "darker crust", "use a bowl"), edit `sprite.py` and re-render.
6. Never change the palette, the spritekit helpers or the style spec to make one sprite work. If the palette is missing a color the dish really needs, tell me and propose a style version bump instead.

## Step 4: Review before writing

Show me the final `recipe.json` in a code block, plus the sprite preview, and ask "Commit this?" Don't commit until I say yes. Apply any changes I ask for and show the result again.

## Step 5: Commit

1. Create the folder with `tools/new_recipe.py` (new recipes only) and write `recipe.json`. Overwrite every placeholder value the tool writes (description, servings, times, ingredients, steps) with the real values, or null.
2. Run `make index`, then `make validate`. Fix any failures. Never edit `cookbook.json` by hand.
3. Commit only that recipe's folder (`recipe.json`, `sprite.py`, `sprite.png`, and `photo.jpg` if kept) and `cookbook.json`, with the message `Add recipe: <Title>` (or `Update recipe: <Title>`).
4. Push directly to `main` (`git pull --rebase origin main` first, then `git push origin HEAD:main`). Only use a branch `recipe/<id>` and a PR if I ask for PRs.
5. Reply with one line confirming it's live, plus the recipe's path.

## Wishlist (dishes I haven't made yet)

**Add to wishlist.** Use this when I say something like "wishlist: beef wellington", or send a link, screenshot or photo of a dish I want to try. Every wishlist dish gets its own sprite drawn by you; that sprite is what the app shows in the wishlist section of the cookbook. Keep it quick:

1. In one message, propose the title, `id` and a 1–2 sentence description. Then ask only:
   * Where it's from (a link, a person, a restaurant), which goes in `source`.
   * Why I want to make it, or anything to remember, which goes in `notes`.
   * If I pasted a recipe or link with ingredients, offer to save those in `notes` as text. `ingredients` and `steps` stay empty arrays for wishlist dishes (the schema requires it).
2. Create it with `python tools/new_recipe.py "<Title>" --wishlist` and fill in the fields. Don't invent ingredients or steps.
3. Draw the sprite exactly as in Step 3, using my link, screenshot, photo or the dish's description as the reference, and set `"sprite": "sprite.png"`. Use the covered-dish placeholder (`"sprite": null`) only if I explicitly say "no sprite" or "placeholder".
4. Show me the JSON and the preview, wait for "yes", then commit as in Step 5 with the message `Wishlist: <Title>`.

**"I made it!"** Use this when I say I've made a wishlist dish (e.g. "made the wellington", usually with a photo):

1. Find the entry and run `python tools/promote.py <id>`.
2. Run the normal intake (Step 1), asking only for what's still missing: ingredients and steps as I actually made them, times, tips and notes ("what would you change next time?"), and a photo of my version.
3. Redraw the sprite from my photo (Step 3), editing the existing wishlist `sprite.py` so it shows my version.
4. Keep the original `source` and wishlist `notes`, and add my new notes below them.
5. Review (Step 4) and commit with the message `Made it: <Title>`.

**Other wishlist requests.** "What's on my wishlist?" means list the titles and sources of `status: "wishlist"` recipes from `cookbook.json`, with samples marked "(sample)". "Remove X from the wishlist" follows the delete rules below.

## Opening from the app's reminder

If a session starts with "Add a recipe" (from the app's daily reminder), go straight to Step 1: ask for a photo or the dish name, and add one suggestion from `cookbook.json` (a non-sample wishlist dish, or the recipe with the oldest `madeAt`). If I already added or made something today (Eastern), mention it in one line. Never commit anything without my answer.

## Edits and deletes

* Edit: load the existing `recipe.json`, show me just the fields that will change, then repeat Steps 4–5. Redraw the sprite only if I ask or send a new photo. To tweak it, edit the existing `sprite.py` rather than starting over.
* No photo: you can still draw the sprite from the recipe and my description. Show me the preview as usual.
* Delete: confirm the title with me first, remove the folder, rebuild the index, validate, and commit `Remove recipe: <Title>`.

## Never

* Change the schema, palette, style spec or tools unless I explicitly ask. If I do, bump `schemaVersion` or the style version and tell me the iOS app may need updating.
* Commit preview images (`.preview/`), temp files or secrets.
* Schedule reminders or recurring tasks; the app owns reminders.
