from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "<h1> welcome to flask to school </h1>"

@app.route("/course")
def course():
    return "welcome to flask course"

@app.route("/<name>")
def name(name):
    return f"hello {name}!"

if __name__ == "__main__":
    app.run(debug = True)

