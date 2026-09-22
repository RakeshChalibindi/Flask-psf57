from flask import (
    Flask,
    request,
    redirect,
    render_template,
    url_for,
    session,
    flash,
    send_from_directory
)

from database import (
    CreateTables,
    getUserByEmail,
    insertUserRecord,
    insertNotesRecord,
    getNotesByUserid,
    getNotesByNotesid,
    updateNotesRecord,
    deleteNotesRecord,
    insertFileRecord,
    getFileByUserID,
    updateUserPassword
)

import random
import os
import secrets
import time
from utils import sendEmail
from EmailTemplates import EmailTemplates
from utils import generateHashPassword, verifyHashPassword

from werkzeug.utils import secure_filename


# ======================================================
#                  Flask Application
# ======================================================

app = Flask(__name__)

app.secret_key = "Rakesh@123"


# ======================================================
#                  File Upload Configuration
# ======================================================

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Allowed file extensions
ALLOWED_EXTENSIONS = {
    "pdf",
    "png",
    "jpg",
    "jpeg",
    "doc",
    "docx",
    "txt",
    "xlsx",
    "csv"
}


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ======================================================
#                     Home
# ======================================================

@app.route("/")
def home():

    return render_template("home.html")


# ======================================================
#                     Register
# ======================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":

        return render_template("register.html")

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    conform_password = request.form.get("conformpassword")

    # Check empty fields
    if not username or not email or not password or not conform_password:

        flash("All fields are required", "err")

        return redirect(url_for("register"))

    # Check password
    if password != conform_password:

        flash("Password mismatch", "err")

        return redirect(url_for("register"))

    # Check whether email already exists
    if getUserByEmail(email=email):

        # Generate OTP
        OTP = random.randint(1000, 9999)

        # Store registration information in session
        session["otp"] = OTP
        session["username"] = username
        session["email"] = email
        session["password"] = password

        # Send OTP
        status, msg = sendEmail(
            to_email=email,
            subject="SNS - OTP Verification for Registration",
            body=EmailTemplates.OTPEmailTemplate(
                username=username,
                otp=OTP
            )
        )

        if status:

            flash("OTP sent to registered email", "msg")

            return redirect(url_for("verifyOTP"))

        else:

            flash(msg, "err")

            return redirect(url_for("register"))

    else:

        flash("Email already exists", "err")

        return redirect(url_for("register"))


# ======================================================
#                     Verify OTP
# ======================================================

@app.route("/verify-otp", methods=["GET", "POST"])
def verifyOTP():

    if "otp" not in session:

        return redirect(url_for("register"))

    if request.method == "GET":

        return render_template("verifyotp.html")

    otp_value = request.form.get("otp")

    if not otp_value:

        flash("Enter OTP", "err")

        return redirect(url_for("verifyOTP"))

    try:

        otp = int(otp_value)

    except ValueError:

        flash("OTP must contain numbers", "err")

        return redirect(url_for("verifyOTP"))

    if otp == session["otp"]:

        hash_password = generateHashPassword(
            password=session["password"]
        )

        status, msg = insertUserRecord(
            name=session["username"],
            email=session["email"],
            hash_pasword=hash_password
        )

        if status:

            # Remove registration information
            session.pop("otp", None)
            session.pop("username", None)
            session.pop("email", None)
            session.pop("password", None)

            flash("Registered successfully", "msg")

            return redirect(url_for("login"))

        else:

            flash(msg, "err")

            return redirect(url_for("verifyOTP"))

    else:

        flash("Enter valid OTP", "err")

        return redirect(url_for("verifyOTP"))


# ======================================================
#                     Login
# ======================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":

        return render_template("login.html")

    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:

        flash("Email and password are required", "err")

        return redirect(url_for("login"))

    status, data = getUserByEmail(
        email=email,
        data=True
    )

    if status is False:

        flash(data, "err")

        return redirect(url_for("login"))

    hash_password = data["HASHPASSWORD"]

    # Verify password
    if verifyHashPassword(password, hash_password):

        session.clear()

        session["USERID"] = data["USERID"]
        session["USERNAME"] = data["USERNAME"]
        session["EMAIL"] = data["EMAIL"]

        flash(
            f"Hello {data['USERNAME']}, Welcome to SNS Management",
            "msg"
        )

        return redirect(url_for("dashboard"))

    flash("Check your password", "err")

    return redirect(url_for("login"))

