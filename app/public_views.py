from app import app 
from flask import render_template
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