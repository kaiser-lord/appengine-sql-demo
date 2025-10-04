from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration (use environment vars in production)
if os.environ.get('GAE_ENV') == 'standard':  # Running on App Engine
    # Use Unix socket for Cloud SQL connection (built-in for same-project App Engine)
    db_user = 'todo_user'  # Your Cloud SQL user
    db_pass = 'your_password'  # Your Cloud SQL password
    db_name = 'todo_db'  # Your database name
    cloud_sql_connection_name = 'your_project_id:region:instance_id'  # From Step 2.2
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f'mysql+pymysql://{db_user}:{db_pass}@/{db_name}'
        f'?unix_socket=/cloudsql/{cloud_sql_connection_name}'
    )
else:  # Local development
    # Use TCP for local (with proxy in Step 4)
    db_user = 'todo_user'
    db_pass = 'your_password'
    db_name = 'todo_db'
    db_host = '127.0.0.1'  # Proxy host
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f'mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}'
    )

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        desc = request.form['description']
        new_task = Task(description=desc)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if not exist (remove in production)
    app.run(debug=True)