# ======================================================
#                  Forgot Password
# ======================================================

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "GET":
        return render_template("forgotpassword.html")

    email = request.form.get("email")

    if not email:
        flash("Please enter your email", "err")
        return redirect(url_for("forgot_password"))

    # Check email
    status, data = getUserByEmail(
        email=email,
        data=True
    )

    if status is False:
        flash("Email is not registered", "err")
        return redirect(url_for("forgot_password"))

    # Generate secure token
    token = secrets.token_urlsafe(32)

    # Store token in session
    session["reset_token"] = token
    session["reset_email"] = email

    # Create reset link
    reset_link = url_for(
        "reset_password",
        token=token,
        _external=True
    )

    # Email content
    body = f"""
    Hello {data["USERNAME"]},

    We received a request to reset your SNS password.

    Click the link below to reset your password:

    {reset_link}

    If you did not request a password reset,
    you can ignore this email.

    Thank you,
    SNS Management System
    """

    status, message = sendEmail(
        to_email=email,
        subject="SNS - Password Reset Link",
        body=body
    )

    if status:

        flash(
            "Password reset link sent to your email",
            "msg"
        )

        return redirect(
            url_for("login")
        )

    flash(
        message,
        "err"
    )

    return redirect(
        url_for("forgot_password")
    )

# ======================================================
#                     Notes Management
# ======================================================

@app.route("/notes")
def mynotes():

    if "USERID" not in session:

        flash("Please login first", "err")

        return redirect(url_for("login"))

    status, notes = getNotesByUserid(
        userid=session["USERID"]
    )

    if status:

        return render_template(
            "notes.html",
            notes=notes
        )

    flash(notes, "err")

    return redirect(url_for("dashboard"))

# ======================================================
#                  Reset Password
# ======================================================

@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):

    # Check reset token
    if "reset_token" not in session:
        flash("Invalid or expired reset link", "err")
        return redirect(url_for("forgot_password"))

    # Check token
    if token != session["reset_token"]:
        flash("Invalid reset link", "err")
        return redirect(url_for("forgot_password"))

    # GET request
    if request.method == "GET":
        return render_template("resetpassword.html")

    # POST request
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    # Check fields
    if not password or not confirm_password:
        flash("All fields are required", "err")
        return redirect(
            url_for("reset_password", token=token)
        )

    # Check passwords
    if password != confirm_password:
        flash("Passwords do not match", "err")
        return redirect(
            url_for("reset_password", token=token)
        )

    # Create password hash
    hash_password = generateHashPassword(
        password=password
    )

    # Get email
    email = session["reset_email"]

    # Update password
    status, message = updateUserPassword(
        email=email,
        hash_password=hash_password
    )

    if status:

        session.pop("reset_token", None)
        session.pop("reset_email", None)

        flash(
            "Password updated successfully",
            "msg"
        )

        return redirect(url_for("login"))

    flash(message, "err")

    return redirect(
        url_for(
            "reset_password",
            token=token
        )
    )
# ======================================================
#                     Add Note
# ======================================================

@app.route("/notes/addnotes", methods=["GET", "POST"])
def add_notes():

    if "USERID" not in session:

        flash("Please login first", "err")

        return redirect(url_for("login"))

    if request.method == "GET":

        return render_template("addnotes.html")

    title = request.form.get("title")
    content = request.form.get("content")

    if not title or not content:

        flash("Title and Content are required", "err")

        return render_template("addnotes.html")

    status, message = insertNotesRecord(
        userid=session["USERID"],
        title=title,
        content=content
    )

    if status:

        flash("Note Saved Successfully", "msg")

        return redirect(url_for("mynotes"))

    flash(message, "err")

    return render_template("addnotes.html")


# ======================================================
#                     View Note
# ======================================================

@app.route("/notes/view/<int:notesid>")
def viewnotes(notesid):

    if "USERID" not in session:

        flash("Please login first", "err")

        return redirect(url_for("login"))

    status, note = getNotesByNotesid(
        notesid=notesid
    )

    if status and note:

        return render_template(
            "viewnotes.html",
            title=note["TITLE"],
            content=note["CONTENT"],
            notesid=notesid
        )

    flash("Note not found", "err")

    return redirect(url_for("mynotes"))


# ======================================================
#                     Edit Note
# ======================================================

