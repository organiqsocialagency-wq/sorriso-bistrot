"""Prepare responsive WebP files from the local image-generation manifest.

Requires Pillow. Originals are preserved at their source paths.
Run after image generation, then run build_site.py.
"""
from pathlib import Path
import json
from PIL import Image

P = Path(__file__).parent
manifest = json.loads((P / "output/imagegen/manifest.json").read_text())
destination = P / "img/generated"
destination.mkdir(parents=True, exist_ok=True)
assets = {}
prompts = []
for asset in sorted(manifest["assets"], key=lambda item: item["id"]):
    original = Path(asset["path"])
    variants = []
    widths = (480, 960, 1440) if asset["key"].startswith("home/") else (480, 960)
    with Image.open(original) as source:
        source = source.convert("RGB")
        for width in widths:
            width = min(width, source.width)
            height = round(source.height * width / source.width)
            filename = f'{asset["id"]}-{width}.webp'
            target = destination / filename
            if not target.exists() or target.stat().st_mtime < original.stat().st_mtime:
                source.resize((width, height), Image.Resampling.LANCZOS).save(
                    target, "WEBP", quality=82, method=6
                )
            variants.append({"src": "img/generated/" + filename, "width": width, "height": height})
    assets[asset["key"]] = {
        "id": asset["id"],
        "name": asset["name"],
        "illustrative": True,
        "variants": variants,
    }
    prompts.append({key: value for key, value in asset.items() if key != "path"})
(P / "image-assets.json").write_text(json.dumps(assets, ensure_ascii=False, indent=2) + "\n")
(P / "output/imagegen/prompts.json").write_text(json.dumps(
    {"tool": "built-in image_gen", "assets": prompts}, ensure_ascii=False, indent=2
) + "\n")
total = sum(file.stat().st_size for file in destination.glob("*.webp"))
print(f"Prepared {len(assets)} images, {sum(len(a['variants']) for a in assets.values())} responsive variants, {total / 1024 / 1024:.1f} MB.")
