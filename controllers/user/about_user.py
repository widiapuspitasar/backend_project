from flask import Blueprint, request
from connectors.mysql_connector import engine
from models.user import User
from models.about_user import About_user
from sqlalchemy.orm import sessionmaker
from flask_login import login_required, current_user
from utils.api_reponse import api_response
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

about_user_routes = Blueprint('about_user_routes', __name__)

@login_required
@about_user_routes.route("/about_user/<int:user_id>", methods=["GET"])
def about_user(user_id):
    session = None
    try:
        connection = engine.connect()
        Session = sessionmaker(bind=connection)
        session = Session()

        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return api_response(
                status_code=404,
                message="User not found",
                data={}
            )

        user_data = {
            "name": user.name,
            "email": user.email,
        }

        about_user_data = []
        for about_user in user.about_user:
            about_user_data.append({
                "name": about_user.name,
                "role": about_user.role,
                "skills": about_user.skills,
                "phonenumber": about_user.phonenumber,
                "about_user": about_user.about_user,
                "email": about_user.email,
                "file_resume": about_user.file_resume,
            })

        return api_response(
            status_code=200,
            message="User and About User data retrieved successfully",
            data={
                "user": user_data,
                "about_user": about_user_data
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

@login_required
@about_user_routes.route("/about_user/create/<int:user_id>", methods=["POST"])
def create_about_user(user_id):
    session = None
    try:
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()

        existing_about_user = session.query(About_user).filter_by(user_id=user_id).first()
        if existing_about_user:
            return api_response(
                status_code=400,
                message="User has already created about user data",
                data={}
            )
        
        data = request.json  
        name = data.get('name') 
        role = data.get('role')
        skills = data.get('skills')
        phonenumber = data.get('phonenumber')
        email = data.get('email')
        about_user = data.get('about_user') 
        file_resume = data.get('file_resume') 

        if not all([name, role, skills, phonenumber, email, about_user, file_resume]):
            return api_response(
                status_code=400,
                message="Name, Skills, Phonenumber, Email, About User, and File Resume are required",
                data={}
            )
        
        print(f"name: {name},role: {role}, skills: {skills}, phonenumber: {phonenumber}, email: {email}, about_user: {about_user}, file_resume: {file_resume}")
        NewAboutUser = About_user(user_id=user_id, name=name,role=role, skills=skills, phonenumber=phonenumber, email=email, about_user=about_user, file_resume=file_resume)
        
        if not session.is_active:
            session.begin()
        
        session.add(NewAboutUser)
        session.commit()

        return api_response(
            status_code=201,
            message="New about user data has been successfully added",
            data={
                "id": NewAboutUser.id,
                "user_id": NewAboutUser.user_id,
                "name": NewAboutUser.name,
                "skills": NewAboutUser.skills,
                "phonenumber": NewAboutUser.phonenumber,
                "email": NewAboutUser.email,
                "about_user": NewAboutUser.about_user,
                "file_resume": NewAboutUser.file_resume
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

@login_required       
@about_user_routes.route("/about_user/edit/<int:user_id>", methods=["PUT"])
def update_about_user(user_id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    session.begin()

    try:
        update_about_user = session.query(About_user).filter(About_user.user_id == user_id).first()
        if not update_about_user:
            return {
                "message": "About user not found for the given user_id and about_user_id",
                "data": {}
            }, 404

        update_about_user.name = request.json.get('name', update_about_user.name)
        update_about_user.role = request.json.get('role', update_about_user.role)
        update_about_user.skills = request.json.get('skills', update_about_user.skills)
        update_about_user.phonenumber = request.json.get('phonenumber', update_about_user.phonenumber)
        update_about_user.about_user = request.json.get('about_user', update_about_user.about_user)
        update_about_user.email = request.json.get('email', update_about_user.email)
        update_about_user.file_resume = request.json.get('file_resume', update_about_user.file_resume)
        update_about_user.updated_at = func.now()

        session.commit()

        return {
            "message": "Profile updated successfully",
            "data": {
                "name": update_about_user.name,
                "role": update_about_user.role,
                "skills": update_about_user.skills,
                "phonenumber": update_about_user.phonenumber,
                "about_user": update_about_user.about_user,
                "email": update_about_user.email,
                "file_resume": update_about_user.file_resume,
                "updated_at": update_about_user.updated_at
            }
        }, 201

    except Exception as e:
        session.rollback()
        return {
            "message": str(e),
            "data": {}
        }, 500
    
    finally:
        session.close()