@app.route(
    "/notes/edit/<int:notesid>",
    methods=["GET", "POST"]
)
def edit_notes(notesid):

    if "USERID" not in session:

        flash("Please login first", "err")

        return redirect(url_for("login"))

    if request.method == "GET":

        status, note = getNotesByNotesid(
            notesid=notesid
        )

        if status and note:

            return render_template(
                "editnotes.html",
                notesid=notesid,
                title=note["TITLE"],
                content=note["CONTENT"]
            )

        flash("Note not found", "err")

        return redirect(url_for("mynotes"))

    title = request.form.get("title")
    content = request.form.get("content")

    if not title or not content:

        flash(
            "Title and Content are required",
            "err"
        )

        return redirect(
            url_for(
                "edit_notes",
                notesid=notesid
            )
        )

    status, message = updateNotesRecord(
        notesid=notesid,
        userid=session["USERID"],
        title=title,
        content=content
    )

    if status:

        flash(
            "Note Updated Successfully",
            "msg"
        )

    else:

        flash(message, "err")

    return redirect(url_for("mynotes"))


# ======================================================
#                     Delete Note
# ======================================================

@app.route("/notes/delete/<int:notesid>")
def delete_notes(notesid):

    if "USERID" not in session:

        flash("Please login first", "err")

        return redirect(url_for("login"))

    status, message = deleteNotesRecord(
        notesid=notesid,
        userid=session["USERID"]
    )

    if status:

        flash(
            "Note Deleted Successfully",
            "msg"
        )

    else:

        flash(message, "err")

    return redirect(url_for("mynotes"))


# ======================================================
#                  User File Folder
# ======================================================

def get_user_upload_folder():

    user_id = str(session["USERID"])

    user_folder = os.path.join(
        app.config["UPLOAD_FOLDER"],
        user_id
    )

    os.makedirs(
        user_folder,
        exist_ok=True
    )

    return user_folder


# ======================================================
#                  Upload / My Files
# ======================================================

@app.route("/files", methods=["GET", "POST"])
def myfiles():

    if "USERID" not in session:

        flash("Please login first", "err")

        return redirect(url_for("login"))

    userid = session["USERID"]

    user_folder = get_user_upload_folder()

    # ---------------- POST / UPLOAD ----------------

    if request.method == "POST":

        if "file" not in request.files:

            flash(
                "File field not found",
                "err"
            )

            return redirect(url_for("myfiles"))

        file = request.files["file"]

        if file.filename == "":

            flash(
                "Please select a file",
                "err"
            )

            return redirect(url_for("myfiles"))

        # Check extension
        if not allowed_file(file.filename):

            flash(
                "File type not allowed",
                "err"
            )

            return redirect(url_for("myfiles"))

        # Original filename
        originalname = file.filename

        # Safe filename
        storedname = secure_filename(
            file.filename
        )

        if not storedname:

            flash(
                "Invalid file name",
                "err"
            )

            return redirect(url_for("myfiles"))

        # Physical file path
        file_path = os.path.join(
            user_folder,
            storedname
        )

        # Check duplicate
        if os.path.exists(file_path):

            flash(
                "File already exists",
                "err"
            )

            return redirect(url_for("myfiles"))

        try:

            # Save physical file
            file.save(file_path)

            # Get file size
            file_size = os.path.getsize(
                file_path
            )

            # Get MIME type
            mimetype = file.content_type

            # Save file information into database
            status, message = insertFileRecord(
                userid=userid,
                originalname=originalname,
                storedname=storedname,
                mimetype=mimetype,
                size=file_size,
                filepath=file_path
            )

            print(
                "DATABASE STATUS:",
                status
            )

            print(
                "DATABASE MESSAGE:",
                message
            )

            if status:

                flash(
                    "File uploaded successfully!",
                    "msg"
                )

            else:

                # If database insert fails,
                # remove physical file
                if os.path.exists(file_path):

                    os.remove(file_path)

                flash(
                    message,
                    "err"
                )

        except Exception as e:

            # Remove file if error happens
            if os.path.exists(file_path):

                os.remove(file_path)

            flash(
                f"Upload Error: {e}",
                "err"
            )

        return redirect(
            url_for("myfiles")
        )

    # ---------------- GET / SHOW FILES ----------------

    try:

        files = os.listdir(user_folder)

    except Exception as e:

        flash(
            f"File list error: {e}",
            "err"
        )

        files = []

    return render_template(
        "files.html",
        files=files,
        search_text=""
    )


# ======================================================
#                     Search Files
# ======================================================

@app.route("/files/search")
def search_files():

    if "USERID" not in session:

        flash(
            "Please login first",
            "err"
        )

        return redirect(url_for("login"))

    search_text = request.args.get(
        "q",
        ""
    ).strip()

    user_folder = get_user_upload_folder()

    try:

        files = os.listdir(user_folder)

    except Exception:

        files = []

    # Search filename
    if search_text:

        files = [
            file
            for file in files
            if search_text.lower()
            in file.lower()
        ]

    return render_template(
        "files.html",
        files=files,
        search_text=search_text
    )


# ======================================================
#                     View File
# ======================================================

