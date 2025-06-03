import sqlite3

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
        return redirect('/index')  # หรือ redirect ไปหน้าแสดงใบเสร็จ
    
    return render_template('add_receipt.html')

