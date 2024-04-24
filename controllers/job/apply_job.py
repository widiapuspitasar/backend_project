from flask import Blueprint, jsonify, request, redirect
from requests import Session
from connectors.mysql_connector import engine
from models.apply_job import Apply_job
from models.post_job import Post_job
from models.about_company import About_company
from models.company import Company
from models.user import User
from sqlalchemy.orm import sessionmaker
from flask_login import login_user, login_required, logout_user, current_user
from utils.api_reponse import api_response
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

apply_job_routes = Blueprint('apply_job_routes', __name__)

# @login_required
# @apply_job_routes.route("/user/apply_job", methods=['POST'])
# def apply_job():
#     try:
#         session = Session()

#         data = request.json
#         user_id = data.get('user_id')
#         post_job_id = data.get('post_job_id')
#         status = data.get('status')


#         user = session.query(User).filter_by(id=user_id).first()
#         post_job = session.query(Post_job).filter_by(id=post_job_id).first()

#         if not user:
#             return jsonify({'message': 'User not found'}), 404
#         if not post_job:
#             return jsonify({'message': 'Post job not found'}), 404

#         apply_job = Apply_job(
#             user_id=user_id,
#             post_job_id=post_job_id,
#             status='Submitted'
#         )
#         session.add(apply_job)
#         session.commit()

#         return jsonify({'message': 'Job application submitted successfully'}), 200
#     except Exception as e:
#         return jsonify({'message': str(e)}), 500
#     finally:
#         session.close()

@login_required
@apply_job_routes.route("/user/apply_job", methods=['POST'])
def apply_job():
    session = None
    try:
        data = request.json
        user_id = data.get('user_id')
        post_job_id = data.get('post_job_id')
        status = data.get('status')
        date = data.get('date')

        if  not post_job_id or not status:
            return api_response(
                    status_code=400,
                    message="post_job_id, status are required",
                    data={}
            )
        session = Session()
        print(f"user_id: {user_id}, post_job_id: {post_job_id}, status: {status}, : {date}")
        NewApply = Apply_job(user_id=current_user.id, post_job_id=post_job_id, status=status, date=date)
        

        session.begin()
        session.add(NewApply)
        session.commit()

        return api_response(
            status_code=201,
            message="New job data has been successfully added",
            data={
                    "id": NewApply.id,
                    "user_id": NewApply.user_id,
                    "post_job_id": NewApply.post_job_id,
                    "status": NewApply.status,
                    "date": NewApply.date
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