from sqlalchemy import Boolean, Column, Integer, String

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uName = Column(String(50))
    uEmail = Column(String(80), unique=True)
    uId = Column(Integer)
