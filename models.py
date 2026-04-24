from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column,Integer,String,Text,ForeignKey,Boolean,DateTime
class  NoteTable(Base):
    __tablename__ = "Notes"
    id = Column(Integer,primary_key=True,)
    title = Column(String)
    content = Column(Text)
    priority = Column(Integer, default=3)
    delete_at = Column(DateTime(timezone=True),nullable=True,index=True)
    user_id = Column(Integer,ForeignKey("Users.id",ondelete="CASCADE"),index=True)
    owner = relationship("UserTable", back_populates="notes")
class UserTable(Base):
    __tablename__="Users"
    id = Column(Integer,primary_key=True,index=True)
    email =Column(String,unique=True,index=True,nullable=False)
    hashed_password=Column(String,nullable=False)
    is_active = Column(Boolean,nullable=False,default=True)
    notes = relationship("NoteTable",back_populates="owner")