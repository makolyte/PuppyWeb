from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random

Base = declarative_base()

class Shelter(Base):
    #Minimized this by stripping out all address fields except for City
    __tablename__="shelter"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    city = Column(String(80))

class Owner(Base):
    __tablename__="owner"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False)
    gender = Column(String(6), nullable = False)
    dateOfBirth = Column(Date)
    pictureURL = Column(String)
    weight = Column(Numeric(10, 2))
    breed = Column(String(15))
    description = Column(String(250))
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)
    owner_id = Column(Integer, ForeignKey("owner.id"))
    owner = relationship(Owner)





def CreateDB():
    engine = create_engine("sqlite:///puppyweb.db")
    Base.metadata.create_all(engine)


def AddABunchOfFakePuppies():
    engine = create_engine('sqlite:///puppyweb.db')

    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)

    session = DBSession()


    #Add Shelters
    shelter1 = Shelter(name = "San Juan Animal Services", city = "San Juan")
    session.add(shelter1)

    shelter2 = Shelter(name = "San Juan Adoption Center", city="San Juan")
    session.add(shelter2)

    shelter3 = Shelter(name = "Carolina Dog Rescue", city = "Carolina")
    session.add(shelter3)

    shelter4 = Shelter(name = "Humane Society of Luqillo",city = "Luquillo")
    session.add(shelter4)

    shelter5 = Shelter(name = "Bayamon Humane Society" ,city = "Bayamon")
    session.add(shelter5)


    #Add Puppies

    gender = ["male", "female"]

    male_names = ["Bailey", "Max", "Charlie", "Buddy","Rocky","Jake", "Jack", "Toby", "Cody", "Buster",
                  "Duke", "Cooper", "Riley", "Harley", "Bear", "Tucker", "Murphy", "Lucky", "Oliver",
                  "Sam", "Oscar", "Teddy", "Winston", "Sammy", "Rusty", "Shadow", "Gizmo", "Bentley",
                  "Zeus", "Jackson", "Baxter", "Bandit", "Gus", "Samson", "Milo", "Rudy", "Louie", "Hunter",
                  "Casey", "Rocco", "Sparky", "Joey", "Bruno", "Beau", "Dakota", "Maximus", "Romeo", "Boomer", "Luke", "Henry"]

    female_names = ['Bella', 'Lucy', 'Molly', 'Daisy', 'Maggie', 'Sophie', 'Sadie', 'Chloe', 'Bailey', 'Lola',
                    'Zoe', 'Abby', 'Ginger', 'Roxy', 'Gracie', 'Coco', 'Sasha', 'Lily', 'Angel', 'Princess',
                    'Emma', 'Annie', 'Rosie', 'Ruby', 'Lady', 'Missy', 'Lilly', 'Mia', 'Katie', 'Zoey', 'Madison',
                    'Stella', 'Penny', 'Belle', 'Casey', 'Samantha', 'Holly', 'Lexi', 'Lulu', 'Brandy', 'Jasmine',
                    'Shelby', 'Sandy', 'Roxie', 'Pepper', 'Heidi', 'Luna', 'Dixie', 'Honey', 'Dakota']
    names = {"male": male_names, "female":female_names}


    puppy_images = ["images/Puppy1.PNG",
                    "images/Puppy2.PNG",
                    "images/Puppy3.PNG",
                    "images/Puppy4.PNG",
                    "images/Puppy5.PNG",
                    "images/Puppy6.PNG",
                    "images/Puppy7.PNG"]

    breeds = ["Mutt", "Corgi", "Terrier", "Cockerspaniel", "Pommeranian", "Weiner Dog", "Collie"]

    descriptions = ["Well-behaved, friendly", "Nice to people, aggressive towards other dogs", "Very energetic"]

    for pupImage in puppy_images:
        newPup = Puppy()
        newPup.gender = random.choice(gender)
        newPup.name = random.choice(names[newPup.gender])
        newPup.dateOfBirth = CreateRandomAge()
        newPup.breed = random.choice(breeds)
        newPup.description = random.choice(descriptions)
        newPup.shelter_id=randint(1,5)
        newPup.weight= CreateRandomWeight()
        newPup.pictureURL = pupImage
        session.add(newPup)

	session.commit()

#This method will make a random age for each puppy between 0-18 months(approx.) old from the day the algorithm was run.
def CreateRandomAge():
	today = datetime.date.today()
	days_old = randint(0,540)
	birthday = today - datetime.timedelta(days = days_old)
	return birthday

#This method will create a random weight between 1.0-40.0 pounds (or whatever unit of measure you prefer)
def CreateRandomWeight():
	return random.uniform(1.0, 40.0)

def DeleteAllPuppies():
    from flask import Flask, render_template
    from database_setup import Base, Puppy, Shelter, Owner, create_engine
    from sqlalchemy.orm import sessionmaker



    engine = create_engine("sqlite:///puppyweb.db")
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    puppies = session.query(Puppy).all();
    for p in puppies:
        session.delete(p)
    session.commit()

def ResetData():
    DeleteAllPuppies()
    AddABunchOfFakePuppies()



def GetSession():
    engine = create_engine('sqlite:///puppyweb.db')

    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)

    session = DBSession()

    return session
