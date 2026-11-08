import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text())


def validate_recipe(recipe):
    schema = json.loads((ROOT / 'schema' / 'recipe.schema.json').read_text())
    Draft202012Validator(schema).validate(recipe)


def compute_recipe_entry(recipe_path: Path):
    recipe = read_json(recipe_path)
    validate_recipe(recipe)
    recipe_dir = recipe_path.parent
    if recipe.get('status') == 'wishlist':
        sprite_rel = 'style/wishlist_placeholder.png'
        sprite_file = ROOT / 'style' / 'wishlist_placeholder.png'
    else:
        sprite_rel = ('recipes/' + recipe_dir.name + '/sprite.png')
        sprite_file = recipe_dir / 'sprite.png'
    photo_rel = None
    if recipe.get('photo'):
        photo_rel = ('recipes/' + recipe_dir.name + '/' + recipe['photo'])
    item = dict(recipe)
    item['spritePath'] = sprite_rel
    item['photoPath'] = photo_rel
    recipe_bytes = recipe_path.read_bytes()
    sprite_bytes = sprite_file.read_bytes() if sprite_file.exists() else b''
    item['contentHash'] = sha256_bytes(recipe_bytes + sprite_bytes)
    return item


def build_cookbook():
    recipes = []
    for path in sorted((ROOT / 'recipes').glob('*/recipe.json')):
        recipes.append(compute_recipe_entry(path))
    recipes.sort(key=lambda item: (item.get('title') or '').lower())
    payload = {
        'schemaVersion': 1,
        'generatedAt': '',
        'recipeCount': len(recipes),
        'madeCount': sum(1 for r in recipes if r.get('status') == 'made'),
        'wishlistCount': sum(1 for r in recipes if r.get('status') == 'wishlist'),
        'recipes': recipes,
    }
    previous = None
    existing = ROOT / 'cookbook.json'
    if existing.exists():
        try:
            previous = json.loads(existing.read_text())
        except Exception:
            previous = None
    payload_without_generated = {k: v for k, v in payload.items() if k != 'generatedAt'}
    if previous is not None:
        previous_without_generated = {k: v for k, v in previous.items() if k != 'generatedAt'}
        if previous_without_generated == payload_without_generated:
            payload['generatedAt'] = previous.get('generatedAt', datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
        else:
            payload['generatedAt'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    else:
        payload['generatedAt'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    text = json.dumps(payload, indent=2, sort_keys=True) + '\n'
    return payload, text


def main():
    payload, text = build_cookbook()
    (ROOT / 'cookbook.json').write_text(text)
    print(f'Wrote {ROOT / "cookbook.json"} with {payload["recipeCount"]} recipes.')


if __name__ == '__main__':
    main()
