from flask import Blueprint, jsonify
from connectors.mysql_connector import engine
from models.apply_job import Apply_job
from models.post_job import Post_job
from models.company import Company
from models.user import User
from sqlalchemy.orm import sessionmaker
from flask_login import login_required
from utils.api_reponse import api_response
from sqlalchemy.exc import SQLAlchemyError


apply_job_routes = Blueprint('apply_job_routes', __name__)


@apply_job_routes.route("/<int:user_id>/apply_job/<int:post_job_id>", methods=['POST'])
def do_apply_job(user_id, post_job_id):
    try:
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()

        post_job = session.query(Post_job).filter_by(id=post_job_id).first()
        if not post_job:
            return jsonify({'message': 'Post job not found'}), 404

        company_id = post_job.company_id

        existing_application = session.query(Apply_job).filter_by(user_id=user_id, post_job_id=post_job_id).first()
        if existing_application:
            return jsonify({'message': 'Job application already submitted by the user'}), 400

        apply_job = Apply_job(
            user_id=user_id,
            post_job_id=post_job_id,
            company_id=company_id  
        )
        session.add(apply_job)
        session.commit()

        return jsonify({'message': 'Job application submitted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        session.close()


@login_required
@apply_job_routes.route("/<int:user_id>/apply_list", methods=['GET'])
def user_apply_list(user_id):
    user = None 
    try:
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()

        user = session.query(User).filter_by(id=user_id).first()
        user_job_data = []

        for job in user.apply_job:
            post_job = session.query(Post_job).filter_by(id=job.post_job_id).first()
            company = session.query(Company).filter_by(id=post_job.company_id).first()
            user_job_data.append({
                    "user_name": user.name,
                    "user_email": user.email,
                    "post_job_id": job.post_job_id,
                    "status": job.status,
                    "date": job.date,
                    "job_name": post_job.job_name,
                    "company_name": company.company_name,
            })
        return api_response(
            status_code=200,
            message="Success",
            data=user_job_data
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
        if user:
            session.close()

@login_required
@apply_job_routes.route("/apply_list/<int:company_id>", methods=['GET'])
def company_apply_list(company_id):
    try:
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()

        company = session.query(Company).filter_by(id=company_id).first()
        
        company_list_apply = []


        if company:
            for apply_job in company.apply_job:
                user = session.query(User).filter_by(id=apply_job.user_id).first()
                post_job = session.query(Post_job).filter_by(id=apply_job.post_job_id).first()
                if user and post_job:
                    company_list_apply.append({
                        "post_job_id": apply_job.post_job_id,
                        "status": apply_job.status,
                        "date": apply_job.date,
                        "job_name": post_job.job_name,
                        "company_name": company.company_name,
                        "user_name": user.name,
                        "user_id": user.id,
                        "user_email": user.email,
                        "apply_job_id":apply_job.id
                    })

            return api_response(
                status_code=200,
                message="Success",
                data=company_list_apply
            )
        else:
            return api_response(
                status_code=404,
                message="Company not found",
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
@apply_job_routes.route("/apply_list/post_job/<int:post_job_id>", methods=['GET'])
def list_user_apply_job(post_job_id):
    try:
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()
        
        apply_jobs = session.query(Apply_job).filter_by(post_job_id=post_job_id).all()
        company_list_apply = []

        for apply_job in apply_jobs:
            user = session.query(User).filter_by(id=apply_job.user_id).first()
            post_job = session.query(Post_job).filter_by(id=apply_job.post_job_id).first()

            if user and post_job:
                company_list_apply.append({
                    "post_job_id": apply_job.post_job_id,
                    "status": apply_job.status,
                    "date": apply_job.date,
                    "job_name": post_job.job_name,
                    "company_name": post_job.company.company_name,
                    "user_name": user.name,
                    "user_id": user.id,
                    "user_email": user.email,
                    "apply_job_id": apply_job.id
                })

        return api_response(
            status_code=200,
            message="Success",
            data=company_list_apply
        )
    except Exception as e:
        return api_response(
            status_code=500,
            message="Server error: " + str(e),
            data={}
        )
    finally:
        session.close()






