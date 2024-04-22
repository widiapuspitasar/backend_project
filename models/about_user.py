from sqlalchemy import Integer, String, DateTime, ForeignKey, JSON
from models.base import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from flask_login import UserMixin
from sqlalchemy.orm import relationship

class About_user(Base, UserMixin):
    __tablename__='about_user'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey('user.id', ondelete="CASCADE"))
    name = mapped_column(String(255), nullable=False, unique=True)
    skill = mapped_column(JSON, nullable=False)
    phonenumber = mapped_column(String(255), nullable=False)
    about_user = mapped_column(String(255), nullable=False)
    email = mapped_column(String(255), nullable=False, unique=True)
    file_resume = mapped_column(String(255), nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    user = relationship("User", back_populates="about_user")

    def serialize(self, full=True):
        if full:
            return{
                'id': self.id,
                'user_id':self.user_id,
                'name':self.name,
                'skill':self.skill,
                'phonenumber':self.phonenumber,
                'about_user':self.about_user,
                'email':self.email,
                'file_resume':self.file_resume,
                'created_at':self.created_at,
                'updated_at':self.updated_at
            }
        else:
            return{
                'id': self.id,
                'user_id':self.user_id,
                'name':self.name,
                'skill':self.skill,
                'phonenumber':self.phonenumber,
                'about_user':self.about_user,
                'email':self.email,
                'file_resume':self.file_resume,
            }
        
    def __repr__(self):
        return f"<About_user(id={self.id}, email={self.email})>"
