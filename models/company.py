from sqlalchemy import Integer, String, DateTime
from models.base import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from flask_login import UserMixin
import bcrypt
from sqlalchemy.orm import relationship

class Company(Base, UserMixin):
    __tablename__='company'
    
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    company_name = mapped_column(String(255), nullable=False, unique=True)
    employer_name = mapped_column(String(255), nullable=False, unique=True)
    company_email = mapped_column(String(255), nullable=False, unique=True)
    password = mapped_column(String(255), nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())

    about_company = relationship("About_company", back_populates="company")
    post_job = relationship("Post_job", back_populates="company")
    

    def serialize(self, full=True):
        if full:
            return{
                'id': self.id,
                'company_name':self.company_name,
                'employer_name':self.employer_name,
                'company_email':self.company_email,
                'password':self.password,
                'created_at':self.created_at
            }
        else:
            return{
               'id': self.id,
                'company_name':self.company_name,
                'employer_name':self.employer_name,
                'company_email':self.company_email,
            }
    
    def __repr__(self):
        return f'<Company{self.company_name}>'
    
    def set_password(self, password):
        self.password = bcrypt.hashpw( password.encode('utf-8') , bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
