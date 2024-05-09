from flask import Flask
import os
from controllers.user.user import user_routes
from controllers.company.company import company_routes
from controllers.company.about_company import about_company_routes
from controllers.user.about_user import about_user_routes
from controllers.job.post_job import post_job_routes
from controllers.job.apply_job import apply_job_routes
from controllers.job.favorite_job import favorite_job_routes
from controllers.job.status_job import status_job_routes
from flask_login import LoginManager
from connectors.mysql_connector import  engine
from sqlalchemy.orm import sessionmaker
from models.user import User
from models.company import Company
from flask_cors import CORS

app=Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

CORS(app, origins=['http://localhost:5173', 'career-search-project-revou-widiapuspitasars-projects.vercel.app'], supports_credentials=True)

# CORS(app)

@app.route("/")
def hello():
    return("hello uhuy")

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user_or_company(id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    user = session.query(User).get(int(id))
    if user:
        return user
    
    company = session.query(Company).get(int(id))
    if company:
        return company
    return None

app.register_blueprint(company_routes)
app.register_blueprint(about_company_routes)
app.register_blueprint(user_routes)
app.register_blueprint(about_user_routes)
app.register_blueprint(post_job_routes)
app.register_blueprint(apply_job_routes)
app.register_blueprint(favorite_job_routes)
app.register_blueprint(status_job_routes)