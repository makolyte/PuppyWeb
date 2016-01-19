from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("startertemplate.html")

if __name__ == '__main__':
    app.secret_key = "super secret key"
    app.debug = True
    app.run(host='localhost', port=5000)