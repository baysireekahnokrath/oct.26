"""Apply one product-manager request to website/catalog.json.

    python3 website/manage/apply.py request.json            # check and show the changes
    python3 website/manage/apply.py request.json --write    # also write catalog.json

request.json is the request's `drafts` from the page's database, after the session has replaced every "asset:<id>"
photo with a file placed by photo.py and added that photo's description:
    {"products": {"OC-04-27": {"price": 45, "status": "out", ...}}, "shop": {"shopee": "https://...", "until": "..."},
     "alt": {"oc-04-27-2": "..."}}
Only the fields the page edits are taken (status, name, price, size, lead, uses, photos, seo; shop: shopee, fair, place,
dates, hours, until). Every rule in catalog.problems() is checked on the result; "ใช้ไม่ได้: ..." and exit 1 if any fails.
New products ("added") are not handled here; APPLY.md says how.
"""
import copy, json, os, re, sys

WEB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, WEB)
import catalog as C

FIELDS = ("status", "name", "price", "size", "lead", "uses", "photos", "seo")
SHOPF = ("shopee", "fair", "place", "dates", "hours", "until")
PATH = os.path.join(WEB, "catalog.json")


def apply(req, data):
    out, notes = copy.deepcopy(data), []
    ids = {p["id"]: p for p in out["products"]}
    for sku, ch in (req.get("products") or {}).items():
        if sku not in ids: raise SystemExit(f"ใช้ไม่ได้: ไม่มีสินค้า {sku}")
        p = ids[sku]
        for f, v in ch.items():
            if f not in FIELDS: raise SystemExit(f"ใช้ไม่ได้: แก้ช่อง {f} ไม่ได้")
            if f == "uses" and not (isinstance(v, list) and len(v) == 3 and all(isinstance(u, str) for u in v)):
                raise SystemExit(f"ใช้ไม่ได้: {p['name']} ใช้ทำอะไรได้ต้องมี 3 ข้อ")
            if f == "photos" and not (isinstance(v, list) and all(isinstance(x, str) for x in v)):
                raise SystemExit(f"ใช้ไม่ได้: {p['name']} รายการรูปผิด")
            if f == "photos" and any(x.startswith("asset:") for x in v):
                raise SystemExit(f"ใช้ไม่ได้: {p['name']} ยังมีรูปที่อัปโหลดแต่ยังไม่ได้ใส่ด้วย photo.py")
            if f in ("name", "size", "lead", "seo") and not isinstance(v, str): raise SystemExit(f"ใช้ไม่ได้: {p['name']} {f} ต้องเป็นข้อความ")
            v = v.strip() if isinstance(v, str) else [u.strip() for u in v] if f == "uses" else v
            if p[f] != v:
                notes.append(f"{p['name']} ({sku}): {f} {p[f]!r} -> {v!r}"); p[f] = v
        if "photos" in ch: p["img"] = p["photos"][0] if p["kind"] != "set" else p["img"]
    shop = out["shop"]
    for f, v in (req.get("shop") or {}).items():
        if f not in SHOPF or not isinstance(v, str): raise SystemExit(f"ใช้ไม่ได้: แก้ช่องร้าน {f} ไม่ได้")
        v = v.strip()
        if f == "until" and not re.fullmatch(r"20\d\d-\d\d-\d\d", v): raise SystemExit("ใช้ไม่ได้: วันที่ประกาศบูธผิด")
        box = shop if f == "shopee" else shop["booth"]
        if box[f] != v: notes.append(f"ร้าน: {f} {box[f]!r} -> {v!r}"); box[f] = v
    for k, v in (req.get("alt") or {}).items():
        if not isinstance(v, str) or not v.strip(): raise SystemExit(f"ใช้ไม่ได้: คำบรรยายรูป {k} ว่าง")
        if out["alt"].get(k) != v.strip(): notes.append(f"คำบรรยายรูป {k}: {v.strip()!r}"); out["alt"][k] = v.strip()
    bad = C.problems(out["products"], out["shop"], out["alt"])
    if bad: raise SystemExit("ใช้ไม่ได้: " + " · ".join(bad))
    return out, notes


if __name__ == "__main__":
    req = json.load(open(sys.argv[1]))
    data = json.load(open(PATH))
    out, notes = apply(req, data)
    print("\n".join(notes) if notes else "ไม่มีอะไรเปลี่ยน (อยู่ในไฟล์แล้ว)")
    if "--write" in sys.argv and notes:
        open(PATH, "w").write(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
        print("wrote", PATH)
