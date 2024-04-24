from sqlalchemy import Integer, String, DateTime
from models.base import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from flask_login import UserMixin
import bcrypt
from sqlalchemy.orm import relationship

class User(Base, UserMixin):
    __tablename__ = 'user'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    email = mapped_column(String(255), nullable=False, unique=True)
    name = mapped_column(String(255), nullable=False, unique=True)
    password = mapped_column(String(255), nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    about_user = relationship("About_user", back_populates="user")
    apply_job = relationship("Apply_job", back_populates="user")

    def serialize(self, full=True):
        if full:
            return{
                'id': self.id,
                'name': self.name,
                'email': self.email,
                'password': self.password,
                'created_at': self.created_at
            }
        else:
            return {
                'id': self.id,
                'name': self.name,
                'email': self.email
            }
    
    def __repr__(self):
        return f'<User{self.name}>'
    
    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
