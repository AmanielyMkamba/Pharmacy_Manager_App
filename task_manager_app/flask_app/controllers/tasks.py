
from dataclasses import dataclass
from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.task import Task
from flask_app.models.user import User


# html page for adding
@app.route('/show/new')
def add_new_show():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template('new_show.html', user=User.get_one(data))
# process adding form
@app.route('/add/show', methods=['POST'])
def add_show():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'title': request.form['title'],
        'network': request.form['network'],
        'description': request.form['description'],
        'release_date': request.form['release_date'],
        "user_id": session["user_id"]
    }
    if not Task.validate_show(request.form):
        return redirect('/show/new')
    Task.create_task(data)
    return redirect ('/dashboard')

@app.route('/details/<int:id>/<int:user_id>')
def show_details(id, user_id):
    if 'user_id' not in session:
        return redirect('/logout')

    data = {
        "id":id,
        "user2":user_id
    }
    user_data ={
        'id': session['user_id']
    }

    return render_template('show_details.html', task=Task.get_one(data), user=User.get_one(user_data), user2=User.get_user_tv_show(data))


# html edit page
@app.route('/show/edit/<int:id>')
def edit_show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data ={
        'id': session['user_id']
    }

    return render_template('edit_show.html', user=User.get_one(user_data), task=Task.get_one(data))
# process edit form
@app.route('/edit/show', methods=['POST'])
def update_show():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'title': request.form['title'],
        'network': request.form['network'],
        'description': request.form['description'],
        'release_date': request.form['release_date'],
        "user_id": session["user_id"],
        'id': request.form['id']
    }
    if not Task.validate_show(request.form):
        return redirect('/dashboard')
    Task.update(data)
    return redirect ('/dashboard')

@app.route('/destroy/show/<int:id>')
def destroy(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    Task.destroy(data)
    return redirect('/dashboard')