"""Apply the owner's Web Builder edits to the brand data, then rebuild the posters and the website.

The Web Builder page (builder/index.html, published as a claude.ai Artifact) keeps the owner's drafts in its
database. Claude exports them to a JSON file and runs:

    python3 website/builder/apply.py drafts.json            # show what would change
    python3 website/builder/apply.py drafts.json --write    # patch brand.py + website/build.py, rebuild everything

drafts.json: {"products": {"01": {"name", "price", "hook", "size", "hide", "sold"}, ...}, "booth": {"until": "YYYY-MM-DD"}}
Any key may be left out; a product that is not listed stays as it is.

name, price, hook and size are literals in brand.py's P table (one source of truth: the booth plan, posters and site
all read them), hide and sold are the HIDE and SOLD sets in website/build.py, the booth notice date is BOOTH["until"].
The literals are found with ast and replaced in place, so comments and layout in brand.py stay as they are.
The drafts are written by people on the page, so every value is checked and quoted here, never run.
"""
import ast, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.dirname(HERE)
REPO = os.path.dirname(WEB)
BRAND_DIR = os.path.join(REPO, "brand-20261014")
BRAND_PY = os.path.join(BRAND_DIR, "brand.py")
SITE_PY = os.path.join(WEB, "build.py")
LIVE = os.path.join(HERE, "live.json")

FIELDS = {"name": 1, "size": 5, "hook": 7, "price": 10}     # index in a P row
LIMITS = {"name": 60, "size": 60, "hook": 160}
POSTER_FIELDS = ("name", "hook", "price")                   # what the how-to posters print


def text(v, key):
    if not isinstance(v, str):
        raise ValueError(f"{key}: ต้องเป็นข้อความ")
    v = re.sub(r"\s+", " ", re.sub(r"[\x00-\x1f\x7f]", " ", v)).strip()
    v = v.replace("<", "").replace(">", "")      # the posters print these texts as HTML
    if not v:
        raise ValueError(f"{key}: ว่างไม่ได้")
    if len(v) > LIMITS[key]:
        raise ValueError(f"{key}: ยาวเกิน {LIMITS[key]} ตัวอักษร")
    return v


def price(v):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or v != int(v) or not 1 <= v <= 99999:
        raise ValueError("price: ต้องเป็นจำนวนเต็ม 1–99999 บาท")
    return int(v)


def py_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def spans(src):
    """Byte spans of every editable literal: {(n, field): (start, end, value)}, plus BOOTH until and the two sets."""
    b = src.encode()
    starts = [0]
    for line in b.split(b"\n"):
        starts.append(starts[-1] + len(line) + 1)
    at = lambda node: (starts[node.lineno - 1] + node.col_offset, starts[node.end_lineno - 1] + node.end_col_offset)
    out = {}
    for node in ast.parse(src).body:
        if not isinstance(node, ast.Assign) or not isinstance(node.targets[0], ast.Name):
            continue
        name = node.targets[0].id
        if name == "P":
            for row in node.value.elts:
                n = row.elts[0].value
                for f, i in FIELDS.items():
                    out[(n, f)] = (*at(row.elts[i]), row.elts[i].value)
        elif name == "BOOTH":
            for kw in node.value.keywords:
                if kw.arg == "until":
                    out["until"] = (*at(kw.value), kw.value.value)
        elif name in ("HIDE", "SOLD"):
            v = node.value
            nums = set() if isinstance(v, ast.Call) else {e.value for e in v.elts}
            out[name] = (*at(v), nums)
    return out


def patch(path, edits):
    """edits: [(start, end, new_text)] in bytes of the file as it is now."""
    b = open(path, "rb").read()
    for s, e, new in sorted(edits, reverse=True):
        b = b[:s] + new.encode() + b[e:]
    compile(b, path, "exec")
    open(path, "wb").write(b)


def set_lit(nums):
    return "{" + ", ".join(str(n) for n in sorted(nums)) + "}" if nums else "set()"


def live():
    """What the site shows now, read from the files: the Web Builder page's baseline."""
    bs, ss = spans(open(BRAND_PY).read()), spans(open(SITE_PY).read())
    ns = sorted({k[0] for k in bs if isinstance(k, tuple)})
    return {"products": {f"{n:02d}": {**{f: bs[(n, f)][2] for f in FIELDS}, "hide": n in ss["HIDE"][2], "sold": n in ss["SOLD"][2]}
                         for n in ns},
            "booth": {"until": bs["until"][2]}}


