from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey,Column,Integer,VARCHAR,Text,TIMESTAMP,func

from .session import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer,autoincrement=True,primary_key=True)
    name_user = Column(VARCHAR(40),nullable=False)
    language_name = Column(VARCHAR(40),nullable=False)

    def __repr__(self,*args,**kwargs):
        return f"{self.name_user}"


class Achivments(Base):
    __tablename__ = "achivments"
    achivment_id = Column(Integer,autoincrement=True,primary_key=True)
    achivment_name = Column(VARCHAR(140),nullable=False)
    number_of_points = Column(Integer)


class Description(Base):
    __tablename__ = "description"
    description_id = Column(Integer,autoincrement=True,primary_key=True)
    language_name = Column(VARCHAR(40),nullable=False)
    achivment_id = Column(ForeignKey("achivments.achivment_id"))
    description = Column(Text)

class Achivment_recived(Base):
    __tablename__ = "achivment_recived"
    achivment_recived_id = Column(Integer,autoincrement=True,primary_key=True)
    user_id = Column(ForeignKey("users.user_id"))
    achivment_id = Column(ForeignKey("achivments.achivment_id"))
    date_of_recived = Column(TIMESTAMP,server_default=func.now())


