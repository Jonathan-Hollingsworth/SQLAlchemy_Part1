"""Blogly application."""

from flask import Flask, redirect, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'Alchemist'

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
    """This will simply redirect to the users page at the moment"""

    return redirect('/users')

@app.route('/users')
def list_users():
    """Lists all users that currently exist and displays them"""

    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/<int:user_id>')
def show_user_data(user_id):
    """Displays all information of the desired user"""

    user = User.query.get_or_404(user_id)
    return render_template('user.html', user=user)

@app.route('/users/new')
def display_user_form():
    """Renders the template for the 'new user' form"""

    return render_template('create.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    """Creates a new user using the submitted data"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form.get('image_url', None)

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/edit')
def display_edit_form(user_id):
    """Renders the template for the 'edit user' form"""

    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Processes the received data and edits the appropriate user accordingly"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User.query.get_or_404(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Deletes the appropriate user"""

    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect('/users')