import os
import sys

sys.path.append(os.getcwd())

from flask import Flask
from invoke import Collection

from app.config import Config
from tasks import db

app = Flask(__name__)
app.config.from_object(Config)

ns = Collection()
ns.add_collection(db)
ns.configure({
    'config': app.config,
})
