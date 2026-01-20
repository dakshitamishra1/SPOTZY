from app.database import Base
from sqlalchemy import Column, Integer, String ,Boolean ,Text


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(80), unique=True, index=True, nullable=False)
    password = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)



    def __repr__(self):
        return f"<User{self.username}>"
    