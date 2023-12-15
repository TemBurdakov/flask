from flask import Flask, render_template, url_for, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from chat_bot import open_file, generate_questions, generate_answer
from io import BytesIO
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = {
    'messages': 'sqlite:///message.db'
}
db = SQLAlchemy(app)


class Upload(db.Model):
    __bind_key__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.Text, nullable=False)#db.Column(db.LargeBinary)
    questions = db.Column(db.Text, nullable=True)
    answer = db.Column(db.Text, nullable=True)


    def __repr__(self):
        return '<Upload %r>' % self.id

    #id = db.Column(db.Integer, primary_key=True)
    #filename = db.Column(db.String(50))


# Create index function for upload and return files
@app.route('/create-article', methods=['GET', 'POST'])
def experience():
    if request.method == 'POST':
        title = request.form['title']
        file = request.files['file']
        data = file.read().decode('utf-8')
        questions = generate_questions(data)
        print(questions)
        text_quest = data + '\n' + questions
        answer = generate_answer(text_quest)
        upload = Upload(filename=title, data=data,questions=questions, answer=answer)
        try:
            db.session.add(upload)
            db.session.commit()
            return redirect('/history')
        except:
            return "При обработке файла произошла ошибка"
    else:
        return render_template("create-article.html")


@app.route('/history')
def history():
    upload = Upload.query.order_by(Upload.id.desc()).all()
    return render_template("history.html", upload=upload)


@app.route('/history/<int:id>')
def more_history(id):
    upload = Upload.query.get(id)
    return render_template("more_history.html", upload=upload)


@app.route('/history/<int:id>/del')
def letter_delete(id):
    upload = Upload.query.get_or_404(id)

    try:
        db.session.delete(upload)
        db.session.commit()
        return redirect('/history')
    except:
        return "При удалении произошла ошибка"

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')

        except:
            return "При обработке файла произошла ошибка"
    else:
        return render_template("create-article.html")


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)


@app.route('/posts/<int:id>/del')
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении произошла ошибка"


@app.route('/posts/<int:id>/save', methods=['POST', 'GET'])
def post_save(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При сохранении произошла ошибка"


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)