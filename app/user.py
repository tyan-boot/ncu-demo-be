# -*- coding: utf-8 -*-
"""
 Created by TyanBoot on 2017/10/19
 Tyan <tyanboot@outlook.com>

"""

from flask import Blueprint
from flask import request
from flask import jsonify
from app.utils import *

user = Blueprint("user", __name__)


@user.route("/register", methods=["POST"])
def register_user():
    req: dict = request.get_json(silent=True)
    if not req:
        return jsonify({
            "err": 1,
            "message": "invalid input"
        })

    username = req.get("username")
    password = req.get("password")

    if not all([username, password]):
        return jsonify({
            "err": 2,
            "message": "missing parameters"
        })

    if has_user(username):
        return jsonify({
            "err": 3,
            "message": "user has already exist"
        })

    token, uid = create_user(username, password)

    return jsonify({
        "err": 0,
        "message": "create succeeded",
        "token": token,
        "uid": uid
    })


@user.route("/token", methods=["POST"])
def login():
    req: dict = request.get_json(silent=True)
    if not req:
        return jsonify({
            "err": 1,
            "message": "invalid input"
        })

    username = req.get("username")
    password = req.get("password")

    if not all([username, password]):
        return jsonify({
            "err": 2,
            "message": "missing parameters"
        })

    token, uid = verify_user(username, password)

    if not token:
        return jsonify({
            "err": 3,
            "message": "username or password mismatch"
        })
    else:
        return jsonify({
            "err": 0,
            "message": "login succeeded",
            "token": token,
            "uid": uid
        })
