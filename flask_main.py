from flask import Flask, render_template
from database_setup import Base, Puppy, Shelter, Owner, create_engine
from sqlalchemy.orm import sessionmaker

class TestData():
    def __init__(self, image, name, age, weight):
        self.image = image
        self.name = name
        self.age = age
        self.weight  = weight


engine = create_engine("sqlite:///puppyweb.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

@app.route("/")
@app.route("/puppies")
def homepage():
    puppies = session.query(Puppy).all()
    return render_template("puppies.html", puppies=puppies)


@app.route("/test")
def test():
    placeholder = "http://placehold.it/300x300"
    testData = []
    testData.append(TestData(image=placeholder, name="Test1", age=1, weight=10))
    testData.append(TestData(image=placeholder, name="Test2", age=2, weight=13))
    testData.append(TestData(image=placeholder, name="Test3", age=3, weight=16))
    testData.append(TestData(image=placeholder, name="Test4", age=4, weight=19))
    testData.append(TestData(image=placeholder, name="Test5", age=5, weight=22))
    testData.append(TestData(image=placeholder, name="Test6", age=6, weight=25))
    return render_template("test.html", testData = testData)

if __name__ == '__main__':
    app.secret_key = "super secret key"
    app.debug = True
    app.run(host='localhost', port=5000)