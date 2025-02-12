from flask import Flask, render_template, redirect, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user

from models import db, Post, Account, login_manager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'foobar key'
login_manager.init_app(app)

db.init_app(app)
with app.app_context():
    db.create_all()



@app.route('/', methods=['POST', 'GET'])
def home():
    articles = Post.query.all()
    return render_template('home.html',  articles = articles)

@app.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    if request.method == 'POST':
        try:
            title = request.form['title']
            content = request.form['content']
            if content and title:
                print(title, content)
                data = Post(title= title, content=content)
                print('data created')
                db.session.add(data)
                db.session.commit()
                print('commited')
                return redirect(url_for('home'))
            else:
                return "Не введён заголовок или содержание"
        except Exception as err:
            print(err)
            return "ошибка при добавлении статьи"
    else:
        return render_template('create.html')


@app.route('/about')
def about():
    return render_template('about.html',)


@app.route('/signup', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        if len(request.form) == 2:
            name = request.form['name']
            password_hashed = generate_password_hash(request.form['password'])
            try:
                data = Account(name=name,password=password_hashed)
                db.session.add(data)
                db.session.commit()
            except Exception as err:
                print(err)
                return 'Ошибка при создании аккаунта'
            return redirect(url_for('sign_in'))
    return render_template('sign_up.html')

@app.route('/signin', methods=['POST','GET'])
def sign_in():
    if request.method == 'POST':
        if len(request.form) == 2:
            name = request.form['name']
            password = request.form['password']
            acc = Account.query.filter_by(name=name).first()

            if check_password_hash(acc.password, password):
                login_user(acc)
                return redirect(url_for('home'))
            return 'не удалось войти'
        else:
            print(request.form)
            redirect(url_for('home'))
    return render_template('sign_in.html')
@app.route('/logout')
def sign_out():
    logout_user()
    return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(debug=True)