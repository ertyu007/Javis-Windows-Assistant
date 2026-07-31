# Windows Assistant

- คำสั่ง “เปิด <ชื่อโปรแกรม>” ใช้ `program.open`
- คำสั่ง “ปิด/ย่อ/ขยาย/สลับหน้าต่าง” ใช้ `window`
- คำสั่ง “พิมพ์ข้อความ” ใช้ `input.write`
- คำสั่ง “กด Ctrl+S” ใช้ `input.hotkey` และ target `ctrl+s`
- shutdown, restart และ sleep ต้องขอการยืนยัน
- ห้ามส่ง shell command หรือ PowerShell เป็น target
