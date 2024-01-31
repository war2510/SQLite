from flask import Flask, render_template, redirect
from auth import LoginForm
from flask_login import login_user
from reg import RegisterForm
from data import db_session, users
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = 'world world world hello'  # csrf-атаки


@app.route('/')
def main():
    return render_template('base.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    db_session.global_init('db/blogs.sqlite')
    form = LoginForm()
    if form.validate_on_submit():
        sessions = db_session.create_session()
        user = sessions.query(users.User).filter(users.User.email == form.email.data).first()
        # user = None
        if user and user.password == form.password.data:
            # login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template("login.html", message="Пользователь не найден")
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reg():
    db_session.global_init('db/blogs.sqlite')
    form = RegisterForm()
    if form.validate_on_submit():
        sessions = db_session.create_session()
        try: # обработка исключений
            user = users.User(
                name=form.name.data,
                email=form.email.data,
                telephone=form.telephone.data,
                password=generate_password_hash(form.password.data)
            )
            sessions.add(user)
            sessions.commit()
        except:
            return render_template('register.html', message='Такой пользователь есть!', form=form)
        return render_template('base.html', message='Вы зарегистрировались!')
    return render_template('register.html', form=form)


if __name__ == '__main__':
    db_session.global_init('db/blogs.sqlite')
    app.run()
