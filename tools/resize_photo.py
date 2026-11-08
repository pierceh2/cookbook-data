import argparse
from pathlib import Path

from PIL import Image, ImageOps


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('recipe_dir')
    args = parser.parse_args()

    src = Path(args.input)
    if not src.exists():
        raise FileNotFoundError(src)

    dst_dir = Path(args.recipe_dir)
    dst_dir.mkdir(parents=True, exist_ok=True)

    image = Image.open(src)
    image = ImageOps.exif_transpose(image)
    max_dim = 1600
    long_edge = max(image.size)
    if long_edge > max_dim:
        scale = max_dim / long_edge
        new_size = (max(1, int(image.width * scale)), max(1, int(image.height * scale)))
        image = image.resize(new_size, Image.Resampling.LANCZOS)
    image.convert('RGB').save(dst_dir / 'photo.jpg', 'JPEG', quality=85, optimize=True)


if __name__ == '__main__':
    main()
