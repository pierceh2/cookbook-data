import argparse
import json
import re
from datetime import date
from pathlib import Path


def slugify(title: str) -> str:
    slug = title.lower().strip()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = re.sub(r'-+', '-', slug).strip('-')
    if not slug:
        raise ValueError('Title produced an empty id')
    return slug


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('title')
    parser.add_argument('--wishlist', action='store_true')
    args = parser.parse_args()

    recipe_id = slugify(args.title)
    root = Path(__file__).resolve().parent.parent
    target = root / 'recipes' / recipe_id
    if target.exists():
        raise FileExistsError(f'Recipe id already exists: {recipe_id}')
    target.mkdir(parents=True)

    today = date.today().isoformat()
    if args.wishlist:
        payload = {
            'schemaVersion': 1,
            'id': recipe_id,
            'status': 'wishlist',
            'title': args.title,
            'description': 'Short 1-3 sentence blurb shown under the sprite.',
            'sprite': None,
            'photo': None,
            'servings': None,
            'prepMinutes': None,
            'cookMinutes': None,
            'tags': [],
            'ingredients': [],
            'steps': [],
            'tips': None,
            'notes': 'Why I want to make it.',
            'source': None,
            'createdAt': today,
            'updatedAt': today,
            'madeAt': None,
        }
    else:
        payload = {
            'schemaVersion': 1,
            'id': recipe_id,
            'status': 'made',
            'title': args.title,
            'description': 'Short 1-3 sentence blurb shown under the sprite.',
            'sprite': 'sprite.png',
            'photo': None,
            'servings': 4,
            'prepMinutes': 15,
            'cookMinutes': 30,
            'tags': [],
            'ingredients': [{'name': 'ingredient', 'line': '1 item', 'group': None}],
            'steps': ['Step one.'],
            'tips': None,
            'notes': None,
            'source': None,
            'createdAt': today,
            'updatedAt': today,
            'madeAt': today,
        }
    (target / 'recipe.json').write_text(json.dumps(payload, indent=2) + '\n')
    print(f'Created {target}')


if __name__ == '__main__':
    main()
