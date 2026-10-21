// Data layer for the claude.ai Artifact page: the artifact's shared database (capability db).
async function getDb() { return window.claude ? await window.claude.use("db") : null; }
const DB_OFFLINE = "ตอนนี้เป็นมุมมองอ่านอย่างเดียว ขั้นที่เห็นคือค่าเริ่มต้นจาก brand.py เปิดหน้านี้ใน claude.ai ขณะลงชื่อเข้าใช้ เพื่อดูบอร์ดสดและบันทึกผล";
