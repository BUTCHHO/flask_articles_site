
from flask import Flask
from models import db
from login_manage.login_manager import login_manager
from controller import post_controller, login_controller, home_controller, about_controller, account_controller
from secret_staff import secret_key

#инициализация
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = secret_key
login_manager.init_app(app)
db.init_app(app)
with app.app_context():
    db.create_all()

app.add_url_rule('/', 'home', home_controller.home_page, methods=['POST', 'GET'])
app.add_url_rule('/home/<int:post_id>', 'post_page', post_controller.post_page, methods=['GET', 'POST'])
app.add_url_rule('/about', 'about', about_controller.about_page)
app.add_url_rule('/create', 'create', post_controller.create_post_page, methods=['GET', 'POST'])
app.add_url_rule('/signup', 'sign_up', login_controller.sign_up_page, methods=['GET', 'POST'])
app.add_url_rule('/signin', 'sign_in', login_controller.sign_in_page, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'sign_out', login_controller.sign_out_page)
app.add_url_rule('/profile_<user_id>', 'profile_page', account_controller.profile_page, methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=True)