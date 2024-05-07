from flask import Blueprint, jsonify, request
from connectors.mysql_connector import engine
from models.apply_job import Apply_job
from sqlalchemy.orm import sessionmaker
from flask_login import  login_required, current_user

status_job_routes = Blueprint('status_job_routes', __name__)

@login_required
@status_job_routes.route("/status_inprocess/<int:user_id>/<int:apply_job_id>", methods=['PUT'])
def inprocess_apply(user_id, apply_job_id):
    try:
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()

        apply_job = session.query(Apply_job).filter_by(id=apply_job_id).first()

        if not apply_job:
            return jsonify({'message': 'Apply job not found'}), 404

        if apply_job.post_job.company_id != user_id:
            return jsonify({'message': 'Forbidden: You do not have permission to update this apply job'}), 403

        apply_job.status = 'In process'
        session.commit()

        return jsonify({'message': 'Apply job status updated successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        session.close()



@login_required
@status_job_routes.route("/status_accepted/<int:user_id>/<int:apply_job_id>", methods=['PUT'])
def accepted_apply(apply_job_id):
    try:
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()

        apply_job = session.query(Apply_job).filter_by(id=apply_job_id).first()

        if not apply_job:
            return jsonify({'message': 'Apply job not found'}), 404

        if apply_job.post_job.company_id != current_user.id:
             return jsonify({'message': 'Forbidden: You do not have permission to update this apply job'}), 403

        apply_job.status = 'Accepted'
        session.commit()

        return jsonify({'message': 'Apply job status updated successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        session.close()

@login_required
@status_job_routes.route("/status_rejected/<int:user_id>/<int:apply_job_id>", methods=['PUT'])
def rejected_apply(apply_job_id):
    try:
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()

        apply_job = session.query(Apply_job).filter_by(id=apply_job_id).first()

        if not apply_job:
            return jsonify({'message': 'Apply job not found'}), 404

        if apply_job.post_job.company_id != current_user.id:
            return jsonify({'message': 'Forbidden: You do not have permission to update this apply job'}), 403

        apply_job.status = 'Rejected'
        session.commit()

        return jsonify({'message': 'Apply job status updated successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        session.close()


@login_required
@status_job_routes.route("/status_update/<int:user_id>/<int:apply_job_id>", methods=['PUT'])
def update_apply_job_status(user_id, apply_job_id):
    try:
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()

        apply_job = session.query(Apply_job).filter_by(id=apply_job_id).first()

        if not apply_job:
            return jsonify({'message': 'Apply job not found'}), 404

        if apply_job.user_id != user_id:
            return jsonify({'message': 'Forbidden: You do not have permission to update this apply job'}), 403

        new_status = request.json.get('status')

        if new_status not in ['Submitted', 'In process', 'Accepted', 'Rejected']:
            return jsonify({'message': 'Invalid status'}), 400

        apply_job.status = new_status
        session.commit()

        return jsonify({'message': 'Apply job status updated successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        session.close()

