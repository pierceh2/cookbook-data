import argparse
import json
from dates import today_iso
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('recipe_id')
    args = parser.parse_args()

    recipe_path = Path(__file__).resolve().parent.parent / 'recipes' / args.recipe_id / 'recipe.json'
    if not recipe_path.exists():
        raise FileNotFoundError(recipe_path)

    recipe = json.loads(recipe_path.read_text())
    if recipe.get('status') == 'made':
        print('Already marked as made.')
        return

    today = today_iso()
    recipe['status'] = 'made'
    recipe['madeAt'] = today
    recipe['updatedAt'] = today
    recipe['sprite'] = recipe.get('sprite') or 'sprite.png'
    recipe_path.write_text(json.dumps(recipe, indent=2) + '\n')
    print(f'Promoted {args.recipe_id} to made status.')


if __name__ == '__main__':
    main()
