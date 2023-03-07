from app import app 
from flask import render_template, request, redirect, jsonify, make_response
from datetime import datetime

#custom template 1
@app.template_filter("clean_date")
def clean_date(dt):
    return dt.strftime("%d %b %Y")

#custome template 2
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
    langs = ["Python","JavsScript","C","Ruby"]
    friends = {
        "David":26,
        "Masila":42,
        "Mwendwa":56
    }

    colors = {"red","blue","orange"}

    class GitRemote:
        def __init__(self, name, description, url):
            self.name = name
            self.descriprion =  description
            self.url=url
        
        def pull(self):
            return f"Pulling repo {self.name}"
        
        def clone(self):
            return f"Cloninig into {self.url}"
        
    my_remote = GitRemote("Scorprog","Committed","https://github.com/scorprog")

    def repeat(x, qty):
        return x*qty
    
    date = datetime.utcnow()

    my_html = "<h1>This is some HTML</h1>"

    suspicious  = "<script>alert('You got hacked')</script>"

    return render_template('public/jinja.html',
                           my_name = my_name,
                           age=age, langs=langs,
                           friends=friends,
                           colors = colors,
                           my_remote = my_remote,
                           repeat=repeat, cool = cool,
                           date=date,
                           my_html = my_html,
                           suspicious = suspicious

                           )

@app.route("/access")
def access():
    return render_template("public/access.html")

@app.route("/sign-up", methods=["GET","POST"])
def sign_up():
    if request.method == "POST":
        req = request.form
        username =  req['username']
        email = req.get('email')
        password =  request.form.get('password')
        print(username, email, password)
        return redirect(request.url)
    return render_template("/public/sign_up.html")

#pseudo database
users = {
    "mitsuhiko" : {
        "name":"Armin Ronachar",
        "bio":"Creator of flask framework",
        "twitter_handle":"@mitsuhiko"
    },
    "gvanrossum": {
        "name":"Guido Van Rossum",
        "bio":"Creator of Python Programming Language",
        "twitter_handle":"@gvanossum"
    },
    "elonmusk": {
        "name":"Elon Musk",
        "bio":"technology, entrepreneur, investor and engineer",
        "twitter_handle":"@elonmusk"
    }
}

@app.route("/profile/<username>")
def profile(username):
    user = None
    if username in users:
        user = users[username]
    return render_template("public/profile.html", user=user, username = username)

@app.route("/json", methods=["POST"])
def json():
    if request.is_json:
        req = request.get_json()

        response = {
            "message":"Json received",
            "name":req.get('name')
        }

        res = make_response(jsonify(response), 200)

        return res
    else:
        res = make_response(jsonify({"message":"no JSON received"}), 400)
        return res
    
@app.route("/guestbook")
def guestbook():
    return render_template("/public/guestbook.html")

    
@app.route("/guestbook/create-entry", methods=["POST"])
def create_entry():

    req = request.get_json()
    print(req)
    res = make_response(jsonify({"message":"JSON RECEIVED"}), 200)
    return res

#Flask Query Strings
@app.route("/query")
def query():
    args = request.args
    for k, v in args.items():
        print(f"{k} : {v}")

    # if "foo" in args:
    #     foo = args.get('foo')
    # print(foo)
    return "Query Received", 200