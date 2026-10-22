# pd.oct26brand.com: ระบบงานฝ่ายพัฒนาสินค้า OCT. 26

เว็บของฝ่าย PD ที่ทีมเปิดลองของได้และส่งความเห็นได้เลยโดยไม่ต้องล็อกอิน มีครบทุกส่วนของหน้า PD ได้แก่บอร์ดสินค้า 30 แบบ
แท็บไขว้ 3D 50 แบบ บันทึกการทดสอบ ขั้นตอน และแผน 12 เดือน ทุกสินค้าและทุกแบบ 3D มีช่องความเห็นของตัวเอง
หน้าภาพรวมมีความเห็นล่าสุดกับห้องคุยทั้งทีม

ระบบใช้ Cloudflare Pages ทำหน้าเว็บ ใช้ Pages Function `/api` ทำส่วนรับส่งข้อมูล และเก็บข้อมูลใน Cloudflare D1
ทั้งหมดอยู่ใน Cloudflare บัญชีเดียวกับ DNS ของ oct26brand.com และอยู่ในแพ็กฟรีได้

## ไฟล์
- `public/index.html` คือหน้าเว็บ ไฟล์นี้สร้างจากต้นฉบับเดียวกับหน้า PD ใน claude.ai ห้ามแก้ไฟล์นี้ตรง ๆ
  ให้แก้ที่ `../product-dev-20261021/site/` แล้วรัน `python3 product-dev-20261021/site/build.py --web`
- `public/_headers` ปิดไม่ให้ search engine เก็บหน้า และกำหนดแหล่งสคริปต์ที่อนุญาต
- `public/robots.txt` บอก search engine ไม่ให้เก็บทุกหน้า
- `functions/api/[[path]].js` คือ API ตารางในฐานข้อมูลถูกสร้างเองตอนใช้งานครั้งแรก
  - รับเฉพาะ `items` (ขั้นและบันทึกของสินค้า), `tests` (ผลทดสอบ), `comments` (ความเห็น) และ `reviews` (ติ๊กผ่าน/ไม่ผ่าน และเลขจริง ระบบไม่ยอมให้เลขจริงซ้ำหรือเปลี่ยน)
  - ตรวจทุกช่องข้อมูลที่ส่งเข้ามา
  - เขียนได้ไม่เกิน 120 ครั้งต่อ 10 นาทีต่อหนึ่ง IP
  - ลบผ่านเว็บไม่ได้ ถ้าจะลบความเห็น ให้ลบใน D1 console

## ติดตั้งครั้งเดียวใน Cloudflare (ใช้เวลาประมาณ 10 นาที)
1. Cloudflare dashboard → **Workers & Pages** → **Create** → แท็บ **Pages** → **Connect to Git**
   - เลือก GitHub repo `baysireekahnokrath/oct.26` ครั้งแรกระบบจะให้ติดตั้งแอป Cloudflare บน GitHub ก่อน
   - Production branch: `main` หลัง merge แล้ว หรือถ้าจะลองตอนนี้ให้ใช้ `claude/vibrant-pascal-16al6b`
   - Framework preset: None · Build command: ว่างไว้ · Build output directory: `public` · **Root directory: `pd-os`**
   - กด Save and Deploy
2. **Storage & Databases → D1** → **Create database** ตั้งชื่อ `oct26-pd`
3. กลับมาที่โปรเจกต์ Pages → **Settings → Bindings** → **Add → D1 database**
   - Variable name: `DB` · Database: `oct26-pd`
   - ทำทั้ง Production และ Preview
4. ไม่บังคับ แต่แนะนำ: **Settings → Variables and Secrets** → เพิ่ม Secret ชื่อ `PD_PASSCODE` เป็นรหัสทีม
   - ถ้าตั้งไว้ ใครก็เปิดดูได้ แต่จะบันทึกหรือส่งความเห็นต้องใส่รหัสก่อน ใส่ครั้งเดียวแล้วเบราว์เซอร์จะจำไว้
   - ถ้าไม่ตั้ง ใครที่มีลิงก์ก็เขียนได้
5. **Deployments** → **Retry deployment** หรือ push ใหม่ เพื่อให้ binding มีผล
6. **Custom domains** → **Set up a custom domain** → `pd.oct26brand.com` → Activate
   - DNS อยู่ที่ Cloudflare อยู่แล้ว ระบบจะเพิ่ม CNAME ให้เอง ไม่กระทบเว็บหลัก oct26brand.com
7. เปิด https://pd.oct26brand.com/api/config ถ้าเห็น `{"passcode":...}` แปลว่าฐานข้อมูลต่อแล้ว

หลังจากนี้ทุกครั้งที่ push เข้า branch ที่ตั้งไว้ Cloudflare จะ deploy ใหม่ให้เอง

## ทดสอบในเครื่อง
```
cd pd-os
cat > wrangler.toml <<'T'
name = "oct26-pd-local"
pages_build_output_dir = "public"
compatibility_date = "2024-09-23"
[[d1_databases]]
binding = "DB"
database_name = "oct26-pd"
database_id = "00000000-0000-0000-0000-000000000000"
T
npx wrangler@3 pages dev --port 8788        # http://127.0.0.1:8788 ใช้ D1 ในเครื่อง
```
อย่า commit `wrangler.toml` ไฟล์นี้ เพราะถ้ามีไฟล์นี้ Cloudflare จะใช้ค่าในไฟล์แทน binding ที่ตั้งไว้ใน dashboard
