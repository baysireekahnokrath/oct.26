"""Instagram mood set made from the real photos: the 9 scenes, their reference crops and prompts (Nano Banana Pro).

Runs 1 and 2 were made on Weave (21 Oct, 22 credits); Weave's free runs then ran out, so 3–9 are left as prompts the
owner can run in the Gemini app with the same reference photo. Output: prompts.txt (pasted into Google Doc 5).
"""
REF = "https://raw.githubusercontent.com/baysireekahnokrath/oct.26/claude/vigilant-faraday-00e92g/ig-real-20261021/ref/{}.jpg"
STYLE = ("Photorealistic editorial lifestyle photograph for an Instagram brand feed, 4:5 portrait. Soft natural morning "
         "window light from the left, warm neutral colour grade, creamy off-white linen and light oak, muted earthy palette, "
         "gentle shadows, shallow depth of field, subtle film grain. Calm, quiet, family-made Thai home mood.")
KEEP = ("The leather must look exactly like the reference photo: same flat die-cut shapes, same thin straight slits, same "
        "colours and grain, each a single flat piece of genuine cowhide about 1 mm thick, no stitching, no glue, nothing "
        "joined. No text, no logos, no watermark.")
SHOTS = [  # (date, scene, references, scene prompt, caption, done url)
    ("พ. 21 ต.ค.", "หมีหนังระยะใกล้", ["bears"],
     "Extreme close-up macro of the tan bear-head leather piece from the reference lying on cream linen, one round ear and part of the face in frame, focus on the cut edge and grain. 100mm macro.",
     "หมีตัวเล็ก ตัดจากหนังวัวแท้ทีละชิ้น\nขอบ ผิว และร่องเล็ก ๆ ทุกเส้นมาจากมือเรา",
     "https://media.weavy.ai/image/upload/v1792595901/uploads/hFlfuPGzThcX0EbDB7eexdlJsfZ2/efvurnfelst5pofsxrzq.png"),
    ("พฤ. 22 ต.ค.", "แก้วนมบนที่รองแก้วหมี", ["bears"],
     "A glass of fresh milk standing on the taupe bear-head leather piece from the reference used as a coaster, ears peeking out, on a light oak breakfast table by a window, crumbs and a folded linen napkin. 50mm.",
     "แก้วนมตอนเช้า\nกับหมีตัวเล็กที่รองอยู่ข้างใต้",
     "https://media.weavy.ai/image/upload/v1792595905/uploads/hFlfuPGzThcX0EbDB7eexdlJsfZ2/puy8tkjta990wen2h9qc.png"),
    ("ศ. 23 ต.ค.", "กาแฟบนที่รองแก้ววงกลม", ["circles"],
     "A white ceramic cup of hot black coffee on the reddish-brown circular leather piece from the reference used as a coaster, on a light oak desk next to an open notebook and pencil, gentle steam. 50mm.",
     "บ่ายที่โต๊ะทำงาน กาแฟหนึ่งแก้ว\nกับของชิ้นเล็กที่ทำให้วันช้าลงนิดหนึ่ง", ""),
    ("ส. 24 ต.ค.", "สี่เหลี่ยมหกสีวางซ้อน", ["squares"],
     "The six rounded-square leather pieces from the reference (navy, black, cream, dark grey, dark brown, tan) loosely stacked and fanned out on cream linen, low raking side light showing grain and slits. 50mm.",
     "กรมท่า ดำ ครีม เทา น้ำตาล\nเศษหนังจากงานจริง สีเลยหลากหลายแบบนี้", ""),
    ("อา. 25 ต.ค.", "มือเด็กถือหมีหนัง", ["bears"],
     "A young child's small hands (no face, cream knit sleeve) gently holding the dark grey-black bear-head leather piece from the reference above cream linen, other bears out of focus behind. 85mm.",
     "มือเล็ก ๆ ที่ช่วยกันทำทุกชิ้น\nOCT. 26 คืองานแรกที่ทั้งห้าคนในบ้านทำด้วยกัน", ""),
    ("จ. 26 ต.ค.", "ชาเย็นบนที่รองแก้วกังหัน", ["pinwheels"],
     "A short clear glass of iced Thai milk tea with light condensation standing on the tan four-lobed leather piece from the reference used as a coaster, on light oak, folded linen napkin beside it. 50mm.",
     "26 ตุลาคม วันเกิดของแม่ และวันเกิดของ OCT. 26\nชาเย็นหนึ่งแก้ว ฉลองเล็ก ๆ กันในบ้าน", ""),
    ("อ. 27 ต.ค.", "ที่รองแก้ว 4 ลายผูกเชือกปอ", ["bears", "pinwheels", "squares", "circles"],
     "Four separate leather coasters from the references, one tan bear head, one beige four-lobed piece, one cream rounded square and one brown circle, stacked loosely and tied with natural jute twine in a simple bow, on cream linen with a sprig of green leaves, top-down.",
     "สี่ทรง สี่สี ผูกเชือกปอไว้ด้วยกัน\nพร้อมส่งต่อให้ใครสักคน", ""),
    ("พ. 28 ต.ค.", "สายชาร์จพันหัวหมีในกระเป๋าผ้า", ["bears"],
     "A white USB charging cable neatly wound around the tan bear-head leather piece from the reference, plug ends tucked into its slits, resting inside an open natural canvas tote bag on a light oak bench with a paperback and keys. 50mm.",
     "สายชาร์จที่ไม่พันกันอีกแล้ว\nเรื่องเล็ก ๆ ที่ทำให้กระเป๋าเป็นระเบียบขึ้น", ""),
    ("พฤ. 29 ต.ค.", "ขอบวงกลมซ้อนกัน", ["circles"],
     "Macro side view of the six circular leather pieces from the reference stacked slightly offset on cream linen, showing the thin cut edges (about 1 mm each) and the different colours. 100mm macro.",
     "มองใกล้ ๆ จะเห็นผิวหนังจริง\nรอยย่น รูขุมขน และลายที่ไม่มีชิ้นไหนซ้ำ", ""),
]
TAGS = "#OCT26 #ourcraftedthings #หนังแท้ #งานแฮนด์เมด #leathercraft #slowliving"


def prompt(scene):
    return f"Using the reference photo of real leather pieces: {scene} {STYLE} {KEEP}"


if __name__ == "__main__":
    out = []
    for i, (d, name, refs, scene, cap, url) in enumerate(SHOTS, 1):
        out += [f"IG {i} · {d} · {name}", "สถานะ: " + ("ทำแล้ว รูปอยู่ด้านบนของเอกสาร" if url else "รอทำ"),
                "รูปต้นแบบ: " + " , ".join(REF.format(r) for r in refs)]
        if not url:
            out += ["ข้อความสั่ง AI (คัดลอกทั้งย่อหน้า):", prompt(scene)]
        out += ["แคปชัน:", cap, "", TAGS, "", "-----", ""]
    open("ig-ai-20261021/prompts.txt", "w").write("\n".join(out))
    print("wrote prompts.txt")
