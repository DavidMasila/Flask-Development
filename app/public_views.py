from flask import send_from_directory, abort
from app import app
from flask import render_template, request, redirect, jsonify, make_response
from datetime import datetime
import os
from werkzeug.utils import secure_filename

# custom template 1


@app.template_filter("clean_date")
def clean_date(dt):
    return dt.strftime("%d %b %Y")

# custome template 2


@app.template_filter("add_xyz")
def add_xyz(x):
    return x + " xyz"


@app.route("/")
def index():
    return render_template('/public/index.html')


@app.route("/about")
def about():
    return render_template('public/about.html')


@app.route("/jinja")
def jinja():

    cool = True
    my_name = "David"
    age = 30
    langs = ["Python", "JavsScript", "C", "Ruby"]
    friends = {
        "David": 26,
        "Masila": 42,
        "Mwendwa": 56
    }

    colors = {"red", "blue", "orange"}

    class GitRemote:
        def __init__(self, name, description, url):
            self.name = name
            self.descriprion = description
            self.url = url

        def pull(self):
            return f"Pulling repo {self.name}"

        def clone(self):
            return f"Cloninig into {self.url}"

    my_remote = GitRemote("Scorprog", "Committed",
                          "https://github.com/scorprog")

    def repeat(x, qty):
        return x*qty

    date = datetime.utcnow()

    my_html = "<h1>This is some HTML</h1>"

    suspicious = "<script>alert('You got hacked')</script>"

    return render_template('public/jinja.html',
                           my_name=my_name,
                           age=age, langs=langs,
                           friends=friends,
                           colors=colors,
                           my_remote=my_remote,
                           repeat=repeat, cool=cool,
                           date=date,
                           my_html=my_html,
                           suspicious=suspicious

                           )


@app.route("/access")
def access():
    return render_template("public/access.html")

## message flashing
 
from flask import flash

@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        req = request.form
        username = req['username']
        email = req.get('email')
        password = request.form.get('password')
        if len(password) < 10:
            flash("Password must be greater than 10 characters", "danger")
            return redirect(request.url)
        flash("Account created","success")
    return render_template("/public/sign_up.html")


# pseudo database

users = {
    "mitsuhiko": {
        "name": "Armin Ronachar",
        "bio": "Creator of flask framework",
        "twitter_handle": "@mitsuhiko",
        "password":"flask"
    },
    "gvanrossum": {
        "name": "Guido Van Rossum",
        "bio": "Creator of Python Programming Language",
        "twitter_handle": "@gvanossum",
        "password":"python"
    },
    "elonmusk": {
        "name": "Elon Musk",
        "bio": "technology, entrepreneur, investor and engineer",
        "twitter_handle": "@elonmusk",
        "password":"twitter"
    }
}


@app.route("/profile/<username>")
def profile(username):
    user = None
    if username in users:
        user = users[username]
    return render_template("public/profile.html", user=user, username=username)


@app.route("/json", methods=["POST", "GET"])
def json():
    if request.is_json:
        req = request.get_json()

        response = {
            "message": "Json received",
            "name": req.get('name')
        }

        res = make_response(jsonify(response), 200)

        return res
    else:
        res = make_response(jsonify({"message": "no JSON received"}), 400)
        return res


@app.route("/guestbook")
def guestbook():
    return render_template("/public/guestbook.html")


@app.route("/guestbook/create-entry", methods=["POST"])
def create_entry():

    req = request.get_json()
    print(req)
    res = make_response(jsonify({"message": "JSON RECEIVED"}), 200)
    return res

# Flask Query Strings


@app.route("/query")
def query():
    args = request.args
    for k, v in args.items():
        print(f"{k} : {v}")

    # if "foo" in args:
    #     foo = args.get('foo')
    # print(foo)
    return "Query Received", 200

# uploading fileswith flask


app.config["IMAGE_UPLOADS"] = "/home/masila/flask_development/app/static/img/uploads"
app.config['ALLOWED_IMAGE_EXTENSIONS'] = ["PNG", "JPG", "JPEG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024

# function that checks the extensions of the image name uploaded to the server.


def allowed_image(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config['ALLOWED_IMAGE_EXTENSIONS']:
        return True
    else:
        return False


def allowed_image_filesize(filesize):
    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if request.files:
            print(request.cookies)

            if not allowed_image_filesize(request.cookies.get('filesize')):
                print("File larger than 0.5MB")
                return redirect(request.url)

            image = request.files['image']

            # check whether image has a name
            if image.filename == '':
                print("Image must have a name")
                return redirect(request.url)

            # controlling image type
            # checking the file name not to be harmful
            if not allowed_image(image.filename):
                print("That image file format is not allowed")
                return redirect(request.url)
            else:
                filename = secure_filename(image.filename)
                # if we want to save the image on our app folders
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            print("Image saved")
            return redirect(request.url)

    return render_template("/public/upload_image.html")


"""
Converter types
string:
int:
float:
path:
uuid:
"""

app.config['CLIENT_IMAGES'] = '/home/masila/flask_development/app/static/client/img'
app.config['CLIENT_PDF'] = '/home/masila/flask_development/app/static/client/pdf'
app.config['CLIENT_CSV'] = '/home/masila/flask_development/app/static/client/csv'

@app.route("/get-image/<image_name>")
def get_image(image_name):
    try:
        return send_from_directory(
            app.config['CLIENT_IMAGES'], image_name, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route("/get-pdf/<pdf_name>")
def get_pdf(pdf_name):
    try:
        return send_from_directory(
            app.config['CLIENT_PDF'], pdf_name, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route("/get-csv/<csv_name>")
def get_csv(csv_name):
    try:
        return send_from_directory(
            app.config['CLIENT_CSV'], csv_name, as_attachment=True)
    except FileNotFoundError:
        abort(404)

## working with cookies
@app.route("/cookies")
def cookies():
    res = make_response("Cookies", 200)

    res.set_cookie("flavour",
                   value="chocolate chip",
                   max_age=10,
                   expires=None,
                   path=request.path,
                   domain=None,
                   secure=False,
                   httponly=False
                   )
    res.set_cookie("chocolate type","dark")
    res.set_cookie("company","scorprog")


    cookies = request.cookies
    print(cookies)
    print(cookies.get('company'))
    return res

## session object
from flask import session, url_for
@app.route("/sign-in", methods=["GET","POST"])
def signin():
    if request.method == "POST":
        req = request.form 

        username = req.get("username")
        password = req.get("password")

        if not username in users:
            print("Username not in users")
            return redirect(request.url)
        else:
            user = users[username]

        if not password in user.get("password"):
            print("password is incorrect")
            return redirect(request.url)
        else:
            session["username"] = username
            print("user added to session")
            return redirect(url_for("user"))
    return render_template("public/sign_in.html")

@app.route("/user")
def user():
    if session.get('username', None) is not None:
        username = session.get('username')
        user = users[username]
        return render_template("public/user.html", user=user)
    else:
        print("Username not found in session")
        return redirect(url_for("signin"))

@app.route("/sign-out")
def signout():
    session.pop('username', None)
    return redirect(url_for('signin'))