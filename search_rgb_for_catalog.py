import re
import math

def parse_gpl(filepath):
    colors = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue
            if line.startswith("GIMP Palette") or line.startswith("Name:") or line.startswith("Columns:"):
                continue

            parts = re.split(r"\s+", line)
            if len(parts) < 4:
                continue

            try:
                r = int(parts[0])
                g = int(parts[1])
                b = int(parts[2])
            except ValueError:
                continue

            catalog_number = parts[-1]
            color_name = " ".join(parts[3:-1]) if len(parts) > 4 else ""

            colors.append({
                "r": r,
                "g": g,
                "b": b,
                "name": color_name,
                "catalog": str(catalog_number),
            })

    return colors


def color_distance(c1, c2):
    return math.sqrt(
        (c1["r"] - c2["r"]) ** 2 +
        (c1["g"] - c2["g"]) ** 2 +
        (c1["b"] - c2["b"]) ** 2
    )


def nearest_catalog(colors, rgb):
    rgb_color = {"r": rgb[0], "g": rgb[1], "b": rgb[2]}
    best = None
    best_dist = None

    for color in colors:
        dist = color_distance(color, rgb_color)
        if best is None or dist < best_dist:
            best = color
            best_dist = dist

    return best, best_dist


def find_by_catalog(colors, target_catalog):
    for color in colors:
        if color["catalog"] == str(target_catalog):
            return color
    return None


def generate_candidates(base_rgb, radius=6, step=1):
    candidates = []
    br, bg, bb = base_rgb

    for dr in range(-radius, radius + 1, step):
        for dg in range(-radius, radius + 1, step):
            for db in range(-radius, radius + 1, step):
                r = min(255, max(0, br + dr))
                g = min(255, max(0, bg + dg))
                b = min(255, max(0, bb + db))
                candidates.append((r, g, b))

    return candidates


if __name__ == "__main__":
    palette_file = "Madeira_Polyneon.gpl"   # troque se necessário
    target_catalog = "1653"
    radius = 8

    colors = parse_gpl(palette_file)
    target = find_by_catalog(colors, target_catalog)

    if not target:
        print(f"Catalog {target_catalog} not found in palette.")
        raise SystemExit(1)

    base_rgb = (target["r"], target["g"], target["b"])
    print(f"Target catalog : {target_catalog}")
    print(f"Target name    : {target['name']}")
    print(f"Base RGB       : {base_rgb}")
    print()

    matches = []
    tested = generate_candidates(base_rgb, radius=radius, step=1)

    for rgb in tested:
        nearest, dist = nearest_catalog(colors, rgb)
        if nearest["catalog"] == str(target_catalog):
            distance_from_base = math.sqrt(
                (rgb[0] - base_rgb[0]) ** 2 +
                (rgb[1] - base_rgb[1]) ** 2 +
                (rgb[2] - base_rgb[2]) ** 2
            )
            matches.append({
                "rgb": rgb,
                "distance_from_base": distance_from_base,
                "nearest_name": nearest["name"],
                "nearest_catalog": nearest["catalog"],
                "palette_distance": dist,
            })

    matches.sort(key=lambda x: (x["distance_from_base"], x["palette_distance"]))

    print(f"Total RGBs mapping to catalog {target_catalog}: {len(matches)}")
    print("Best candidates:")
    for item in matches[:30]:
        print(
            f"RGB={item['rgb']} | "
            f"distance_from_base={item['distance_from_base']:.2f} | "
            f"nearest_catalog={item['nearest_catalog']} | "
            f"name={item['nearest_name']} | "
            f"palette_distance={item['palette_distance']:.2f}"
        )