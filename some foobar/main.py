
from flask import Flask, render_template, redirect, request, url_for, abort
from flask_login import login_user, login_required, logout_user, current_user
from models import db, Post, Account, Comment
from login_manage.login_manager import login_manager
from secret_staff import secret_key

#инициализация
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = secret_key
login_manager.init_app(app)
db.init_app(app)
with app.app_context():
    db.create_all()



#обработка маршрутов
@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        if current_user.is_authenticated:
            if 'liked_post_id' in request.form:
                Post.like_post(request.form, current_user) #в функции уже реализовано удаление лайка

            #удаление аккаунта не реализовано на фронтенде
            # elif request.form['delete_acc']:
            #     Account.query.filter_by(id=current_user.id).delete()
            #     db.session.delete(current_user)
            #     db.session.commit()
    posts = Post.get_all()
    return render_template('home.html',  posts = posts)



@app.route('/home/<post_id>', methods=['POST', 'GET'])
def post_page(post_id):
    target_post = Post.query.filter_by(id=int(post_id)).first()
    if target_post == None:
        abort(404)
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        print(request.form)
        if current_user.is_authenticated:
            if form_type == 'like_post':
                Post.like_post(request.form, current_user)
            elif form_type == 'write_comment':
                Comment.create_commentary(request.form,current_user,target_post)
            elif form_type == 'like_comment':
                Comment.like_comment(request.form, current_user)
    return render_template('post_extended.html', post=target_post)



@app.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    if request.method == 'POST':
        match Post.create_post(request.form, current_user):
            case True:
                return redirect(url_for('home'))
            case False:
                return "не введен заголовок или содержимое"
            case _: #если вернул Exception
                return 'ошибка при добавлении статьи'
    else:
        return render_template('create.html')



@app.route('/about')
def about():
    return render_template('about.html',)



@app.route('/profile/<username>')
def profile_page(username):
    if current_user.is_authenticated:
        return 'this page is in development. You successfully entered this page'
    return 'this page is in development and ypu have to authorize before opening it'



@app.route('/signup', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        match Account.create_account(request.form):
            case True:
                return redirect(url_for('sign_in'))
            case False:
                return redirect(url_for('sign_up'))
            case _: #если вернул Exception
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