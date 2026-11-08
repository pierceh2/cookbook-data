import argparse
import json
import importlib.util
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))


def load_canvas(script_path: Path):
    spec = importlib.util.spec_from_file_location('sprite_module', script_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules['sprite_module'] = module
    spec.loader.exec_module(module)
    if not hasattr(module, 'c'):
        raise ValueError(f'{script_path} did not define a canvas object as c')
    return module.c


def read_palette():
    palette = {}
    for line in (ROOT / 'style' / 'palette.hex').read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split()
        if len(parts) >= 2:
            name, hex_value = parts[0], parts[1].lstrip('#')
            palette[name] = tuple(int(hex_value[i:i+2], 16) for i in range(0, len(hex_value), 2))
    return palette


def validate_pixels(image: Image.Image):
    palette = read_palette()
    allowed = set(tuple(v) for v in palette.values())
    for y in range(image.height):
        for x in range(image.width):
            rgba = image.getpixel((x, y))
            if rgba[3] == 0:
                continue
            if tuple(rgba[:3]) not in allowed:
                raise ValueError(f'Non-palette color used at {x},{y}: {rgba[:3]}')
            if x < 2 or y < 2 or x > image.width - 3 or y > image.height - 3:
                raise ValueError(f'Drawing exceeds canvas margin at {x},{y}')


def add_outline_and_shadow(img: Image.Image):
    width, height = img.size
    alpha = img.getchannel('A')
    outline = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    for y in range(height):
        for x in range(width):
            if alpha.getpixel((x, y)) == 0:
                continue
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]:
                xx, yy = x + dx, y + dy
                if xx < 0 or yy < 0 or xx >= width or yy >= height or alpha.getpixel((xx, yy)) == 0:
                    outline.putpixel((x, y), (26, 18, 32, 255))
                    break
    result = Image.alpha_composite(img, outline)
    shadow = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow)
    draw.ellipse((15, 46, 49, 58), fill=(44, 54, 90, 255))
    # Shadow sits under the dish, not over it.
    return Image.alpha_composite(shadow, result)


def render_sprite(script_path: Path, output_path: Path):
    canvas_obj = load_canvas(script_path)
    img = canvas_obj.img.copy().convert('RGBA')
    img = add_outline_and_shadow(img)
    validate_pixels(img)
    img = img.resize((256, 256), Image.Resampling.NEAREST)
    img.save(output_path)


def _hex(name: str):
    return read_palette()[name] + (255,)


def _neighbor_sprites(recipe_dir: Path, limit: int = 3):
    """Most recently made/created other recipes that have a sprite; real recipes before samples."""
    candidates = []
    for png in (ROOT / 'recipes').glob('*/sprite.png'):
        other = png.parent
        if other.resolve() == recipe_dir.resolve():
            continue
        stamp = ''
        try:
            data = json.loads((other / 'recipe.json').read_text())
            stamp = data.get('madeAt') or data.get('createdAt') or ''
        except Exception:
            pass
        is_sample = other.name.startswith('sample-')
        candidates.append((is_sample, _neg(stamp), other.name, png))
    candidates.sort()
    return [Image.open(c[3]).convert('RGBA') for c in candidates[:limit]]


def _neg(stamp: str):
    # Sort newest first without parsing: invert each character.
    return ''.join(chr(0x10FFFF - ord(ch)) for ch in stamp)


def build_preview(recipe_dir: Path, source_png: Path):
    """Preview strip: [parchment][dark wood][this sprite + up to 3 neighbors at half size, app navy]."""
    sprite = Image.open(source_png).convert('RGBA')
    panel_paper = Image.new('RGBA', (256, 256), _hex('paper'))
    panel_paper.alpha_composite(sprite)
    panel_wood = Image.new('RGBA', (256, 256), _hex('wood_dark'))
    panel_wood.alpha_composite(sprite)
    strip = Image.new('RGBA', (512, 256), _hex('navy'))
    smalls = [sprite] + _neighbor_sprites(recipe_dir)
    for i, img in enumerate(smalls[:4]):
        small = img.resize((128, 128), Image.Resampling.NEAREST)
        strip.alpha_composite(small, (128 * i, 64))
    preview = Image.new('RGBA', (1024, 256), (0, 0, 0, 255))
    preview.paste(panel_paper, (0, 0))
    preview.paste(panel_wood, (256, 0))
    preview.paste(strip, (512, 0))
    out_dir = ROOT / '.preview'
    out_dir.mkdir(exist_ok=True)
    preview_path = out_dir / f'{recipe_dir.name}_preview.png'
    preview.save(preview_path)
    return preview_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('recipe', type=str)
    parser.add_argument('--preview', action='store_true')
    args = parser.parse_args()

    recipe_dir = ROOT / args.recipe
    if not recipe_dir.exists():
        raise FileNotFoundError(f'Recipe directory not found: {recipe_dir}')
    sprite_script = recipe_dir / 'sprite.py'
    if not sprite_script.exists():
        raise FileNotFoundError(f'Missing sprite.py in {recipe_dir}')
    out = recipe_dir / 'sprite.png'
    render_sprite(sprite_script, out)
    if args.preview:
        print(f'Preview: {build_preview(recipe_dir, out).relative_to(ROOT)}')


if __name__ == '__main__':
    main()
