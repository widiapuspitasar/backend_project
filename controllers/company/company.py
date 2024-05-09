from flask import Blueprint, jsonify, request
from connectors.mysql_connector import engine
from models.company import Company
from sqlalchemy.orm import sessionmaker
from flask_login import login_user, logout_user
from utils.api_reponse import api_response
from sqlalchemy.exc import SQLAlchemyError
from models.validation import RegistrationRequestCompany

company_routes = Blueprint('company_routes', __name__)

@company_routes.route("/signup", methods=['POST'])
def company_do_register():
    registration_data = request.json
    registration_request = RegistrationRequestCompany(**registration_data)
    
    if not registration_request.company_name or not registration_request.employer_name or not registration_request.company_email or not registration_request.password:
        return jsonify({"message": "Incomplete data"}), 400

    company_name = registration_request.company_name
    employer_name = registration_request.employer_name
    company_email = registration_request.company_email
    password = registration_request.password

    try:
        print(f"company_name: {company_name}, employer_name: {employer_name}, company_email: {company_email}, Password Hash: {password}")
        NewCompany = Company(company_name=company_name,employer_name=employer_name, company_email=company_email )
        NewCompany.set_password(password)

        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()

        session.begin()
        session.add(NewCompany)
        session.commit()
    
        return api_response(
                status_code=201,
                message= "New user data has been successfully added",
                data={
                    "id": NewCompany.id,
                    "company_name": NewCompany.company_name,
                    "employer_name": NewCompany.employer_name,
                    "company_email": NewCompany.company_email,
                }
            )
    except Exception as e:
        print(f"Error during registration: {e}")
        session.rollback()
        return { "message": "Failed to Register" }

@company_routes.route("/login_company", methods=['POST'])
def company_do_login():
    session = None  
    try:
        data = request.json
        company_email = data.get('company_email')
        password = data.get('password')

        if not company_email or not password:
            return api_response(
                status_code=400,
                message="Email and password are required",
                data={}
            )
        
        connection = engine.connect()
        Session = sessionmaker(bind=connection)
        session = Session()

        company = session.query(Company).filter(Company.company_email == company_email).first()

        if not company:
            return api_response(
                status_code=404,
                message="Email not found",
                data={}
            )
        
        if not company.check_password(password):
            return api_response(
                status_code=401,
                message="Incorrect password",
                data={}
            )
        
        login_user(company, remember=False)

        return api_response(
            status_code=200,
            message="Login Successfully",
            data={"company": company.serialize(full=False)}
        )
    except SQLAlchemyError as e:
        if session:
            session.rollback()  
        return api_response(
            status_code=500,
            message="Database error: " + str(e),
            data={}
        )
    except Exception as e:
        return api_response(
            status_code=500,
            message="Server error: " + str(e),
            data={}
        )
    finally:
        if session:
            session.close()  

 

@company_routes.route("/logout_company", methods=['GET'])
def company_do_logout():
    logout_user()
    return("logout user succes")


    

        
