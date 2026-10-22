"""Product numbers, owner 22 Oct: digits only, like IKEA.

Draft number  4 digits, 0001, 0002 ... one per SKU in the assortment, given once and kept in draft_numbers.json
              so a number never moves to another product when the list changes.
Real number   8 digits as 260.001.CC, given only when a SKU is ticked "ผ่าน" on the PD page (tab สินค้า).
              260001, 260002 ... run in the order SKUs pass ("26" for OCT. 26). CC are two check digits
              (ISO 7064 mod 97-10, as in IBAN), so a mistyped digit or two swapped digits never reads as another product.
              A real number is never given to another product, even if its SKU is later ticked "ไม่ผ่าน".
The page computes real numbers itself (site/review.js); this file is the same rule for scripts and the sheet.
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
DRAFT_FILE = os.path.join(HERE, "draft_numbers.json")
REAL_START = 260001

def check(seq):
    return 98 - (seq * 100) % 97

def real(seq):
    s = f"{seq:06d}"
    return f"{s[:3]}.{s[3:]}.{check(seq):02d}"

def valid(code):
    d = code.replace(".", "")
    return len(d) == 8 and d.isdigit() and int(d) % 97 == 1

def drafts(codes):
    """Draft number for each assortment code, adding new codes at the end of draft_numbers.json."""
    try: known = json.load(open(DRAFT_FILE))
    except FileNotFoundError: known = {}
    nxt = max(map(int, known.values()), default=0) + 1
    changed = False
    for c in codes:
        if c not in known:
            known[c] = f"{nxt:04d}"; nxt += 1; changed = True
    if changed:
        with open(DRAFT_FILE, "w") as f: json.dump(known, f, ensure_ascii=False, indent=1)
    return {c: known[c] for c in codes}

WAVE_ORDER = {0: 0, 1: 1, 2: 2, "C": 3}

def drafts_for(items):
    """Draft numbers for assortment items; new ones are numbered in wave order (selling now first)."""
    order = sorted(items, key=lambda a: WAVE_ORDER[a["wave"]])          # stable: list order inside a wave
    return drafts([a["code"] for a in order])

if __name__ == "__main__":
    for n in (260001, 260002, 260043): print(n, real(n), valid(real(n)))
    a = real(260012); swapped = a[:4] + a[5] + a[4] + a[6:]
    print("swap caught:", a, swapped, not valid(swapped))
    assert all(valid(real(n)) for n in range(REAL_START, REAL_START + 5000))
