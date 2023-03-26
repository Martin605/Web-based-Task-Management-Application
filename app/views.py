from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Task
from app.forms import TaskForm

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    tasks = []
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('task.html', tasks=tasks)

@bp.route('/task/create', methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data, description=form.description.data, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        flash('Task created successfully.', 'success')
        return redirect(url_for('main.index'))
    return render_template('create_task.html', form=form)

@bp.route('/task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        db.session.commit()
        flash('Task updated successfully.', 'success')
        return redirect(url_for('main.index'))
    return render_template('edit_task.html', form=form, task=task)

@bp.route('/task/<int:task_id>/complete')
@login_required
def complete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    task.complete = True
    db.session.commit()
    flash('Task marked as complete.', 'success')
    return redirect(request.referrer)

@bp.route('/task/<int:task_id>/delete')
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully.', 'success')
    return redirect(request.referrer)