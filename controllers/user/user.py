from flask import Blueprint, jsonify, request, Flask
from connectors.mysql_connector import engine
from models.user import User
from sqlalchemy.orm import sessionmaker
from flask_login import login_user, login_required, logout_user, current_user
from utils.api_reponse import api_response
from sqlalchemy.exc import SQLAlchemyError
from models.validation import RegistrationRequest


user_routes = Blueprint('user_routes',__name__)


@user_routes.route("/register", methods=['GET'])
def user_register():
     return('register user')


@user_routes.route("/login", methods=['GET'])
@login_required
def user_login():
    response_data = dict()
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    try:
        user_query = session.query(User)


        if request.args.get('query') != None:
            search_query = request.args.get('query')
            user_query = user_query.filter(User.name.like(f'%{search_query}%'))

        users = user_query.all()
        response_data['user'] = [user.serialize(full=False) for user in users]


        return jsonify(response_data)

    except Exception as e:
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )
    finally:
        session.close()

@user_routes.route("/register", methods=['POST'])
def do_registration():
    registration_data = request.json
    registration_request = RegistrationRequest(**registration_data)

    if not registration_request.name or not registration_request.email or not registration_request.password:
        return jsonify({"message": "Incomplete data"}), 400
    
    name = registration_request.name
    email = registration_request.email
    password = registration_request.password

    try:
        NewUser = User(name=name, email=email)
        NewUser.set_password(password)

        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()

        session.begin()
        session.add(NewUser)
        session.commit()

        return jsonify({
            "message": "New user data has been successfully added",
            "data": {
                "id": NewUser.id,
                "name": NewUser.name,
                "email": NewUser.email
            }
        }), 200
    
    except Exception as e:
        print(f"Error during registration: {e}")
        return jsonify({"message": "Failed to register"}), 500


@user_routes.route("/login_user", methods=['POST'])
def do_user_login():
    session = None
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        connection = engine.connect()
        Session = sessionmaker(bind=connection)
        session = Session()

        user = session.query(User).filter(User.email == email).first()

        if not email or not password:
            return api_response(
                status_code=400,
                message="Email and password are required",
                data={}
            )

        if not user or not user.check_password(password):
            return api_response(
                status_code=401,
                message="Invalid email or password",
                data={}
            )

        login_user(user, remember=False)
        print(current_user)
        print(current_user.is_authenticated)

        return api_response(
            status_code=200,
            message="Login Successfully",
            data={"user": user.serialize(full=False)}
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

@user_routes.route("/get_current_user", methods=['GET'])
@login_required
def get_current_user():
    print(current_user)
    if current_user.is_authenticated:
        return api_response(
            status_code=200,
            message="User data retrieved successfully",
            data={"user": current_user.serialize(full=False)}
        )
    else:
        return api_response(
            status_code=401,
            message="User not authenticated",
            data={}
        )



@user_routes.route("/logout", methods=['GET'])
def do_user_logout():
    logout_user()
    return("logout User")

