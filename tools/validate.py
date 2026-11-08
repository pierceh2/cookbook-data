import json
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def load_schema(name: str):
    return json.loads((ROOT / name).read_text())


def render_matches(recipe_dir: Path):
    subprocess.run([
        sys.executable,
        str(ROOT / 'tools' / 'render_sprite.py'),
        str(recipe_dir.relative_to(ROOT)),
    ], cwd=str(ROOT), check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    sprite_png = recipe_dir / 'sprite.png'
    return sprite_png.exists() and sprite_png.stat().st_size > 0


def main():
    errors = []
    recipe_schema = load_schema('schema/recipe.schema.json')
    for recipe_dir in sorted((ROOT / 'recipes').glob('*')):
        if not recipe_dir.is_dir():
            continue
        recipe_path = recipe_dir / 'recipe.json'
        if not recipe_path.exists():
            errors.append(f'Missing recipe.json for {recipe_dir.name}')
            continue
        recipe = json.loads(recipe_path.read_text())
        try:
            Draft202012Validator(recipe_schema).validate(recipe)
        except Exception as exc:
            errors.append(f'{recipe_path}: {exc}')
        if recipe.get('id') != recipe_dir.name:
            errors.append(f'Folder name mismatch: {recipe_dir.name} != {recipe.get("id")}')
        if recipe.get('status') == 'wishlist':
            if recipe.get('madeAt') is not None:
                errors.append(f'Wishlist recipe {recipe.get("id")} has a madeAt value')
            if recipe.get('ingredients') and len(recipe['ingredients']) != 0:
                errors.append(f'Wishlist recipe {recipe.get("id")} must have empty ingredients')
            if recipe.get('steps') and len(recipe['steps']) != 0:
                errors.append(f'Wishlist recipe {recipe.get("id")} must have empty steps')
        if recipe.get('status') == 'made':
            if not recipe.get('sprite'):
                errors.append(f'Made recipe {recipe.get("id")} missing sprite')
            if recipe.get('ingredients') is None or len(recipe['ingredients']) == 0:
                errors.append(f'Made recipe {recipe.get("id")} must have at least one ingredient')
            if recipe.get('steps') is None or len(recipe['steps']) == 0:
                errors.append(f'Made recipe {recipe.get("id")} must have at least one step')
        sprite = recipe.get('sprite')
        if sprite:
            sprite_path = recipe_dir / sprite
            if not sprite_path.exists():
                errors.append(f'Missing sprite asset for {recipe.get("id")}: {sprite_path}')
            elif not (recipe_dir / 'sprite.py').exists():
                errors.append(f'Missing sprite.py for {recipe.get("id")}')
            elif not render_matches(recipe_dir):
                errors.append(f'Sprite render mismatch for {recipe.get("id")}')
        for ingredient in recipe.get('ingredients', []):
            if ingredient.get('name') and ingredient['name'] != ingredient['name'].lower():
                errors.append(f'Ingredient name must be lowercase for {recipe.get("id")}: {ingredient.get("name")}')

    import tools.build_index as builder
    expected_payload, _ = builder.build_cookbook()
    actual = json.loads((ROOT / 'cookbook.json').read_text()) if (ROOT / 'cookbook.json').exists() else {}
    if actual != expected_payload:
        errors.append('cookbook.json is out of date; run python tools/build_index.py')

    if errors:
        for error in errors:
            print(f'ERROR: {error}')
        raise SystemExit(1)

    print('All validations passed.')


if __name__ == '__main__':
    main()
