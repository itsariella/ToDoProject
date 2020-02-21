from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' ##where the database is located, relative path
db = SQLAlchemy(app) ##initialize database with settings from app

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False) ##holds each task, 200 characters, task cannot be null
    date_created = db.Column(db.DateTime, default = datetime.utcnow) ##date set automatically 

    def __repr__(self):
        return '<Task %r>' % self.id ##returns id of task created

    ##run python, from app import db, db.create_all to create new database



@app.route('/', methods=['POST', 'GET']) ##can send data to database
def index():
    if request.method == 'POST':
        task_content = request.form['content'] ##pass input 'content'
        new_task = Todo(content=task_content)

        try: ##push to database
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error when adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all() ##querying database and order by date created
        return render_template('index.html',tasks = tasks) ##pass into template

if __name__ == "__main__":
    app.run(debug=True)

