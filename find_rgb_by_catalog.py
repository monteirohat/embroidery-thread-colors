import re

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
                "catalog": catalog_number,
            })

    return colors


def find_by_catalog(colors, target_catalog):
    for color in colors:
        if str(color["catalog"]) == str(target_catalog):
            return color
    return None


if __name__ == "__main__":
    palette_file = "Madeira_Polyneon.gpl"  # troque se necessário
    target_catalog = "1653"

    colors = parse_gpl(palette_file)
    result = find_by_catalog(colors, target_catalog)

    if result:
        print("Match found:")
        print(f"Catalog : {result['catalog']}")
        print(f"Name    : {result['name']}")
        print(f"RGB     : ({result['r']}, {result['g']}, {result['b']})")
    else:
        print(f"Catalog {target_catalog} not found.")