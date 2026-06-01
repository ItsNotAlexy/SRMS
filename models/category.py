from database.db_manager import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    tickets = db.relationship('Ticket', backref='category', lazy=True)
