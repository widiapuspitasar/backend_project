from flask import Flask
import os
from dotenv import load_dotenv
from controllers.user import user_routes
from controllers.company import company_routes
from controllers.about_company import about_company_routes
from controllers.about_user import about_user_routes
from flask_login import LoginManager
from connectors.mysql_connector import  engine
from sqlalchemy.orm import sessionmaker
from models.user import User
from models.company import Company

app=Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route("/")
def hello():
    return("hello")

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    user = session.query(User).get(int(user_id))
    if user:
        return user
    else:
        return None

@login_manager.user_loader
def load_company(company_id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    company = session.query(Company).get(int(company_id))
    if company:
        return company
    else:
        return None

    
app.register_blueprint(user_routes)
app.register_blueprint(company_routes)
app.register_blueprint(about_company_routes)
app.register_blueprint(about_user_routes)