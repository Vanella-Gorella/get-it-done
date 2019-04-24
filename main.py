from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True

#type//name/username/localhostport/database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:localhost@localhost:3306/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True

#creates new database object
db = SQLAlchemy(app)

#extends the sqlalchemy class, creates new model
class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean, default = False)
    def __init__(self, name):
        self.name = name
        self.completed = False



@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        task_name = request.form['task']
        new_task = Task(task_name)
        db.session.add(new_task)
        db.session.commit()
        

    tasks = Task.query.filter_by(completed=False).all()
    completed_tasks = Task.query.filter_by(completed=True).all()
    return render_template('todos.html', title="Get It Done!",
     tasks=tasks, completed_tasks = completed_tasks)

@app.route('/delete-task', methods=['POST'])
def delete_task():
    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect('/')



if __name__ == '__main__':
    app.run()
