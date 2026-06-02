from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from database.db_manager import db
from models.ticket import Ticket
from models.user import User

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def is_staff():
    return session.get('role') in ('technician', 'admin')


@admin_bp.route('/')
def dashboard():
    if 'user_id' not in session or not is_staff():
        return redirect(url_for('auth.login'))

    tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    total = len(tickets)
    open_count = sum(1 for t in tickets if t.ticket_status == 'Open')
    in_progress_count = sum(1 for t in tickets if t.ticket_status == 'In Progress')
    resolved_count = sum(1 for t in tickets if t.ticket_status in ('Resolved', 'Closed'))

    return render_template(
        'admin/dashboard.html',
        tickets=tickets,
        total=total,
        open_count=open_count,
        in_progress_count=in_progress_count,
        resolved_count=resolved_count,
    )


@admin_bp.route('/users', methods=['GET', 'POST'])
def users():
    if 'user_id' not in session or not is_staff():
        return redirect(url_for('auth.login'))

    if request.method == 'GET':
        registered_users = User.query.order_by(User.id).all()
        return render_template('admin/user.html', users=registered_users)

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'create':
            full_name = request.form.get('full_name')
            email = request.form.get('email')
            password = request.form.get('password', '').strip()
            role = request.form.get('role')

            if not full_name or not email or not role:
                flash('All fields are required.', 'danger')
            else:
                existing_user = User.query.filter_by(email=email).first()
                if existing_user:
                    flash('Email already registered.', 'danger')
                else:
                    new_user = User(full_name=full_name, email=email, role=role)
                    new_user.set_password(password)
                    db.add(new_user)
                    db.commit()
                    flash('User created successfully!', 'success')
        elif action == 'update':
            user_id = request.form.get('user_id')
            user = User.query.get_or_404(user_id)
            
            user.full_name = request.form.get('full_name')
            user.email = request.form.get('email')
            user.role = request.form.get('role')
            print(request.form.get('role'))
            
            db.commit()
            flash('User updated successfully!', 'success')
        elif action == 'delete':
            user_id = request.form.get('user_id')
            user = User.query.get_or_404(user_id)
            
            db.delete(user)
            db.commit()
            flash('User deleted successfully!', 'success')
        return redirect(url_for('admin.users'))


@admin_bp.route('/tickets/<int:ticket_id>', methods=['GET', 'POST'])
def ticket(ticket_id):
    if 'user_id' not in session or not is_staff():
        return redirect(url_for('auth.login'))

    ticket = Ticket.query.get_or_404(ticket_id)
    technicians = User.query.filter(User.role.in_(['technician', 'admin'])).all()

    if request.method == 'POST':
        ticket_status = request.form.get('ticket_status')
        assigned_to = request.form.get('assigned_to')

        if ticket_status:
            ticket.ticket_status = ticket_status

        ticket.assigned_to = int(assigned_to) if assigned_to else None

        db.commit()

        flash('Ticket updated successfully.', 'success')
        return redirect(url_for('admin.ticket', ticket_id=ticket.id))

    return render_template(
        'admin/ticket.html',
        ticket=ticket,
        technicians=technicians,
    )