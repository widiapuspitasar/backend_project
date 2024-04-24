from sqlalchemy import Integer, String, DateTime, ForeignKey, JSON, Enum
from models.base import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from flask_login import UserMixin
from sqlalchemy.orm import relationship

class Post_job(Base, UserMixin):
    __tablename__= 'post_job'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    about_company_id = mapped_column(Integer, ForeignKey('about_company.id', ondelete="CASCADE"))
    company_id   = mapped_column(Integer, ForeignKey('company.id', ondelete="CASCADE"))
    job_name = mapped_column(String(255), nullable=False)
    job_description = mapped_column(String(255), nullable=False)
    post_until = mapped_column(String(255), nullable=False)
    qualification = mapped_column(JSON, nullable=False)
    benefit = mapped_column(JSON, nullable=False)
    address_job = mapped_column(String(255), nullable=False)
    job_level = mapped_column(Enum('Entry-level', 'Intermediate', 'First-level management', 'Senior management'), default='Entry-level')
    job_category = mapped_column(String(255), nullable=False)
    vacancy = mapped_column(String(255), nullable=False)
    educational_requirenment = mapped_column(String(255), nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    about_company = relationship("About_company", back_populates="post_job")
    company= relationship("Company", back_populates="post_job")
    apply_job = relationship("Apply_job", back_populates="post_job")


    def serialize(self, full=True):
        if full:
            return{
                'id': self.id,
                'about_company_id':self.about_company_id,
                'company_id':self.company_id,
                'job_name':self.job_name,
                'job_description':self.job_description,
                'post_until':self.post_until,
                'qualification':self.qualification,
                'benefit':self.benefit,
                'address_job':self.address_job,
                'job_level':self.job_level,
                'job_category':self.job_category,
                'vacancy':self.vacancy,
                'educational_requirenment':self.educational_requirenment,
                'created_at':self.created_at,
                'updated_at':self.updated_at
            }
        else:
            return{
                'id': self.id,
                'about_company_id':self.about_company_id,
                'company_id':self.company_id,
                'job_name':self.job_name,
                'job_description':self.job_description,
                'post_until':self.post_until,
                'qualification':self.qualification,
                'benefit':self.benefit,
                'address_job':self.address_job,
                'job_level':self.job_level,
                'job_category':self.job_category,
                'vacancy':self.vacancy,
                'educational_requirenment':self.educational_requirenment,
            }
        
    def __repr__(self):
            return f"<Post_job(id={self.id}, job_name={self.job_name})>"
