from sqlalchemy import Integer, String, DateTime, ForeignKey
from models.base import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from flask_login import UserMixin
from sqlalchemy.orm import relationship

class About_company(Base,UserMixin):
    __tablename__= 'about_company'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    company_id = mapped_column(Integer, ForeignKey('company.id', ondelete="CASCADE"))
    company_type = mapped_column(String(255), nullable=False)
    address = mapped_column(String(255), nullable=False)
    phonenumber = mapped_column(String(255), nullable=False)
    about_us = mapped_column(String(255), nullable=False)
    email = mapped_column(String(255), nullable=False, unique=True)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    company = relationship("Company", back_populates="about_company")

    def serialize(self, full=True):
        if full:
            return{
                'id': self.id,
                'company_id':self.company_id,
                'company_type':self.company_type,
                'address':self.address,
                'phonenumber':self.phonenumber,
                'about_us':self.about_us,
                'email':self.email,
                'created_at':self.created_at,
                'updated_at':self.updated_at
            }
        else:
            return{
                'id': self.id,
                'company_id':self.company_id,
                'company_type':self.company_type,
                'address':self.address,
                'phonenumber':self.phonenumber,
                'about_us':self.about_us,
                'email':self.about_us,
            }
    def __repr__(self):
        return f"<About_company(id={self.id}, email={self.email})>"
