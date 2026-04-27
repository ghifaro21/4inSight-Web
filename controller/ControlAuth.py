from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, redirect, url_for, flash
from flask_login import login_user, logout_user
from model.ModulUser import User
from controller import db

def signup_post():
    if request.method == 'POST':
        nim = request.form.get('nim')
        nama = request.form.get('nama')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate password confirmation
        if password != confirm_password:
            flash("Password dan konfirmasi password tidak sama!", "error")
            return redirect(url_for('signup'))
        
        # Check if NIM already exists
        user = User.query.filter_by(nim=nim).first()
        if user:
            flash("NIM sudah terdaftar, silakan gunakan NIM lain!", "error")
            return redirect(url_for('signup'))
        
        # Check if email already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email sudah terdaftar, silakan gunakan email lain!", "error")
            return redirect(url_for('signup'))

        # Create new user with hashed password
        new_user = User(
            nim=nim,
            nama=nama,
            email=email,
            password=generate_password_hash(password, method='pbkdf2:sha256')
        )

        # Save to database
        db.session.add(new_user)
        db.session.commit()

        flash("Pendaftaran berhasil! Silakan login.", "success")
        return redirect(url_for('login'))

def login_post():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Find user by email
        user = User.query.filter_by(email=email).first()

        if user is None:
            flash("Email tidak ditemukan.", "error")
            return redirect(url_for('login'))
        
        # Verify password
        if check_password_hash(user.password, password):
            login_user(user)
            flash("Login berhasil! Selamat datang di 4in Sight.", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Password salah. Silakan coba lagi.", "error")
            return redirect(url_for('login'))

def logout():
    logout_user()
    flash("Anda berhasil logout.", "info")
    return redirect(url_for('login'))
