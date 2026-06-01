from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from database.db_manager import db
from models.ticket import Ticket
from models.category import Category

tickets_bp = Blueprint('tickets', __name__, url_prefix='/tickets')


@tickets_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    tickets = Ticket.query.filter_by(created_by=session['user_id']).order_by(Ticket.created_at.desc()).all()
    return render_template(
        'tickets/index.html',
        tickets=tickets,
        open_count=sum(1 for ticket in tickets if ticket.ticket_status == 'Open'),
        in_progress_count=sum(1 for ticket in tickets if ticket.ticket_status == 'In Progress'),
        resolved_count=sum(1 for ticket in tickets if ticket.ticket_status == 'Resolved'),
    )


@tickets_bp.route('/create', methods=['GET', 'POST'])
def create():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    categories = Category.query.all()

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        priority = request.form.get('priority', 'Low')
        category_id = request.form.get('category_id')

        if not title or not description:
            flash('Title and description are required.', 'danger')
            return render_template('tickets/create.html', categories=categories)

        ticket = Ticket(
            title=title,
            description=description,
            priority=priority,
            category_id=category_id if category_id else None,
            created_by=session['user_id'],
            ticket_status='Open'
        )

        db.add(ticket)
        db.commit()

        flash('Ticket submitted successfully.', 'success')
        return redirect(url_for('tickets.index'))

    return render_template('tickets/create.html', categories=categories)


@tickets_bp.route('/<int:ticket_id>')
def detail(ticket_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    ticket = Ticket.query.get_or_404(ticket_id)

    if ticket.created_by != session['user_id']:
        flash('You do not have permission to view this ticket.', 'danger')
        return redirect(url_for('tickets.index'))

    return render_template('tickets/detail.html', ticket=ticket)


@tickets_bp.route('/<int:ticket_id>/edit', methods=['GET', 'POST'])
def edit(ticket_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    ticket = Ticket.query.get_or_404(ticket_id)
    categories = Category.query.all()

    if ticket.created_by != session['user_id']:
        flash('You do not have permission to edit this ticket.', 'danger')
        return redirect(url_for('tickets.index'))

    if not ticket.is_open():
        flash('Only open tickets can be edited.', 'warning')
        return redirect(url_for('tickets.detail', ticket_id=ticket.id))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        priority = request.form.get('priority')
        category_id = request.form.get('category_id')

        if not title or not description:
            flash('Title and description are required.', 'danger')
            return render_template('tickets/edit.html', ticket=ticket, categories=categories)

        ticket.title = title
        ticket.description = description
        ticket.priority = priority
        ticket.category_id = category_id if category_id else None

        db.commit()

        flash('Ticket updated successfully.', 'success')
        return redirect(url_for('tickets.detail', ticket_id=ticket.id))

    return render_template('tickets/edit.html', ticket=ticket, categories=categories)


@tickets_bp.route('/<int:ticket_id>/delete', methods=['POST'])
def delete(ticket_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    ticket = Ticket.query.get_or_404(ticket_id)

    if ticket.created_by != session['user_id']:
        flash('You do not have permission to delete this ticket.', 'danger')
        return redirect(url_for('tickets.index'))

    if not ticket.is_open():
        flash('Only open tickets can be deleted.', 'warning')
        return redirect(url_for('tickets.detail', ticket_id=ticket.id))

    db.delete(ticket)
    db.commit()

    flash('Ticket deleted successfully.', 'success')
    return redirect(url_for('tickets.index'))