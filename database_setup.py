from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Shelter(Base):
    #Minimized this by stripping out all address fields except for City
    __tablename__="shelter"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    city = Column(String(80))

class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False)
    gender = Column(String(6), nullable = False)
    dateOfBirth = Column(Date)
    pictureURL = Column(String)
    weight = Column(Numeric(10))
    breed = Column(String(15))
    description = Column(String(250))
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)
    owner_id = Column(Integer, ForeignKey("owner.id"))
    owner = relationship(Owner)


class Owner(Base):
    __tablename__="owner"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

