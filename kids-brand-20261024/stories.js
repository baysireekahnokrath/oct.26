// Season 1 for the kids' brand: six episodes, one real pattern each. The kids rewrite these; this is a starting draft.
// Characters are referred to by position (0, 1, 2) so a new name, colour or shape in characters.json flows through.
const STORIES = (() => {
  const C = KIT.DATA.characters, n = i => C[i].name;
  const SEASON = [
    { ep: 1, pattern: "02", title: "เพื่อนที่ยังไม่มา", idea: `${n(0)} ${n(1)} และ${n(2)} ออกมาจากกองเศษหนัง แล้วพบว่าเพื่อนรูปกังหันเลข 02 ยังไม่มา`, lesson: "ของที่คนอื่นว่าใช้ไม่ได้ ยังเป็นอะไรได้อีกเยอะ" },
    { ep: 2, pattern: "02", title: "กังหันหมุนไม่หยุด", idea: "เจอ 02 ที่หมุนไปมาไม่ยอมหยุด ทั้งสามช่วยให้กังหันรู้จักพัก", lesson: "เหนื่อยแล้วพักได้" },
    { ep: 3, pattern: "07", title: "เพื่อนที่ชอบกอด", idea: "07 กากบาทข้อต่อวงกลม ชอบกางแขนกอดทุกคน แต่บางคนยังไม่พร้อม", lesson: "ถามเพื่อนก่อนกอด" },
    { ep: 4, pattern: "03", title: "ของขวัญวันที่ 26", idea: "วันที่ 26 ตุลาคมเป็นวันเกิดแม่ ทั้งสามแอบทำป้ายห้อยของขวัญรูป 03 เขียนชื่อแม่ด้วยลายมือตัวเอง", lesson: "ของที่ทำเองมีค่ามาก" },
    { ep: 5, pattern: "05", title: "วันขายของที่บูธ", idea: `ไปช่วยขายที่บูธ KIDS MARKET ${n(0)} นับเหรียญ ${n(1)} จัดของ ${n(2)} ไหว้ขอบคุณลูกค้า`, lesson: "ทำงานเป็นทีม ทุกคนมีหน้าที่" },
    { ep: 6, pattern: "04", title: "สีที่ซ่อนอยู่", idea: "กลับบ้าน เจอป้ายของร้านแม่ OCT. 26 พลิกดูด้านหลังเจอสีของทุกคนในบ้านซ่อนอยู่", lesson: "บ้านอยู่ข้างใน" },
  ];
  // Episode 1, four panels, drawn from the same pieces as the products.
  const at = (inner, x, y, s, rot = 0, code = "05") => {
    const p = KIT.PATTERNS[code], cx = p.w * s / 2, cy = p.h * s / 2;
    return `<g transform="translate(${x} ${y}) rotate(${rot} ${cx} ${cy}) scale(${s})">${inner}</g>`;
  };
  const ch = (i, x, y, s, r = 0) => at(KIT.character(C[i].id), x, y, s, r, C[i].pattern);
  const pc = (code, fill, x, y, s, r = 0) => at(KIT.shape(code, fill), x, y, s, r, code);
  const EP1 = [
    { art: pc("04", "#8B5E3C", 20, 70, .45, -12) + pc("05", "#C9B79C", 70, 78, .45, 8) + pc("07", "#4A4542", 118, 66, .45, 15) + pc("03", "#B07A4A", 160, 80, .4, -5) + pc("04", "#D9CDB8", 95, 40, .4, 20),
      text: "ที่โรงงาน มีเศษหนังกองใหญ่ ใคร ๆ ก็คิดว่าใช้อะไรไม่ได้แล้ว" },
    { art: pc("04", "#8B5E3C", 20, 96, .4, -12) + pc("07", "#4A4542", 150, 96, .4, 15) + ch(0, 22, 26, .62) + ch(1, 80, 18, .62, -6) + ch(2, 138, 30, .58, 5),
      text: `แต่จากกองนั้น มีสามตัวกระโดดออกมา ${n(0)} ${n(1)} และ${n(2)}` },
    { art: ch(0, 14, 40, .55) + ch(1, 66, 46, .55) + ch(2, 118, 44, .5) +
        `<g transform="translate(170 22) scale(.32)"><g fill="none" stroke="#2A2725" stroke-width="2.4" stroke-dasharray="5 5">${KIT.PATTERNS["02"].cut}</g></g><text x="184" y="70" font-family="Mali" font-size="15" fill="#2A2725" text-anchor="middle">?</text>`,
      text: `"เพื่อนอีกคนล่ะ" ${n(1)}ถาม เพื่อนรูปกังหันเลข 02 ยังไม่มา` },
    { art: `<rect x="20" y="30" width="170" height="70" rx="6" fill="#5E7A3A"/><text x="105" y="58" font-family="Jost" font-size="12" fill="#F4F0E8" text-anchor="middle" letter-spacing="2">KIDS MARKET</text>` + ch(0, 34, 66, .42) + ch(1, 84, 62, .42) + ch(2, 134, 68, .4),
      text: "ทั้งสามเลยออกตามหา และนัดเจอกันที่บูธ KIDS MARKET (ติดตามตอนต่อไป)" },
  ];
  return { SEASON, EP1 };
})();
