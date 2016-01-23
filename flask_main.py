from flask import Flask, render_template
from database_setup import Base, Puppy, Shelter, Owner, create_engine
from sqlalchemy.orm import sessionmaker


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
    #TODO - Create shelter profile
    return "TODO - Create shelter profile"

@app.route("/shelter/<int:shelter_id>/edit", methods=("GET", "POST"))
def editShelter(shelter_id):
    #TODO - Create edit
    return "TODO - Create edit"

@app.route("/shelter/<int:shelter_id>/delete", methods=("GET", "POST"))
def deleteShelter(shelter_id):
    #TODO - Create delete
    return "TODO - Create delete"

@app.route("/createShelter")
def createShelter():
    #TODO: Create shelter
    return "TODO-Create shelter"

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