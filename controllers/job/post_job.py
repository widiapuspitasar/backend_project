from flask import Blueprint,request
from connectors.mysql_connector import engine
from models.about_company import About_company
from models.post_job import Post_job
from models.company import Company
from sqlalchemy.orm import sessionmaker
from flask_login import login_required, current_user
from models.user import User
from utils.api_reponse import api_response
from sqlalchemy import func
from sqlalchemy.orm import joinedload

post_job_routes = Blueprint('post_job_routes', __name__)

@login_required
@post_job_routes.route("/company/create_job/<int:company_id>", methods=['POST'])
def create_post_job(company_id):
        session = None
        try:
            data = request.json
            job_name = data.get('job_name')
            job_description = data.get('job_description')
            post_until = data.get('post_until')
            qualification = data.get('qualification')
            benefit = data.get('benefit')
            address_job = data.get('address_job')
            job_level = data.get('job_level')
            job_category = data.get('job_category')
            vacancy = data.get('vacancy')
            educational_requirenment = data.get('educational_requirenment')
        
            if not job_name or not job_description or not post_until or not qualification or not benefit or not address_job or not job_level or not job_category or not vacancy or not educational_requirenment:
                return api_response(
                    status_code=400,
                    message="Job name, job description, post until, qualification, benefit, address job, job level, job category, vacancy, and educational requirement are required",
                    data={}
                )
        
            print(f"job_name: {job_name}, job_description: {job_description}, post_until: {post_until}, qualification: {qualification}, benefit: {benefit}, address_job: {address_job}, job_level: {job_level}, job_category: {job_category}, vacancy: {vacancy}, educational_requirenment: {educational_requirenment}")
            NewJob = Post_job(company_id=company_id, job_name=job_name, job_description=job_description, post_until=post_until, qualification=qualification, benefit=benefit, address_job=address_job, job_level=job_level, job_category=job_category, vacancy=vacancy, educational_requirenment=educational_requirenment)

            connection = engine.connect()
            Session = sessionmaker(connection)
            session = Session()

            session.begin()
            session.add(NewJob)
            session.commit()
        

            return api_response(
                status_code=201,
                message="New job data has been successfully added",
                data={
                    "id": NewJob.id,
                    "company_id": NewJob.company_id,
                    "about_company_id": NewJob.about_company_id,
                    "job_name": NewJob.job_name,
                    "job_description": NewJob.job_description,
                    "post_until": NewJob.post_until,
                    "qualification": NewJob.qualification,
                    "benefit": NewJob.benefit,
                    "address_job": NewJob.address_job,
                    "job_level": NewJob.job_level,
                    "job_category": NewJob.job_category,
                    "vacancy": NewJob.vacancy,
                    "educational_requirenment": NewJob.educational_requirenment
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
@post_job_routes.route("/company/job", methods=['GET'])
def get_job_list():
    session = None
    try:
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()

        companies_with_jobs = session.query(Company).options(joinedload(Company.post_job)).all()
        company_job_data = []

        for company in companies_with_jobs:
            for job in company.post_job:
                company_job_data.append({
                    "id": job.id,
                    "company_name": company.company_name,
                    "company_email": company.company_email,
                    "job_name": job.job_name,
                    "job_description": job.job_description,
                    "post_until": job.post_until,
                    "qualification": job.qualification,
                    "benefit": job.benefit,
                    "address_job": job.address_job,
                    "job_level": job.job_level,
                    "job_category": job.job_category,
                    "vacancy": job.vacancy,
                    "educational_requirenment": job.educational_requirenment
                })

        return api_response(
            status_code=200,
            message="Success",
            data=company_job_data
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
@post_job_routes.route("/company/job_list/<int:company_id>", methods=['GET']) 
def get_job_list_by_company_id(company_id):
    try:
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()
        
        company = session.query(Company).filter_by(id=company_id).first()

        if company:
            company_job_data = []
            for job in company.post_job:
                company_job_data.append({
                    "id": job.id,
                    "company_name": company.company_name,
                    "company_email": company.company_email,
                    "job_name": job.job_name,
                    "job_description": job.job_description,
                    "post_until": job.post_until,
                    "qualification": job.qualification,
                    "benefit": job.benefit,
                    "address_job": job.address_job,
                    "job_level": job.job_level,
                    "job_category": job.job_category,
                    "vacancy": job.vacancy,
                    "educational_requirenment": job.educational_requirenment
                })

            return api_response(
                status_code=200,
                message="Success",
                data=company_job_data
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
        if session:
            session.close()


@login_required
@post_job_routes.route("/company/job/<int:post_job_id>", methods=['GET'])
def get_job(post_job_id):
        session = None
        try:
            connection = engine.connect()
            Session = sessionmaker(connection)
            session = Session()

            
            about_company = session.query(About_company).filter_by(id=About_company.id).first()
            post_job = session.query(Post_job).filter_by(id=post_job_id).first()

            if post_job:
                company = session.query(Company).filter_by(id=post_job.company_id).first()
                job_data = {
                    "about_us": about_company.about_us,
                    "phonenumber": about_company.phonenumber,
                    "email": about_company.email,
                    "company_name": company.company_name,
                    "company_email": company.company_email,
                    "job_name": post_job.job_name,
                    "job_description": post_job.job_description,
                    "post_until": post_job.post_until,
                    "qualification": post_job.qualification,
                    "benefit": post_job.benefit,
                    "address_job": post_job.address_job,
                    "job_level": post_job.job_level,
                    "job_category": post_job.job_category,
                    "vacancy": post_job.vacancy,
                    "educational_requirenment": post_job.educational_requirenment
                }

                return api_response(
                    status_code=200,
                    message="Success",
                    data=job_data
                )
            else:
                return api_response(
                    status_code=404,
                    message="Post job not found",
                    data={}
                )
        except Exception as e:
            return api_response(
                status_code=500,
                message="Server error: " + str(e),
                data={}
            )
      
@login_required
@post_job_routes.route("/company/job/<int:post_job_id>", methods=['PUT'])
def update_job(post_job_id):
    if isinstance(current_user, Company):
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()
        session.begin()

        try: 
            update_job = session.query(Post_job).filter(Post_job.id == post_job_id).first()

            update_job.job_name = request.json.get('job_name', update_job.job_name)
            update_job.job_description = request.json.get('job_description', update_job.job_description)
            update_job.post_until = request.json.get('post_until', update_job.post_until)
            update_job.qualification = request.json.get('qualification', update_job.qualification)
            update_job.benefit = request.json.get('benefit', update_job.benefit)
            update_job.address_job = request.json.get('address_job', update_job.address_job)
            update_job.job_level = request.json.get('job_level', update_job.job_level)
            update_job.job_category = request.json.get('job_category', update_job.job_category)
            update_job.vacancy = request.json.get('vacancy', update_job.vacancy) 
            update_job.educational_requirenment = request.json.get('educational_requirenment', update_job.educational_requirenment)  
            update_job.updated_at = func.now()

            session.commit()
                
            return api_response(
                status_code=201,
                message="About Company data updated successfully",
                data={
                        "job_name": update_job.job_name,
                        "job_description": update_job.job_description,
                        "post_until": update_job.post_until,
                        "qualification": update_job.qualification,
                        "benefit": update_job.benefit,
                        "address_job": update_job.address_job,
                        "job_level": update_job.job_level,
                        "job_category": update_job.job_category,
                        "educational_requirenment": update_job.educational_requirenment,
                        "vacancy": update_job.vacancy,
                        "updated_at": update_job.updated_at
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

