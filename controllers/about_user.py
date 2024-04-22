from flask import Blueprint, jsonify, request, redirect
from connectors.mysql_connector import engine
from models.user import User
from models.about_user import About_user
from sqlalchemy.orm import sessionmaker
from flask_login import login_user, login_required, logout_user, current_user
from utils.api_reponse import api_response
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

about_user_routes = Blueprint('about_user_routes', __name__)

@login_required
@about_user_routes.route("/about_user", methods=["GET"])

def about_user():
    print(current_user)
    if isinstance(current_user, User):
        user_data = {
            "name": current_user.name,
            "email": current_user.email, 
        }

        about_user_data = []
        for about_user in current_user.about_user:
            about_user_data.append({
            "name": about_user.name,
            "skill": about_user.skill,
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
    else:
        return api_response(
            status_code=403,
            message="Forbidden: Only user are allowed to access this route",
            data={}
        )
    

@about_user_routes.route("/about_user/create", methods=["POST"])
@login_required
def create_about_user():
    print(current_user)
    session = None
    try:
        data = request.json  
        name = data.get('name') 
        skill = data.get('skill')
        phonenumber = data.get('phonenumber')
        email = data.get('email')
        about_user = data.get('about_user') 
        file_resume = data.get('file_resume') 

        if not name or not skill or not phonenumber or not email or not about_user or not file_resume:
            return api_response(
                status_code=400,
                message="Name, Skill, Phonenumber, Email,About Use, and File Resume are required",
                data={}
            )
        
        print(f"name: {name}, skill: {skill}, phonenumber: {phonenumber}, email: {email}, about_user: {about_user}, file_resume: {file_resume}")
        NewAboutUser = About_user(user_id=current_user.id, name=name, skill=skill, phonenumber=phonenumber, email=email, about_user=about_user, file_resume=file_resume)
        
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()

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
                "skill": NewAboutUser.skill,
                "phonenumber": NewAboutUser.phonenumber,
                "email": NewAboutUser.email,
                "about_user": NewAboutUser.about_user,
                "file_resume": NewAboutUser.file_resume
            }
        )
    
    except SQLAlchemyError as e:
        if session:
            session.rollback()
        print("SQLAlchemy Error:", e)  # Tambahkan pencatatan kesalahan di sini
        return api_response(
            status_code=500,
            message="Database error: " + str(e),
            data={}
        )
    except Exception as e:
        print("Server Error:", e)  # Tambahkan pencatatan kesalahan di sini
        return api_response(
            status_code=500,
            message="Server error: " + str(e),
            data={}
        )
    finally:
        if session:
            session.close()

        
