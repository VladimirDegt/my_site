from flask import Flask, render_template, url_for, request, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qwer234afawre324sdg' # ключ для шифрования данных перед тем как их сохранить в браузере клиента

menu=[{"name": "Обо мне", "url": "about_me"},
      {"name": "Контакт", "url": "contact"}]

@app.route("/")
def index():
    return render_template("index.html", menu=menu, title = 'Главная страница')

@app.route("/contact", methods=["POST", "GET"]) # вводим переменную, т.к. на странице происходит отправка данных
def contact():
    # проверяем какой запрос пришел через форму
    if request.method == "POST":
        # и можем взять переданные значения через переменные, указанные в input
        print(request.form)
        # мгновенные сообщение по результатам отправки формы
        if len(request.form["username"]) > 1:
            flash('Сообщение отправлено')
        else:
            flash('Вы не указали имя')

    return render_template("contact.html", title = "Обратная связь", menu=menu)

if __name__ == "__main__":
    app.run(debug=True)