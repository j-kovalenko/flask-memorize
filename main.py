from flask import Flask, render_template, request, session, redirect
from data import db_session
from data.lessons import Lesson
from sqlalchemy import func
from random import shuffle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def generate_study_session(lesson_num):
    db_sess = db_session.create_session()
    words = db_sess.query(Lesson).filter(Lesson.lesson_id == lesson_num)
    # shuffle(words)
    phrases = {}
    for word in words:
        phrases[word.finnish.lower()] = word.russian.lower()
    keys = list(phrases.keys())
    shuffle(keys)
    new_phrases = {}
    for key in keys:
        new_phrases.update({key: phrases[key]})
    return new_phrases


@app.route('/')
@app.route('/index')
def index():
    page_name = "Домашняя страница"
    db_sess = db_session.create_session()
    words = db_sess.query(Lesson).all()
    return render_template('index.html', title=page_name, words=words)


@app.route('/create', methods=["GET", "POST"])
def create():
    if request.method == 'GET':
        page_name = "Добавить слово/фразу"
        return render_template('create.html', title=page_name)
    elif request.method == 'POST':
        word = Lesson()
        word.finnish = request.form['finnish']
        word.russian = request.form['russian']
        word.lesson_id = request.form['lesson']
        db_sess = db_session.create_session()
        db_sess.add(word)
        db_sess.commit()
        return redirect('/create')


@app.route('/learn')
def learn_page():
    page_name = 'Учить слова'
    db_sess = db_session.create_session()
    words = db_sess.query(func.max(Lesson.lesson_id)).first()
    return render_template("learn_index.html", title=page_name, num=words[0])


@app.route('/learn/<lesson_num>', methods=["GET", "POST"])
def learn(lesson_num):
    words = generate_study_session(int(lesson_num))
    if request.method == "GET":
        page_name = f"Учить урок {lesson_num}"
        return render_template("learn.html", title=page_name, rus_phrases=words.values())
    else:
        results = [request.form[tup].lower() for tup in request.form]
        return render_template("results.html", ress=results, answs=list(words.keys()), rus_phrases=list(words.values()))



if __name__ == '__main__':
    db_session.global_init("db/finnish.db")
    app.run(port=8080, host='127.0.0.1')    