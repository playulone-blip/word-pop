# Word Pop ศัพท์ป๊อป

เว็บแอปเล่นคำศัพท์รายวัน วันละ 10-20 คำ (แฟลชการ์ด + ควิซ + เรียงตัวอักษร) รองรับระดับ A1, A2, B1, B2, C1
ไม่มี backend ความคืบหน้าเก็บใน localStorage ของเบราว์เซอร์

## ขึ้น GitHub Pages
1. สร้าง repo ใหม่ แล้ว push ไฟล์ทั้งหมดในโฟลเดอร์นี้ขึ้นสาขา `main`
2. ไปที่ Settings > Pages แล้วเลือก Source เป็น **GitHub Actions**
3. รอ workflow "Deploy to GitHub Pages" ทำงานเสร็จ จะได้ลิงก์ `https://<user>.github.io/<repo>/`

## รันในเครื่อง
```
python3 -m http.server 8000   # แล้วเปิด http://localhost:8000
```
(เปิดไฟล์ index.html ตรงๆ ไม่ได้ เพราะแอปโหลด data/vocab.json ด้วย fetch)

## เพิ่มคำศัพท์
- แก้ไฟล์ `data/b1_words.csv`, `b2_words.csv` หรือ `c1_words.csv` (ไม่มี header, คอลัมน์: อังกฤษ,ชนิดคำ,คำแปลไทย) แล้วรัน
  ```
  pip install openpyxl
  python3 scripts/build_vocab.py
  ```
  สคริปต์จะรวมไฟล์ Excel ใน `data/source/` กับไฟล์ `*_words.csv` เป็น `data/vocab.json` และข้ามคำที่ซ้ำ
- ชนิดคำที่แสดงชื่อไทยในแอป: N, V, Adj, Adv, Pron, Prep/Conj
- ชุด **IELTS 3000** (ระดับ `LM`) มาจากไฟล์ `data/source/vocab_3000_Kru_Leela_IELTS.pdf` ซึ่งเป็นภาพสแกน จึงแปลงด้วย OCR เก็บไว้ที่ `data/lm_words.csv` อาจมีตัวอักษรไทยผิดบ้าง แก้ในไฟล์ CSV แล้วรัน build ใหม่ได้
