from threading import Thread

from flask import Flask
from flask_login import LoginManager

from web import config
import time
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from web.models import db, User


def create_app():
    app = Flask(__name__)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.config['SECRET_KEY'] = '123abc'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///127.0.0.1'

    db.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main_web import main as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()

    Thread(target=handle_ads, args=(app,)).start()

    return app


def handle_ads(app):
    from .models import Log

    while True:
        with app.app_context():
            users = User.query.all()

        for user in users:
            try:
                automate_yad2_jumper(user.email, user.saved_password)
                with app.app_context():
                    db.session.add(Log(severity='info', message='successfully jumped all your posts'))
                    db.session.commit()
            except Exception as e:
                with app.app_context():
                    db.session.add(Log(severity='error', message=str(e)))
                    db.session.commit()


def automate_yad2_jumper(email, password):
    driver = Edge()

    driver.get(config.YAD2_LOGIN_URL)
    email_element = driver.find_element(by=By.ID, value='email')
    email_element.send_keys(email)

    password_element = driver.find_element(by=By.ID, value='password')
    password_element.send_keys(password)

    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    time.sleep(5)
    driver.get(config.YAD2_POSTS_URL)

    ad_jump_buttons = driver.find_elements(By.XPATH, "//button[@type='submit']")

    for jump_button in ad_jump_buttons:
        jump_button.click()

    driver.quit()
