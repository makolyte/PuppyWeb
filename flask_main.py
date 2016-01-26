from flask import Flask, render_template, request, redirect, url_for
from database_setup import Base, Puppy, Shelter, Owner, create_engine
from sqlalchemy.orm import sessionmaker
import random
from datetime import date, datetime
import uuid



import os

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

engine = create_engine("sqlite:///puppyweb.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

@app.route("/")
@app.route("/puppies")
def homepage():
    puppies = session.query(Puppy).filter(Puppy.shelter_id != None).all()
    return render_template("puppies.html", puppies=puppies)

@app.route("/puppy/<int:puppy_id>")
def puppy(puppy_id):
    pup = session.query(Puppy).filter(Puppy.id == puppy_id).first()
    shelter = session.query(Shelter).filter(Shelter.id == pup.shelter_id).first()
    return render_template("puppy.html", puppy=pup, shelter=shelter)

def parseDate(dateStr):
    #my sample data seems to be saved in a different format than when creating new records from the web
    #just use a try catch, yes I know it's lazy but this is a udacity project!
    try:
        return datetime.strptime(dateStr, "%Y-%d-%m")
    except:
        return datetime.strptime(dateStr, "%Y-%m-%d")

@app.route("/puppy/<string:operation>/<int:puppy_id>", methods=("GET", "POST"))
def puppyOperation(operation, puppy_id):
    #i'm trying out this style of routing, combining multiple operations instead of having a separate create for each operation (like for shelters)

    #ideally i would manage the images associated with the puppies
    #such that Delete would delete the photo, and Edit would delete a photo if the original was switched out
    #but I don't want to do that on this project
    pup = session.query(Puppy).filter(Puppy.id == puppy_id).first()
    if operation.upper() == "EDIT":
        if request.method == "GET":
            return render_template("edit_puppy.html", puppy=pup)
        else:
            mapRequestToPuppy(request, pup)
            session.commit()
            return redirect(url_for("shelter", shelter_id=pup.shelter_id))
    elif operation.upper() == "DELETE":
        session.delete(pup)
        session.commit()
        return redirect(request.referrer) #use referrer, because they could be coming from home page or shelter page
    elif operation.upper() == "ADOPT":
        pup.shelter_id = None;
        owner = Owner()
        owner.name = request.form["ownerName"]
        session.add(owner)
        pup.owner_id = owner.id
        session.commit()
        return redirect(request.referrer);

@app.route("/shelter/<int:shelter_id>/createpuppy", methods=("GET", "POST"))
def createPuppy(shelter_id):
    if request.method == "GET":
        return render_template("create_puppy.html", shelter_id=shelter_id)
    else:
        newPup = Puppy()
        newPup.shelter_id = shelter_id
        mapRequestToPuppy(request, newPup)

        session.add(newPup)
        session.commit()
        return redirect(url_for("shelter", shelter_id=shelter_id))

def mapRequestToPuppy(request, puppy):
    for key,value in request.form.items():
        print "{0}:{1}".format(key, value)
    puppy.breed = request.form["puppyBreed"]
    puppy.dateOfBirth = parseDate(request.form["puppyDOB"])
    puppy.description = request.form["puppyDescription"]
    puppy.gender = request.form["puppyGender"]
    puppy.name = request.form["puppyName"]
    puppy.weight = request.form["puppyWeight"]
    file = request.files['puppyPic']
#
    if file and allowed_file(file.filename):
        filename = "{0}.{1}".format(str(uuid.uuid4()), getFileExt(file.filename))
        puppy.pictureURL = "images/{0}".format(filename)
        print "Puppy URL = {0}".format(puppy.pictureURL)
        file.save( os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        print "Not saving puppy pic"

def getFileExt(filename):
    fileArr = filename.rsplit(".", 1)
    return fileArr[1].lower()

def allowed_file(filename):
    return '.' in filename and getFileExt(filename) in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.secret_key = "super secret key"
    app.debug = True
    app.run(host='localhost', port=5000)