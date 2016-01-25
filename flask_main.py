from flask import Flask, render_template, request, redirect, url_for
from database_setup import Base, Puppy, Shelter, Owner, create_engine
from sqlalchemy.orm import sessionmaker
import random
from datetime import date, datetime

import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

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
    puppies = session.query(Puppy).all()
    return render_template("puppies.html", puppies=puppies)

@app.route("/puppy/<int:puppy_id>")
def puppy(puppy_id):
    pup = session.query(Puppy).filter(Puppy.id == puppy_id).first()
    shelter = session.query(Shelter).filter(Shelter.id == pup.shelter_id).first()
    return render_template("puppy.html", puppy=pup, shelter=shelter)

@app.route("/puppy/<string:operation>/<int:puppy_id>", methods=("GET", "POST"))
def puppyOperation(operation, puppy_id): #i'm trying out this style of routing, combining multiple operations instead of having a separate create for each operation (like for shelters)
    #TODO - Create puppy delete page
    #TODO - Create puppy adopt page
    pup = session.query(Puppy).filter(Puppy.id == puppy_id).first()
    if operation.upper() == "EDIT":
        if request.method == "GET":
            return render_template("edit_puppy.html", puppy=pup)
        else:
            pup.breed = request.form["puppyBreed"]
            #my sample data seems to be saved in a different format than when creating new records from the web
            try:
                pup.dateOfBirth =  datetime.strptime(request.form["puppyDOB"], "%Y-%d-%m")
            except:
                pup.dateOfBirth =  datetime.strptime(request.form["puppyDOB"], "%Y-%m-%d")
            pup.description = request.form["puppyDescription"]
            pup.gender = request.form["puppyGender"]
            pup.name = request.form["puppyName"]
            #pup.pictureURL = "";
            session.commit()
            return redirect(url_for("shelter", shelter_id=pup.shelter_id))
    else:
        return "Not done yet"


@app.route("/shelter/<int:shelter_id>/createpuppy", methods=("GET", "POST"))
def createPuppy(shelter_id):
    if request.method == "GET":
        return render_template("create_puppy.html", shelter_id=shelter_id)
    else:
        """
        I'm not going to handle uploading the picture at the same time as creating a
        new puppy, because that would require:
        1) Upload image
        2) Associate the image with the puppy BEFORE saving
        3) Save the puppy
        I think i would need jQuery to be able to show the puppy image BEFORE saving
        """
        newPup = Puppy()
        newPup.breed = request.form["puppyBreed"]
        newPup.dateOfBirth =  datetime.strptime(request.form["puppyDOB"], "%Y-%d-%m")
        newPup.description = request.form["puppyDescription"]
        newPup.gender = request.form["puppyGender"]
        newPup.name = request.form["puppyName"]
        newPup.shelter_id = shelter_id
        newPup.pictureURL = "";
        session.add(newPup)
        session.commit()
        return redirect(url_for("shelter", shelter_id=shelter_id))


#TODO Found this in the documentation. perhaps use this to upload image for the puppy
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/imageupload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
#Debug

if __name__ == '__main__':
    app.secret_key = "super secret key"
    app.debug = True
    app.run(host='localhost', port=5000)