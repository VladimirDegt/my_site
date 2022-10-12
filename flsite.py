from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, make_response
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '91c6560cc17b86902f16614d10b2054abbb3ce6e' # ключ для шифрования данных перед тем как их сохранить в браузере клиента
# os.urandom(20).hex()
app.permanent_session_lifetime = datetime.timedelta(days=1) # время жизни сесии
menu=[{"name": "Авторизация", "url": "login"},
      {"name": "Контакт", "url": "contact"}]

@app.route("/")
def index():
    session.permanent = True # т.к. сессия живет до закрытия браузера, то так можно изменить время жизни
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1 # добавление данных сессии
    else:
        session['visits'] = 1 # запись данных в сессию
        session.modified = True # уставнавливаем изменяемость объекта сессии
    return render_template("index.html", menu=menu, title = 'Главная страница', count=session['visits'])

@app.route("/contact", methods=["POST", "GET"]) # вводим переменную, т.к. на странице происходит отправка данных
def contact():
    # проверяем какой запрос пришел через форму
    if request.method == "POST":
        # и можем взять переданные значения через переменные, указанные в input
        print(request.form)
        # мгновенные сообщение по результатам отправки формы
        if request.form["username"] != "" and request.form["email"] != "" and request.form["message"] != "":
            flash('Сообщение отправлено', category="success")
        else:
            flash('Вы не заполнили все поля', category="error")
    return render_template("contact.html", title = "Обратная связь", menu=menu)

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='Страница не найдена', menu=menu), 404

@app.route("/profile/<username>")
def profile(username):
    # запрет на доступ пользователю к другим profile
    if username not in session:
        abort(401)
    return render_template('profile.html', title = f"Страница {username}")

@app.route("/login", methods=["POST", "GET"])
def login():
    print(session)
    if request.method == "POST" and request.form['username'] not in session:
        session.setdefault(request.form['username'], request.form['password'])
        print(session)
        return redirect(url_for('profile', username=request.form['username']))
    elif request.method == "POST" and request.form['username'] in session and session[request.form['username']] == request.form['password']:
        return redirect(url_for('profile', username=request.form['username']))
    elif request.method == "POST" and request.form['username'] in session and session[request.form['username']] != request.form['password']:
        flash("Такой пользователь существует или вы ввели неверный пароль")
        return render_template('login.html', title="Авторизация", menu=menu)
    return render_template('login.html', title="Авторизация", menu=menu)
    # log = "куки еще не записаны"
    # if request.cookies.get('logged'):
    #     log = request.cookies.get('logged')
    # res = make_response(f"<h1>Форма авторизации</h1><p>logged: {log}")
    # res.set_cookie("logged", "yes", 24*3600) # время хранения куков в сек
    # return res

# # очишение куков
# @app.route("/logout")
# def logout():
#     res = make_response("<p>Куки очистились</p>")
#     res.set_cookie("logged", "", 0)
#     return res

if __name__ == "__main__":
    app.run(debug=True)