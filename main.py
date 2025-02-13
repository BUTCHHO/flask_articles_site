from flask import Flask, render_template, redirect, request, url_for
from flask_login import login_user, login_required, logout_user

from models import db, login_manager, Post, Account
from secret_staff import secret_key


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = secret_key
login_manager.init_app(app)

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    articles = Post.get_all()
    return render_template('home.html',  articles = articles)

@app.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    if request.method == 'POST':
        match Post.create_article(request.form):
            case True:
                return redirect(url_for('home'))
            case False:
                return "не введен заголовок или содержимое"
            case None:
                #функция возвращает None если возник Exception
                return "ошибка при добавлении статьи"

    else:
        return render_template('create.html')


@app.route('/about')
def about():
    return render_template('about.html',)

@app.route('/signup', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        match Account.create_account(request.form):
            case True:
                return redirect(url_for('sign_in'))
            case False:
                return redirect(url_for('sign_up'))
            case None:
                #функция возвращает None если произошёл Exception
                return "ошибка при добавлении аккаунта"
    return render_template('sign_up.html')

@app.route('/signin', methods=['POST','GET'])
def sign_in():
    if request.method == 'POST':
        if (answers_dict := Account.verify_account(request.form))['verified']:
            login_user(answers_dict['user'])
            return redirect(url_for('home'))
        return 'не удалось войти'
    return render_template('sign_in.html')

@app.route('/logout')
def sign_out():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)