from flask import Flask 
app = Flask(__name__)

from app import public_views
from app import admin_views