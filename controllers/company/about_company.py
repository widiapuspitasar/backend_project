from flask import Blueprint, jsonify, request, redirect
from connectors.mysql_connector import engine
from models.company import Company
from models.about_company import About_company
from sqlalchemy.orm import sessionmaker
from flask_login import login_user, login_required, logout_user, current_user
from utils.api_reponse import api_response
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

about_company_routes = Blueprint('about_company_routes', __name__)

@login_required
@about_company_routes.route("/about_company", methods=['GET'])
def about_company():
    print(current_user)
    if isinstance(current_user, Company):
       company_data = {
            "company_name": current_user.company_name,
            "employer_name": current_user.employer_name,
            "company_email": current_user.company_email, 
        }
       
       about_company_data =[]
       for about_company in current_user.about_company:
           about_company_data.append({
            "company_type": about_company.company_type,
            "address": about_company.address,
            "phonenumber": about_company.phonenumber,
            "about_us": about_company.about_us,
            "email": about_company.email,
           })
           
       return api_response(
            status_code=200,
            message="Company and About_company data retrieved successfully",
            data={
                "company": company_data,
                "about_company": about_company_data
            }
        )
    else:
        return api_response(
            status_code=403,
            message="Forbidden: Only companies are allowed to access this route",
            data={}
        )
    
@about_company_routes.route("/about_company/create", methods=['POST'])  
def create_about_company():
    session = None  
    try:
        data = request.json  
        company_type = data.get('company_type') 
        address = data.get('address')
        phonenumber = data.get('phonenumber')
        email = data.get('email')
        about_us = data.get('about_us')

        if not company_type or not address or not phonenumber or not email or not about_us:
            return api_response(
                status_code=400,
                message="Company type, Address, Phonenumber, Email, and About Us are required",
                data={}
            )
        
        print(f"company_type: {company_type}, address: {address}, phonenumber: {phonenumber}, email: {email}, about_us: {about_us}")
        NewAboutCompany = About_company(company_id=current_user.id, company_type=company_type, address=address, phonenumber=phonenumber, email=email, about_us=about_us)
        
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()

        session.begin()
        session.add(NewAboutCompany)
        session.commit()

        return api_response(
            status_code=201,
            message="New about company data has been successfully added",
            data={
                "id": NewAboutCompany.id,
                "company_id": NewAboutCompany.company_id,
                "company_type": NewAboutCompany.company_type,
                "address": NewAboutCompany.address,
                "phonenumber": NewAboutCompany.phonenumber,
                "email": NewAboutCompany.email,
                "about_us": NewAboutCompany.about_us,   
            }
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


@about_company_routes.route("/about_company_list", methods=['GET'])
def get_about_company_list():
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
@about_company_routes.route("/about_company/<int:about_company_id>", methods=['PUT'])
def update_about_company(about_company_id):
    if isinstance(current_user, Company):
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()
        session.begin()

        try: 
            update_about_company = session.query(About_company).filter(About_company.id == about_company_id).first()

            update_about_company.company_type = request.json.get('company_type', update_about_company.company_type)
            update_about_company.address = request.json.get('address', update_about_company.address)
            update_about_company.phonenumber = request.json.get('phonenumber', update_about_company.phonenumber)
            update_about_company.about_us = request.json.get('about_us', update_about_company.about_us)
            update_about_company.email = request.json.get('email', update_about_company.email)
            update_about_company.updated_at = func.now()

            session.commit()
                
            return api_response(
                status_code=201,
                message="About Company data updated successfully",
                data={
                        "company_type": update_about_company.company_type,
                        "address": update_about_company.address,
                        "phonenumber": update_about_company.phonenumber,
                        "about_us": update_about_company.about_us,
                        "email": update_about_company.email,
                        "updated_at": update_about_company.updated_at
                    }
                )    
        except Exception as e:
            session.rollback()
            return api_response(
                status_code=500,
                message=str(e),
                data={}
            )
        
        finally:
            session.close()