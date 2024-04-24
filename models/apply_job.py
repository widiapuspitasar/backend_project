from sqlalchemy import Integer, String, DateTime, ForeignKey, JSON, Enum
from models.base import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from flask_login import UserMixin
from sqlalchemy.orm import relationship

class Apply_job(Base, UserMixin):
    __tablename__= 'apply_job'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    post_job_id = mapped_column(Integer, ForeignKey('post_job.id', ondelete="CASCADE"))
    user_id   = mapped_column(Integer, ForeignKey('user.id', ondelete="CASCADE"))
    status = mapped_column(Enum('Submitted', 'In process', 'Accepted', 'SRejected'), default='Submitted')
    date = mapped_column(DateTime(timezone=True), server_default=func.now())

    post_job = relationship("Post_job", back_populates="apply_job")
    user = relationship("User", back_populates="apply_job")

    def serialize(self, full=True):
        if full:
            return{
                'id': self.id,
                'post_job_id':self.post_job_id,
                'user_id':self.user_id,
                'status':self.status,
                'date':self.date,
            }
        else:
             return{
                'id': self.id,
                'post_job_id':self.post_job_id,
                'status':self.status,
             }
    
    def __repr__(self):
            return f"<Apply_job(id={self.id}, date={self.date})>"
    