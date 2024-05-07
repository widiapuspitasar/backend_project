from sqlalchemy import Integer, DateTime, ForeignKey
from models.base import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from flask_login import UserMixin
from sqlalchemy.orm import relationship

class Favorite_job(Base, UserMixin):
    __tablename__ = 'favorite_job'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    post_job_id = mapped_column(Integer, ForeignKey('post_job.id', ondelete="CASCADE"))
    user_id   = mapped_column(Integer, ForeignKey('user.id', ondelete="CASCADE"))
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())

    post_job = relationship("Post_job", back_populates="favorite_job")
    user = relationship("User", back_populates="favorite_job")

    def serialize(self, full=True):
        if full:
            return{
                'id': self.id,
                'post_job_id':self.post_job_id,
                'user_id':self.user_id,
                'created_at':self.created_at,
            }
        else:
             return{
                'id': self.id,
                'post_job_id':self.post_job_id,
                'user_id':self.user_id,
             }
    
    def __repr__(self):
            return f"<Apply_job(id={self.id})>"
    