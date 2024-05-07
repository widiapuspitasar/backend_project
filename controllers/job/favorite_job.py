from flask import Blueprint, jsonify
from connectors.mysql_connector import engine
from models.favorite_job import Favorite_job
from models.post_job import Post_job
from models.company import Company
from models.user import User
from sqlalchemy.orm import sessionmaker
from flask_login import login_required, current_user
from flask import jsonify

favorite_job_routes = Blueprint('favorite_job_routes', __name__)

@login_required
@favorite_job_routes.route("/favorite/<int:user_id>/<int:post_job_id>", methods=['POST'])
def do_favorite(user_id, post_job_id):
        try:
            connection = engine.connect()
            Session = sessionmaker(connection)
            session = Session()

            existing_favorite = session.query(Favorite_job).filter_by(user_id=user_id, post_job_id=post_job_id).first()
            if existing_favorite:
                return jsonify({'message': 'Job already favorited by the user'}), 400

            favorite_job = Favorite_job(
                user_id=user_id,
                post_job_id=post_job_id
            )

            session.add(favorite_job)
            session.commit()

            return jsonify({'message': 'Job added to favorites successfully'}), 200
        except Exception as e:
            return jsonify({'message': str(e)}), 500
        finally:
            session.close()

@login_required
@favorite_job_routes.route("/favorite/<int:user_id>/<int:post_job_id>", methods=['DELETE'])
def delete_favorite(user_id, post_job_id):
        try:
            connection = engine.connect()
            Session = sessionmaker(connection)
            session = Session()

            favorite_job = session.query(Favorite_job).filter_by(user_id=user_id, post_job_id=post_job_id).first()

            if not favorite_job:
                return jsonify({'message': 'Favorite job not found'}), 404

            session.delete(favorite_job)
            session.commit()

            return jsonify({'message': 'Favorite job deleted successfully'}), 200
        except Exception as e:
            return jsonify({'message': str(e)}), 500
        finally:
            session.close()

@login_required
@favorite_job_routes.route("/favorite_list/<int:user_id>", methods=['GET'])
def favorite_list(user_id):
    print(current_user)
    session = None
    try:
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()

        user = session.query(User).filter_by(id=user_id).first()

        if not user:
            return jsonify({'message': 'User not found'}), 404

        favorite_jobs = session.query(Favorite_job).filter_by(user_id=user_id).all()
        favorite_job_data = []

        for favorite_job in favorite_jobs:
            post_job = session.query(Post_job).filter_by(id=favorite_job.post_job_id).first()
            if post_job:
                company = session.query(Company).filter_by(id=post_job.company_id).first()
                favorite_job_data.append({
                    "user_name": user.name,
                    "user_email": user.email,
                    "post_job_id": post_job.id,
                    "job_name": post_job.job_name,
                    "company_name": company.company_name,
                    "created_at": favorite_job.created_at
                })

        return jsonify({
            'message': 'Success',
            'data': favorite_job_data
        }), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        if session:
            session.close()


