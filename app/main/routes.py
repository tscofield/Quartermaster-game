from flask import session, redirect, url_for, render_template, request
from . import main
from .forms import LoginForm
from flask_login import login_user
import flask_login


class User(flask_login.UserMixin):
    pass


@main.route('/', methods=['GET', 'POST'])
def index():
    """Login form to enter a room."""
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data

        user = User()
        user.id = form.name.data
        login_user(user)
        # force session timeout set in login
        # session permaneny needs to be TRUE for the timeout to work
        session.permanent = True
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('index.html', form=form)


@main.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = session.get('room', '')
    if room is None or name is None:
        return redirect(url_for('.index'))
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room)
