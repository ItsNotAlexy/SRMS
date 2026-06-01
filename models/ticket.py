from database.db_manager import db
from datetime import datetime

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ticket_status = db.Column(db.Enum('Open', 'In Progress', 'Resolved', 'Closed'), default='Open', nullable=False)
    priority = db.Column(db.Enum('Low', 'Medium', 'High'), default='Low', nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def is_open(self):
        return self.ticket_status == 'Open'

    def is_resolved(self):
        return self.ticket_status in ('Resolved', 'Closed')
    
    def priority_badge_color(self):
        priority_colors = {
            'Low': 'success',
            'Medium': 'warning',
            'High': 'danger'
        }
        return priority_colors.get(self.priority, 'secondary')
    
    def status_badge_color(self):
        status_colors = {
            'Open': 'primary',
            'In Progress': 'info',
            'Resolved': 'success',
            'Closed': 'secondary'
        }
        return status_colors.get(self.ticket_status, 'secondary')
