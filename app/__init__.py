from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from os import path

db = SQLAlchemy()

DB_NAME = "users.db"

