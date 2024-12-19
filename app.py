from flask import Flask, redirect,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"


@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title_a =request.form.get("title")
        description_a =request.form.get("description")
        todo = Todo(title=title_a, description=description_a)
        db.session.add(todo)
        db.session.commit()
    all_todo = Todo.query.all()
    return render_template("index.html", all_todo = all_todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    me = Todo.query.filter_by(sno=sno).first()
    db.session.delete(me)
    db.session.commit()
    all_todo = Todo.query.all()
    return render_template("index.html", all_todo = all_todo)

@app.route('/update')
def update():
    return render_template("index.html")
    

if __name__==("__main__"):
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port="8000")