from database import db
from datetime import datetime


class Meal(db.Model):
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    is_in_diet = db.Column(db.Boolean, nullable=False, default=False)

    # foreignKey, ligando a refeição ao usuário
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