@app.route("/files/view/<filename>")
def view_file(filename):

    if "USERID" not in session:

        flash(
            "Please login first",
            "err"
        )

        return redirect(url_for("login"))

    filename = secure_filename(filename)

    user_folder = get_user_upload_folder()

    file_path = os.path.join(
        user_folder,
        filename
    )

    if not os.path.isfile(file_path):

        flash(
            "File not found",
            "err"
        )

        return redirect(
            url_for("myfiles")
        )

    return send_from_directory(
        user_folder,
        filename,
        as_attachment=False
    )


# ======================================================
#                     Download File
# ======================================================

@app.route("/files/download/<filename>")
def download_file(filename):

    if "USERID" not in session:

        flash(
            "Please login first",
            "err"
        )

        return redirect(url_for("login"))

    filename = secure_filename(filename)

    user_folder = get_user_upload_folder()

    file_path = os.path.join(
        user_folder,
        filename
    )

    if not os.path.isfile(file_path):

        flash(
            "File not found",
            "err"
        )

        return redirect(
            url_for("myfiles")
        )

    return send_from_directory(
        user_folder,
        filename,
        as_attachment=True
    )


# ======================================================
#                     Edit File
# ======================================================

@app.route(
    "/files/edit/<filename>",
    methods=["GET", "POST"]
)
def edit_file(filename):

    if "USERID" not in session:

        flash(
            "Please login first",
            "err"
        )

        return redirect(url_for("login"))

    old_filename = secure_filename(
        filename
    )

    user_folder = get_user_upload_folder()

    old_path = os.path.join(
        user_folder,
        old_filename
    )

    if not os.path.isfile(old_path):

        flash(
            "File not found",
            "err"
        )

        return redirect(
            url_for("myfiles")
        )

    # GET
    if request.method == "GET":

        return render_template(
            "editfile.html",
            filename=old_filename
        )

    # POST
    new_filename = request.form.get(
        "filename"
    )

    if not new_filename:

        flash(
            "File name is required",
            "err"
        )

        return redirect(
            url_for(
                "edit_file",
                filename=old_filename
            )
        )

    new_filename = secure_filename(
        new_filename
    )

    if not new_filename:

        flash(
            "Invalid file name",
            "err"
        )

        return redirect(
            url_for(
                "edit_file",
                filename=old_filename
            )
        )

    # Check extension
    if not allowed_file(new_filename):

        flash(
            "File type not allowed",
            "err"
        )

        return redirect(
            url_for(
                "edit_file",
                filename=old_filename
            )
        )

    new_path = os.path.join(
        user_folder,
        new_filename
    )

    # Same name
    if old_filename == new_filename:

        flash(
            "File name is same",
            "err"
        )

        return redirect(
            url_for("myfiles")
        )

    # Duplicate
    if os.path.exists(new_path):

        flash(
            "A file with this name already exists",
            "err"
        )

        return redirect(
            url_for(
                "edit_file",
                filename=old_filename
            )
        )

    try:

        os.rename(
            old_path,
            new_path
        )

        flash(
            "File updated successfully!",
            "msg"
        )

    except Exception as e:

        flash(
            f"Rename error: {e}",
            "err"
        )

    return redirect(
        url_for("myfiles")
    )


# ======================================================
#                     Delete File
# ======================================================

@app.route("/files/delete/<filename>")
def delete_file(filename):

    if "USERID" not in session:

        flash(
            "Please login first",
            "err"
        )

        return redirect(url_for("login"))

    filename = secure_filename(
        filename
    )

    user_folder = get_user_upload_folder()

    file_path = os.path.join(
        user_folder,
        filename
    )

    if not os.path.isfile(file_path):

        flash(
            "File not found",
            "err"
        )

        return redirect(
            url_for("myfiles")
        )

    try:

        os.remove(file_path)

        flash(
            "File deleted successfully!",
            "msg"
        )

    except Exception as e:

        flash(
            f"Delete error: {e}",
            "err"
        )

    return redirect(
        url_for("myfiles")
    )


# ======================================================
#                     Profile
# ======================================================

@app.route("/profile")
def profile():

    if "USERID" not in session:

        flash(
            "Please login first",
            "err"
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "profile.html",
        username=session["USERNAME"],
        email=session["EMAIL"]
    )


# ======================================================
#                     Logout
# ======================================================

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "Logged out successfully",
        "msg"
    )

    return redirect(
        url_for("login")
    )

# ======================================================
#                     Main
# ======================================================

if __name__ == "__main__":

    print(CreateTables())

    app.run(
        debug=True,
        port=8000
    )