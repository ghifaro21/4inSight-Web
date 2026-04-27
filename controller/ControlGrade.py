from model.ModulGrade import Grade
from model.ModulUser import User
from controller import db
from flask import request, redirect, url_for, flash
from flask_login import current_user

def get_all_grades():
    """Get all grades for current user"""
    return Grade.query.filter_by(user_id=current_user.id).order_by(Grade.semester).all()

def get_grades_by_semester(semester):
    """Get grades for a specific semester"""
    return Grade.query.filter_by(user_id=current_user.id, semester=semester).all()

def add_grade():
    """Add a new grade"""
    mata_kuliah = request.form['mata_kuliah']
    sks = int(request.form['sks'])
    score = request.form['nilai'] # receiving numerical score 0-100
    semester = int(request.form['semester'])
    
    nilai = Grade.convert_score_to_grade(score)
    bobot = Grade.get_bobot(nilai)
    
    grade = Grade(
        user_id=current_user.id,
        mata_kuliah=mata_kuliah,
        sks=sks,
        nilai=nilai,
        bobot=bobot,
        semester=semester
    )
    
    db.session.add(grade)
    db.session.commit()
    
    flash("Nilai berhasil ditambahkan!", "success")
    return redirect(url_for('halaman_grade'))

def delete_grade(grade_id):
    """Delete a grade"""
    grade = Grade.query.get(grade_id)
    
    if not grade:
        flash("Data nilai tidak ditemukan!", "error")
        return redirect(url_for('halaman_grade'))
    
    if grade.user_id != current_user.id:
        flash("Anda tidak memiliki akses untuk menghapus data ini!", "error")
        return redirect(url_for('halaman_grade'))
    
    db.session.delete(grade)
    db.session.commit()
    
    flash("Nilai berhasil dihapus!", "success")
    return redirect(url_for('halaman_grade'))

def get_grade_by_id(grade_id):
    """Get a single grade by ID"""
    return Grade.query.get(grade_id)

def edit_grade(grade_id):
    """Edit an existing grade"""
    grade = Grade.query.get(grade_id)
    
    if not grade:
        flash("Data nilai tidak ditemukan!", "error")
        return redirect(url_for('halaman_grade'))
    
    if grade.user_id != current_user.id:
        flash("Anda tidak memiliki akses untuk mengubah data ini!", "error")
        return redirect(url_for('halaman_grade'))
    
    grade.mata_kuliah = request.form['mata_kuliah']
    grade.sks = int(request.form['sks'])
    score = request.form['nilai']
    grade.nilai = Grade.convert_score_to_grade(score)
    grade.bobot = Grade.get_bobot(grade.nilai)
    grade.semester = int(request.form['semester'])
    
    db.session.commit()
    
    flash("Nilai berhasil diperbarui!", "success")
    return redirect(url_for('halaman_grade'))

def calculate_ipk():
    """Calculate IPK (cumulative GPA)"""
    grades = Grade.query.filter_by(user_id=current_user.id).all()
    
    if not grades:
        return 0.0, 0
    
    total_sks = sum(g.sks for g in grades)
    total_points = sum(g.sks * g.bobot for g in grades)
    
    if total_sks == 0:
        return 0.0, 0
    
    ipk = total_points / total_sks
    return round(ipk, 2), total_sks

def calculate_ips(semester):
    """Calculate IPS (semester GPA) for a specific semester"""
    grades = Grade.query.filter_by(user_id=current_user.id, semester=semester).all()
    
    if not grades:
        return 0.0, 0
    
    total_sks = sum(g.sks for g in grades)
    total_points = sum(g.sks * g.bobot for g in grades)
    
    if total_sks == 0:
        return 0.0, 0
    
    ips = total_points / total_sks
    return round(ips, 2), total_sks

def get_semester_summary():
    """Get summary of all semesters"""
    grades = Grade.query.filter_by(user_id=current_user.id).all()
    
    if not grades:
        return []
    
    semesters = set(g.semester for g in grades)
    summary = []
    
    for sem in sorted(semesters):
        ips, total_sks = calculate_ips(sem)
        sem_grades = [g for g in grades if g.semester == sem]
        summary.append({
            'semester': sem,
            'ips': ips,
            'total_sks': total_sks,
            'total_mk': len(sem_grades)
        })
    
    return summary

def get_grade_distribution():
    """Get distribution of letter grades"""
    grades = Grade.query.filter_by(user_id=current_user.id).all()
    
    dist = {
        'A': 0,
        'AB': 0,
        'B': 0,
        'BC': 0,
        'C': 0,
        'D': 0,
        'E': 0
    }
    
    for g in grades:
        if g.nilai.upper() in dist:
            dist[g.nilai.upper()] += 1
            
    return dist