def plan(drafts):
    """Check the drafts against the files. Returns (brand edits, site edits, changes, poster numbers)."""
    bs, ss = spans(open(BRAND_PY).read()), spans(open(SITE_PY).read())
    b_edits, changes, posters = [], [], set()
    hide, sold = set(ss["HIDE"][2]), set(ss["SOLD"][2])
    for key, d in (drafts.get("products") or {}).items():
        if not re.fullmatch(r"\d{1,2}", str(key)) or (int(key), "name") not in bs or not isinstance(d, dict):
            raise ValueError(f"ไม่มีสินค้า #{key}")
        n = int(key)
        for f in FIELDS:
            if f not in d:
                continue
            new = price(d[f]) if f == "price" else text(d[f], f)
            s, e, old = bs[(n, f)]
            if new != old:
                b_edits.append((s, e, str(new) if f == "price" else py_str(new)))
                changes.append(f"#{n:02d} {f}: {old} → {new}")
                if f in POSTER_FIELDS:
                    posters.add(n)
        for f, st in (("hide", hide), ("sold", sold)):
            if f in d:
                if not isinstance(d[f], bool):
                    raise ValueError(f"#{n:02d} {f}: ต้องเป็นจริงหรือไม่จริง")
                if d[f] != (n in st):
                    (st.add if d[f] else st.discard)(n)
                    changes.append(f"#{n:02d} {f}: {not d[f]} → {d[f]}")
    until = (drafts.get("booth") or {}).get("until")
    if until is not None:
        if not isinstance(until, str) or not re.fullmatch(r"20\d\d-\d\d-\d\d", until):
            raise ValueError("booth.until: ต้องเป็นวันที่ YYYY-MM-DD")
        s, e, old = bs["until"]
        if until != old:
            b_edits.append((s, e, py_str(until)))
            changes.append(f"booth until: {old} → {until}")
    s_edits = [(ss[k][0], ss[k][1], set_lit(v)) for k, v in (("HIDE", hide), ("SOLD", sold)) if v != ss[k][2]]
    return b_edits, s_edits, changes, posters


def run(*cmd, cwd=REPO):
    print("$", " ".join(cmd)); subprocess.run(cmd, cwd=cwd, check=True)


def rebuild(posters):
    """Posters for the products whose printed text changed, their thumbnails, then the whole website."""
    run(sys.executable, os.path.join(BRAND_DIR, "posters", "build.py"))
    if posters:
        jobs = json.load(open(os.path.join(BRAND_DIR, "posters", "jobs.json")))
        jobs = [j for j in jobs if int(os.path.basename(j["src"])[:2]) in posters]
        tmp = os.path.join(HERE, ".jobs.json")
        json.dump(jobs, open(tmp, "w"))
        try:
            run("node", os.path.join(BRAND_DIR, "tools", "render.mjs"), tmp)
        finally:
            os.remove(tmp)
        from PIL import Image
        for n in posters:
            im = Image.open(os.path.join(BRAND_DIR, "posters", "png", f"{n:02d}-post.png")).convert("RGB")
            im.resize((360, 450), Image.LANCZOS).save(os.path.join(BRAND_DIR, "posters", "thumb", f"{n:02d}.jpg"), quality=86)
    run(sys.executable, os.path.join(WEB, "build.py"))
    run(sys.executable, os.path.join(HERE, "build.py"))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        json.dump(live(), open(LIVE, "w"), ensure_ascii=False, indent=1); print("wrote", LIVE); sys.exit()
    drafts = json.load(open(args[0]))
    try:
        b_edits, s_edits, changes, posters = plan(drafts)
    except ValueError as e:
        sys.exit(f"ใช้ไม่ได้: {e}")
    print("\n".join(changes) or "ไม่มีอะไรเปลี่ยน")
    if "--write" in sys.argv and changes:
        if b_edits:
            patch(BRAND_PY, b_edits)
        if s_edits:
            patch(SITE_PY, s_edits)
        rebuild(posters)
        print("posters re-rendered:", ", ".join(f"{n:02d}" for n in sorted(posters)) or "none")
