#Static and dynamic routing

from flask import Flask
app=Flask(__name__)


#Student data
Students = {
    "1":{"name":"Rakesh","class":10,"age":11},
    "2":{"name":"Srinu","class":11,"age":20},
    "3":{"name":"Sindhu","class":12,"age":23},
    "4":{"name":"usha","class":13,"age":22},
    "5":{"name":"Raji","class":14,"age":21},
    "6":{"name":"nanna","class":11,"age":45},
    "7":{"name":"amma","class":16,"age":43}
}


#Routes
#Home routes

@app.route("/")
def home():
    return "This is Student Managements"

# Student route
@app.route("/student")
def Allstudent():
    return Students

# get student 1 data
# @app.route("/students")
# def Allstudent1():
#     return Students["1"]
# # get student 2 data
# @app.route("/student/2")
# def Allstudent2():
#     return Students["2"]
# #get student 3 data
# @app.route("/student/3")
# def Allstudent3():
#     return Students["3"]


#dynamic routing
@app.route("/students/id>")
def Allstudent1(id):
    if id in Students:
        return Students[id]
    else:
        return "Students id not Found"


# get student data by class
@app.route("/students/<class_id>")
def Allstudents(class_id):
    result = {}
    for id in Students:
        if Students[id]["class"] == int==class_id:
            result[id] = Students[id]
    if result:
        return result
    else:
        return "Student class not found"
    


if __name__=="__main__":
    app.run(debug=True)