from controller import db

class Grade(db.Model):
    __tablename__ = 'grades'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mata_kuliah = db.Column(db.String(100), nullable=False)
    sks = db.Column(db.Integer, nullable=False)
    nilai = db.Column(db.String(5), nullable=False)  # A, AB, B, BC, C, D, E
    bobot = db.Column(db.Float, nullable=False)  # 4.0, 3.5, 3.0, 2.5, 2.0, 1.0, 0.0
    semester = db.Column(db.Integer, nullable=False)
    
    @staticmethod
    def get_bobot(nilai):
        """Convert letter grade to numeric score"""
        nilai_map = {
            'A': 4.0,
            'AB': 3.5,
            'B': 3.0,
            'BC': 2.5,
            'C': 2.0,
            'D': 1.0,
            'E': 0.0
        }
        return nilai_map.get(nilai.upper(), 0.0)

    @staticmethod
    def convert_score_to_grade(score):
        """Convert 0-100 score to letter grade"""
        try:
            score = float(score)
            if score >= 85: return 'A'
            elif score >= 80: return 'AB'
            elif score >= 75: return 'B'
            elif score >= 70: return 'BC'
            elif score >= 60: return 'C'
            elif score >= 50: return 'D'
            else: return 'E'
        except (ValueError, TypeError):
            return 'E'
