import os

from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'database.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    from . import db
    db.init_app(app)

    # Register blueprints
    from . import contravenants
    app.register_blueprint(contravenants.bp)

    # Schedule jobs
    schedule_jobs(app)

    # ensure the instancs folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app

def schedule_jobs(app):
    from .jobs.import_violations import perform_import_violations
    scheduler = BackgroundScheduler()
    scheduler.add_job(perform_import_violations, 'cron', hour=0, args=[app])
    scheduler.start()
