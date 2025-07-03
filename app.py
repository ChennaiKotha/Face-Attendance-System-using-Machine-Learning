# Main app will go here
# app.py
from flask import Flask, render_template, request, redirect, session
import cv2
import numpy as np
from model.embedder import recognize_face
from model.detector import detect_face
import datetime
import csv
import os

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/')
def home():
    if 'user' in session:
        return render_template('index.html')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin123':
            session['user'] = username
            return redirect('/')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/capture')
def capture():
    if 'user' not in session:
        return redirect('/login')

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    name = None

    if ret:
        face_img = detect_face(frame)
        if face_img is not None:
            name = recognize_face(face_img)

    cap.release()
    cv2.destroyAllWindows()

    if name:
        now = datetime.datetime.now()
        date_str = now.strftime('%Y-%m-%d')
        time_str = now.strftime('%H:%M:%S')
        with open('data/attendance.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([name, date_str, time_str])
        return f"Attendance marked for {name}"
    return "Face not recognized"

if __name__ == '__main__':
    if not os.path.exists('data/attendance.csv'):
        with open('data/attendance.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Date', 'Time'])
    app.run(debug=True)
