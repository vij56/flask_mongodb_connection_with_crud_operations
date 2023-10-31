from flask import Flask
import os
from dotenv import load_dotenv
from .extensions import mongo

load_dotenv()


def create_app():
  app = Flask(__name__)
  app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
  mongo.init_app(app)
  return app
