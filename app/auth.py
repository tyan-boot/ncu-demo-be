# -*- coding: utf-8 -*-
"""
 Created by TyanBoot on 2017/10/19
 Tyan <tyanboot@outlook.com>

"""
from functools import wraps

from flask import request, make_response, jsonify, g


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return make_response(jsonify({
                "err": 1,
                "message": "auth failed"
            }), 401)
        from app.utils import verify_token
        uid = verify_token(token)
        if not uid:
            return make_response(jsonify({
                "err": 1,
                "message": "auth failed"
            }), 401)
        else:
            g.uid = uid
        return func(*args, **kwargs)

    return wrapper
