from flask import Blueprint, jsonify, request, redirect, url_for
from connectors.mysql_connector import engine
from models.user import User
from models.company import Company
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
        return jsonify({
            "status": {
                "code": 403,
                "message": "Forbidden: Only authenticated users are allowed to access this route"
            },
            "data": {}
        }), 403

    

@about_user_routes.route("/about_user/create", methods=["POST"])
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
@about_user_routes.route("/about_user/<int:about_user_id>", methods=["PUT"])
def update_about_user(about_user_id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    session.begin()

    try:
        update_about_user = session.query(About_user).filter(About_user.id == about_user_id).first()

        update_about_user.name = request.json.get('name', update_about_user.name)
        update_about_user.skill = request.json.get('skill', update_about_user.skill)
        update_about_user.phonenumber = request.json.get('phonenumber', update_about_user.phonenumber)
        update_about_user.about_user = request.json.get('about_user', update_about_user.about_user)
        update_about_user.email = request.json.get('email', update_about_user.email)
        update_about_user.file_resume = request.json.get('file_resume', update_about_user.file_resume)
        update_about_user.updated_at = func.now()

        session.commit()

        return api_response(
            status_code=201,
            message="About Company data updated successfully",
            data={
                    "name": update_about_user.name,
                    "skill": update_about_user.skill,
                    "phonenumber": update_about_user.phonenumber,
                    "about_user": update_about_user.about_user,
                    "email": update_about_user.email,
                    "file_resume": update_about_user.file_resume,
                    "updated_at": update_about_user.updated_at
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
