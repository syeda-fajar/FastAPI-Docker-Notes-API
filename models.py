from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column,Integer,String,Text,ForeignKey
class  NoteTable(Base):
    __tablename__ = "Notes"
    id = Column(Integer,primary_key=True,)
    title = Column(String)
    content = Column(Text)
    priority = Column(Integer, default=3)
    user_id = Column(Integer,ForeignKey("Users.id",ondelete="CASCADE"))
    owner = relationship("UserTable", back_populates="notes")
class UserTable(Base):
    __tablename__="Users"
    id = Column(Integer,primary_key=True,index=True)
    email =Column(String,unique=True,index=True,nullable=False)
    hashed_password=Column(String,nullable=False)
    notes = relationship("NoteTable",back_populates="owner")