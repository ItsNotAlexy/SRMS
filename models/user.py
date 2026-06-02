from database.db_manager import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(500), nullable=False)
    role = db.Column(db.Enum('user', 'technician', 'admin'), default='user', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tickets_created = db.relationship('Ticket', backref='creator', lazy=True, foreign_keys='Ticket.created_by')
    tickets_assigned = db.relationship('Ticket', backref='assignee', lazy=True, foreign_keys='Ticket.assigned_to')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_badge_color(self):
        if self.is_admin():
            return "primary"
        elif self.is_technician():
            return "warning"
        elif self.is_user():
            return "info"
        else:
            return "secondary"

    def is_admin(self):
        return self.role == 'admin'

    def is_technician(self):
        return self.role == 'technician'

    def is_user(self):
        return self.role == 'user'

    def is_staff(self):
        return self.role in ('technician', 'admin')
