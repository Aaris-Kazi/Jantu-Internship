from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from database import Base

class Students(Base):
    __tablename__ = "Students"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String, index=True)
    # items = relationship("Item", back_populates="owner")

class Books(Base):
    __tablename__ = "Books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    available = Column(Boolean, default=True)
    
class Inventory(Base):
    __tablename__ = "Inventory"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String, index=True)
    Book_name = Column(String, index=True)
    returned = Column(Boolean, default=True)
    