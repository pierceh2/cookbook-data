import argparse
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
    return Image.alpha_composite(result, shadow)


def render_sprite(script_path: Path, output_path: Path):
    canvas_obj = load_canvas(script_path)
    img = canvas_obj.img.copy().convert('RGBA')
    img = add_outline_and_shadow(img)
    validate_pixels(img)
    img = img.resize((256, 256), Image.Resampling.NEAREST)
    img.save(output_path)


def build_preview(recipe_dir: Path, source_png: Path):
    sprite = Image.open(source_png).convert('RGBA')
    checker = Image.new('RGBA', (256, 256), (248, 245, 233, 255))
    for y in range(0, 256, 16):
        for x in range(0, 256, 16):
            if (x // 16 + y // 16) % 2 == 0:
                checker.putpixel((x, y), (228, 223, 210, 255))
    panel_a = checker.copy()
    panel_a.paste(sprite, (0, 0), sprite)
    panel_b = Image.new('RGBA', (256, 256), (246, 238, 220, 255))
    panel_b.paste(sprite, (0, 0), sprite)
    side_refs = []
    for ref in sorted((ROOT / 'recipes').glob('*/sprite.png')):
        if ref.name == 'sprite.png' and ref.parent.name.startswith('sample-'):
            side_refs.append(Image.open(ref).convert('RGBA').resize((128, 128), Image.Resampling.NEAREST))
    while len(side_refs) < 3:
        side_refs.append(sprite.resize((128, 128), Image.Resampling.NEAREST))
    panel_c = Image.new('RGBA', (256, 256), (245, 235, 220, 255))
    for i, ref in enumerate(side_refs[:3]):
        panel_c.paste(ref, (12 + 80 * i, 64))
    preview = Image.new('RGBA', (768, 256), (255, 255, 255, 255))
    preview.paste(panel_a, (0, 0))
    preview.paste(panel_b, (256, 0))
    preview.paste(panel_c, (512, 0))
    preview_path = Path('/tmp') / f'{recipe_dir.name}_preview.png'
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
        build_preview(recipe_dir, out)


if __name__ == '__main__':
    main()
