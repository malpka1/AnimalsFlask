from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from celery.signals import worker_process_init
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///animals.db'
SECRET_KEY = os.urandom(24).hex()
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

db = SQLAlchemy(app)

Base = declarative_base()

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    animals = Animal.query.all()
    return render_template('index.html', animals=animals)

@app.route('/create_sync', methods=['GET', 'POST'])
def create_sync():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        new_animal = Animal(name=name, description=description)
        db.session.add(new_animal)
        db.session.commit()
        flash('Animal created successfully!')
        return redirect(url_for('index'))
    return render_template('create_sync.html')

@app.route('/create_async', methods=['GET', 'POST'])
def create_async():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        add_animal_async.apply_async(args=[name, description])
        flash('Animal creation task has been submitted!')
        return redirect(url_for('index'))
    return render_template('create_async.html')

@celery.task
def add_animal_async(name, description):
    new_animal = Animal(name=name, description=description)
    db.session.add(new_animal)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
