from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask('app')
app.config['SECRET_KEY'] = 'AojIKNgaOSJGjhuyS'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Users(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String())
  email = db.Column(db.String())
  password = db.Column(db.String())
  created_at = db.Column(db.String())
  updated_at = db.Column(db.String())

class Contacts(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String())
  email = db.Column(db.String())
  phone = db.Column(db.String())
  image = db.Column(db.String())
  user_id = db.Column(db.String())
  created_at = db.Column(db.String())
  updated_at = db.Column(db.String())

@app.route('/')
def index():
  if 'user_id' not in session:
    return redirect('/login')
  else:
    contacts = Contacts.query.all()
    return render_template('index.html', contacts=contacts)

@app.route('/create', methods=['POST'])
def create():
  name = request.form.get('name')
  email = request.form.get('email')
  phone = request.form.get('phone')
  new_contact = Contacts (name=name, email=email, phone=phone)
  db.session.add(new_contact)
  db.session.commit()
  return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
  name = request.form.get('name')
  email = request.form.get('email')
  phone = request.form.get('phone')
  contacts = Contacts.query.filter_by(id=id).first()
  contacts.name = name
  contacts.email = email
  contacts.phone = phone
  db.session.commit()
  return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
  contacts = Contacts.query.filter_by(id=id).first()
  db.session.delete(contacts)
  db.session.commit()
  return redirect('/')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/signin', methods=['POST'])
def signin():
  email = request.form.get('email')
  password = request.form.get('password')
  user = Users.query.filter_by(email=email).first()
  if not user:
    return redirect('/login')
  if not check_password_hash(user.password, password):
    return redirect('/login')
  else:
    session['user_id'] = user.id
    return redirect('/')

@app.route('/register')
def register():
  return render_template('register.html')

@app.route('/signup', methods=['POST'])
def signup():
  name = request.form.get('name')
  email = request.form.get('email')
  password = request.form.get('password')
  user = Users.query.filter_by(email=email).first()
  if user:
    return redirect('/register')
  else:
    new_user = Users(name=name, email=email, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
  db.create_all()
  app.run(host='0.0.0.0', port=8080)