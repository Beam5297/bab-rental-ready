from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # ตั้งค่านี้สำหรับใช้ session

# หน้าแรก
@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    return redirect('/login')

# หน้า Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = username
            return redirect('/')
        else:
            return 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง'

    return render_template('login.html')

# ออกจากระบบ
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
