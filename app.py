from flask import Flask, flash, render_template, request, redirect, url_for
import bcrypt, uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

class User(db.Model):
    id = db.Column(db.String, nullable=False, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=False)
    task = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        form_username = request.form['username']
        form_password = request.form['password']
        bytes_password = form_password.encode('utf-8')
        user_search = User.query.filter_by(username=form_username).first()
        if user_search != None:
            if bcrypt.checkpw(bytes_password, user_search.password):
                return redirect(url_for('home', id=user_search.id))
            else:
                flash('Password was incorrect.')
        else:
            flash('User not found.')
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        bytes_password = new_password.encode('utf-8')
        hashed_password = bcrypt.hashpw(bytes_password, bcrypt.gensalt())
        user_check = User.query.filter_by(username=new_username).first()
        u = uuid.uuid4()
        new_user = User(id=u.hex, username=new_username, password=hashed_password)
        print(u.hex)
        if user_check == None:
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue adding your account.'
        else:
            flash('Username is taken. Try again.')
    return render_template('signup.html')

@app.route('/home/<id>', methods=['POST', 'GET'])
def home(id):
    user = User.query.filter_by(id=id).first()
    tasks = Todo.query.filter_by(username=user.username).all()
    if request.method == 'POST':
        task = request.form['task']
        task_username = user.username
        new_task = Todo(task=task, username=task_username)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('home', id=user.id))
        except:
            return 'There was an issue adding your task'
    return render_template('home.html', user=user, tasks=tasks, id=id)

@app.route('/home/<id>/delete/<idt>')
def delete(id, idt):
    task_to_delete = Todo.query.get_or_404(idt)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for('home', id=id))
    except:
        return 'There was a problem deleting that task.'

@app.route('/home/<id>/update/<idt>', methods=['GET', 'POST'])
def update(id, idt):
    item = Todo.query.get_or_404(idt)
    if request.method == 'POST':
        item.task = request.form['task']
        try:
            db.session.commit()
            return redirect(url_for('home', id=id))
        except:
            return "There was an issue updating your task"
    else:
        return render_template('update.html', item=item, id=id)

if __name__ == "__main__":
    app.run(debug=True)