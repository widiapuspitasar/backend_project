from flask import Blueprint, request
from connectors.mysql_connector import engine
from models.company import Company
from models.about_company import About_company
from sqlalchemy.orm import sessionmaker
from flask_login import login_required
from utils.api_reponse import api_response
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

about_company_routes = Blueprint('about_company_routes', __name__)

@login_required
@about_company_routes.route("/about_company/<int:company_id>", methods=['GET'])
def about_company(company_id):
    session = None
    try:
        connection = engine.connect()
        Session = sessionmaker(bind=connection)
        session = Session()

        company = session.query(Company).filter(Company.id == company_id).first()
        if not company:
            return api_response(
                status_code=404,
                message="User not found",
                data={}
            )
        company_data = {
            "company_name": company.company_name,
            "company_email": company.company_email,
            "employer_name": company.employer_name,
        }

        about_ucompany_data = []
        for about_company in company.about_company:
            about_ucompany_data.append({
                "company_name": about_company.company_name,
                "company_type": about_company.company_type,
                "address": about_company.address,
                "phonenumber": about_company.phonenumber,
                "email": about_company.email,
                "about_us": about_company.about_us,
            })

        return api_response(
            status_code=200,
            message="User and About User data retrieved successfully",
            data={
                "company": company_data,
                "about_company": about_ucompany_data
            }
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

@about_company_routes.route("/about_company/create/<int:company_id>", methods=['POST'])  
def create_about_company(company_id):
    session = None  
    try:
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()

        existing_about_company = session.query(About_company).filter_by(company_id=company_id).first()
        if existing_about_company:
            return api_response(
                status_code=400,
                message="User has already created about user data",
                data={}
            )
        data = request.json  
        company_type = data.get('company_type') 
        company_name = data.get('company_name') 
        address = data.get('address')
        phonenumber = data.get('phonenumber')
        email = data.get('email')
        about_us = data.get('about_us')

        if not all([company_name, company_type, address, about_us, phonenumber, email]):
            return api_response(
                status_code=400,
                message="Company Name, Company Type, address, Phonenumber, Email, About Company are required",
                data={}
            )
        
        NewAboutCompany = About_company(company_name=company_name, company_id=company_id, company_type=company_type, address=address, phonenumber=phonenumber, about_us=about_us, email=email)
        if not session.is_active:
            session.begin()
        
        session.add(NewAboutCompany)
        session.commit()

        return api_response(
            status_code=201,
            message="New about user data has been successfully added",
            data={
                "id": NewAboutCompany.id,
                "company_id": NewAboutCompany.company_id,
                "company_name": NewAboutCompany.company_name,
                "company_type": NewAboutCompany.company_type,
                "about_us": NewAboutCompany.about_us,
                "phonenumber": NewAboutCompany.phonenumber,
                "email": NewAboutCompany.email   
            }
        )
    except SQLAlchemyError as e:
        if session:
            session.rollback()
        print("SQLAlchemy Error:", e) 
        return api_response(
            status_code=500,
            message="Database error: " + str(e),
            data={}
        )
    except Exception as e:
        print("Server Error:", e)  
        return api_response(
            status_code=500,
            message="Server error: " + str(e),
            data={}
        )
    finally:
        if session:
            session.close()


@about_company_routes.route("/about_company_list", methods=['GET'])
def get_about_company_list():
    session = None 
    try:
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()

        about_company_list = session.query(About_company).all()
        about_company_data = [company.serialize() for company in about_company_list]

        return api_response(
            status_code=200,
            message="Success",
            data=about_company_data
        )
    except SQLAlchemyError as e:
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
        session.close()

@login_required
@about_company_routes.route("/about_company/edit/<int:company_id>", methods=['PUT'])
def update_about_company(company_id):
    session = None 
    
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    session.begin()

    try:
        update_about_company = session.query(About_company).filter(About_company.company_id == company_id).first()
        if not update_about_company:
            return {
                "message": "About user not found for the given user_id and about_user_id",
                "data": {}
            }, 404

        update_about_company.company_name = request.json.get('company_name', update_about_company.company_name)
        update_about_company.company_type = request.json.get('company_type', update_about_company.company_type)
        update_about_company.address = request.json.get('address', update_about_company.address)
        update_about_company.phonenumber = request.json.get('phonenumber', update_about_company.phonenumber)
        update_about_company.about_us = request.json.get('about_us', update_about_company.about_us)
        update_about_company.email = request.json.get('email', update_about_company.email)
        update_about_company.updated_at = func.now()

        session.commit()
                
        return {
            "message": "Profile updated successfully",
            "data": {
                "company_name": update_about_company.company_name,
                "company_type": update_about_company.company_type,
                "address": update_about_company.address,
                "phonenumber": update_about_company.phonenumber,
                "about_us": update_about_company.about_us,
                "email": update_about_company.email,
                "updated_at": update_about_company.updated_at
            }
        }, 200   
    
    except Exception as e:
        session.rollback()
        return {
            "message": str(e),
            "data": {}
        }, 500
    
    finally:
        session.close()