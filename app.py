from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db=SQLAlchemy(app)

class Todo(db.Model):
    No=db.Column(db.Integer, primary_key = True)
    title=db.Column(db.String(200), nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    status=db.Column(db.String(200),nullable=False, default = "in progress")
    time=db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.No} - {self.Title}"
@app.route('/',methods=['GET','POST'])
def create_todo():
    if request.method == "POST":
        todo_title = request.form["title"]
        todo_desc = request.form["desc"]
        data=Todo(title=todo_title,desc=todo_desc)
        db.session.add(data)
        db.session.commit()
    alltodo=Todo.query.all()
    return render_template("index.html", alltodo=alltodo)
@app.route("/delete/<int:No>")
def delete_todo(No):
    todo=Todo.query.filter_by(No=No).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")
@app.route("/finished/<int:No>")
def finished_todo(No):
    todo=Todo.query.filter_by(No=No).first()
    todo.status="done"
    db.session.commit()
    return redirect("/")
if __name__ == "__main__":
   app.run()