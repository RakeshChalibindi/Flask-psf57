# Rendar template,redirect,forms,Request,HTTP Request methods

from flask import Flask,render_template,redirect,request
app=Flask(__name__)


#Student data
Students = {
    "1":{"name":"Rakesh","class":10,"age":11,"marks":30},
    "2":{"name":"Srinu","class":11,"age":20,"marks":44},
    "3":{"name":"Sindhu","class":12,"age":23,"marks":50},
    "4":{"name":"usha","class":13,"age":22,"marks":50},
    "5":{"name":"Raji","class":14,"age":21,"marks":55},
    "6":{"name":"nanna","class":11,"age":45,"marks":40},
    "7":{"name":"amma","class":16,"age":43,"marks":60}
}


#Routes
#Home routes

@app.route("/")
def home():
    return render_template("Home.html",username="ChalibindiRakesh")  # it is sused to exute the file.

# Student route
@app.route("/students")
def Allstudent():
    return render_template("students.html",students=Students)

# get student 1 data
@app.route("/students")
def Allstudent1():
    return Students["1"]

# # get student 2 data
# @app.route("/student/2")
# def Allstudent2():
#     return Students["2"]
# #get student 3 data
# @app.route("/student/3")
# def Allstudent3():
#     return Students["3"]


## Register student

@app.route("/student/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")



#dynamic routing
@app.route("/studentss1/id>")
def Allstudent33(id):
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