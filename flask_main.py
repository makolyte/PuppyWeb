from flask import Flask, render_template, request, redirect, url_for
from database_setup import Base, Puppy, Shelter, Owner, create_engine
from sqlalchemy.orm import sessionmaker
import random


engine = create_engine("sqlite:///puppyweb.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

@app.route("/shelters")
def shelters():
    shelters = session.query(Shelter).all()
    return render_template("shelters.html", shelters=shelters)

@app.route("/shelter/<int:shelter_id>")
def shelter(shelter_id):
    shelter = session.query(Shelter).filter(Shelter.id == shelter_id).first()
    puppies = session.query(Puppy).filter(Puppy.shelter_id == shelter_id)
    return render_template("shelter.html", shelter = shelter, puppies=puppies)

@app.route("/shelter/<int:shelter_id>/edit", methods=("GET", "POST"))
def editShelter(shelter_id):
    #I'm not putting error handling in here. This would obviously need to chekc if the shelter exists, and redirect to an error page or something
    shelter = session.query(Shelter).filter(Shelter.id == shelter_id).first()
    if request.method == "GET":
        return render_template("edit_shelter.html", shelter=shelter)
    else:
        shelter.name = request.form["shelterName"]
        shelter.city = request.form["shelterCity"]
        session.commit()
        return redirect(url_for("shelter", shelter_id=shelter_id))
        #TODO flash success message

@app.route("/shelter/<int:shelter_id>/delete")
def deleteShelter(shelter_id):
    #first, move the puppies randomly amongst the other shelters
    #note: this ignores the fact that there could be 0 shelters

    allOtherShelters = session.query(Shelter).filter(Shelter.id != shelter_id).all()

    puppies = session.query(Puppy).filter(Puppy.shelter_id==shelter_id).all()
    for puppy in puppies:
        puppy.shelter_id = random.choice(allOtherShelters).id

    shelter = session.query(Shelter).filter(Shelter.id == shelter_id).first()
    session.delete(shelter)
    session.commit()
    return redirect(url_for("shelters"))
    #TODO - flash success message

@app.route("/createShelter", methods=("GET", "POST"))
def createShelter():
    if request.method == "GET":
        return render_template("create_shelter.html")
    else:
        #Validation would be done on the client-side with JS, which i'm not going to do in this project
        newShelter = Shelter()
        newShelter.name = request.form["shelterName"]
        newShelter.city = request.form["shelterCity"]
        session.add(newShelter)
        session.commit()
        return redirect(url_for("shelters"))
        #TODO flash success message

@app.route("/")
@app.route("/puppies")
def homepage():
    puppies = session.query(Puppy).all()
    return render_template("puppies.html", puppies=puppies)

@app.route("/puppy/<int:puppy_id>")
def puppy(puppy_id):
    #TODO: Create puppy profile
    return "TODO Create puppy profile"

@app.route("/puppy/<string:operation>/<int:puppy_id>")
def puppyOperation(operation, puppy_id): #i'm trying out this style of routing, combining multiple operations instead of having a separate create for each operation (like for shelters)
    #TODO - Create puppy delete page
    #TODO - Create puppy edit page
    #TODO - Create puppy adopt page
    return "operation={0} puppy_id={1}".format(operation, puppy_id)

@app.route("/createpuppy")
def createPuppy():
    #TODO - Create create puppy page
    return "TODO - Create create puppy page"

if __name__ == '__main__':
    app.secret_key = "super secret key"
    app.debug = True
    app.run(host='localhost', port=5000)