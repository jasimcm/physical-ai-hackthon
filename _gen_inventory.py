# -*- coding: utf-8 -*-
"""Generate HARDWARE_ITEMS lines from Inventory TinkerSpace CSV (4 columns)."""
import csv
import pathlib

CSV_PATH = r"c:\Users\sebin\Downloads\Inventory TinkerSpace - Sheet1.csv"
HTML_PATH = pathlib.Path(r"g:\physical-ai-hackthon\index.html")

CMAP = {
    "Actuation": "actuation",
    "Compute": "compute",
    "Reference": "reference",
    "Sensors": "sensors",
    "Edge AI": "edge",
    "Infra": "infra",
    "Display": "display",
}


def esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", " ")


def main():
    rows_out = []
    with open(CSV_PATH, newline="", encoding="utf-8-sig") as f:
        r = csv.reader(f)
        header = next(r, None)
        for row in r:
            if len(row) < 4:
                continue
            cat, item, qty_raw, notes = row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip()
            if not item:
                continue
            ckey = CMAP.get(cat, "other")
            try:
                q_js = str(int(qty_raw))
            except ValueError:
                q_js = "'" + esc(qty_raw) + "'"
            nm, ct, nt = esc(item), esc(cat), esc(notes)
            rows_out.append(
                f"{{ name: '{nm}', category: '{ct}', cat: '{ckey}', qty: {q_js}, notes: '{nt}' }}"
            )

    items_body = ",\n".join("        " + r for r in rows_out)
    html = HTML_PATH.read_text(encoding="utf-8")
    start = html.index("      var HARDWARE_ITEMS = [")
    end = html.index("      ];", start) + len("      ];")
    new_block = "      var HARDWARE_ITEMS = [\n" + items_body + "\n      ];"
    HTML_PATH.write_text(html[:start] + new_block + html[end:], encoding="utf-8")
    print(len(rows_out), "items patched into", HTML_PATH)


if __name__ == "__main__":
    main()
