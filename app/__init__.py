# -*- coding: utf-8 -*-
"""
 Created by TyanBoot on 2017/10/19
 Tyan <tyanboot@outlook.com>

"""

from flask import Flask, make_response, jsonify
import psycopg2
from functools import wraps
from flask import g
from flask import request

db = psycopg2.connect("dbname=demo user=demo password=demo")
db.autocommit = True


def create_app():
    app = Flask(__name__)

    from app.user import user
    app.register_blueprint(user, url_prefix="/user")

    from app.comment import comment
    app.register_blueprint(comment, url_prefix="/comment")
    return app
