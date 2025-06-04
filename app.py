from flask import Flask, render_template, request, redirect, session, send_file
import sqlite3
import io
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# สร้างตารางใน SQLite ถ้ายังไม่มี
def init_db():
    conn = sqlite3.connect('rent_receipts.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS receipts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tenant_name TEXT,
            room_number TEXT,
            amount REAL,
            due_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

# เรียกใช้เมื่อเริ่มแอป
init_db()

@app.route('/')
def index():
    return 'ระบบห้องเช่า BAB พร้อมใช้งานแล้ว!'

@app.route('/add_receipt', methods=['GET', 'POST'])
def add_receipt():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect('/login')
    
    if request.method == 'POST':
        tenant_name = request.form['tenant_name']
        room_number = request.form['room_number']
        amount = float(request.form['amount'])
        due_date = request.form['due_date']

        conn = sqlite3.connect('rent_receipts.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO receipts (tenant_name, room_number, amount, due_date)
            VALUES (?, ?, ?, ?)
        ''', (tenant_name, room_number, amount, due_date))
        conn.commit()
        conn.close()
        return redirect('/')

    return render_template('add_receipt.html')

@app.route('/my_receipts')
def my_receipts():
    if 'username' not in session:
        return redirect('/login')
    
    username = session['username']
    conn = sqlite3.connect('rent_receipts.db')
    c = conn.cursor()
    c.execute("SELECT * FROM receipts WHERE tenant_name=?", (username,))
    receipts = c.fetchall()
    conn.close()

    return render_template('my_receipts.html', receipts=receipts)

@app.route('/download_receipt/<int:receipt_id>')
def download_receipt(receipt_id):
    if 'username' not in session:
        return redirect('/login')

    conn = sqlite3.connect('rent_receipts.db')
    c = conn.cursor()
    c.execute("SELECT * FROM receipts WHERE id=?", (receipt_id,))
    receipt = c.fetchone()
    conn.close()

    if not receipt:
        return "ไม่พบใบเสร็จ", 404

    # สร้าง PDF ในหน่วยความจำ
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica", 14)
    p.drawString(100, 800, f"ใบเสร็จค่าเช่าห้อง")
    p.drawString(100, 780, f"ผู้เช่า: {receipt[1]}")
    p.drawString(100, 760, f"ห้อง: {receipt[2]}")
    p.drawString(100, 740, f"จำนวนเงิน: {receipt[3]} บาท")
    p.drawString(100, 720, f"ครบกำหนดชำระ: {receipt[4]}")
    p.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="receipt.pdf", mimetype='application/pdf')

# ✅ ต้องอยู่ล่างสุดเท่านั้น!
if __name__ == '__main__':
    app.run(debug=True)
