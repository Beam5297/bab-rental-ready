from flask import Flask, render_template, request, redirect, session
import sqlite3

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
        return redirect('/index')  # ✅ แก้ให้สมบูรณ์จาก /ind

    return render_template('add_receipt.html')

# สำหรับรันในเครื่อง
if __name__ == '__main__':
    app.run(debug=True)


