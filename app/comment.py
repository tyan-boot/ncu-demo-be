# -*- coding: utf-8 -*-
"""
 Created by TyanBoot on 2017/10/19
 Tyan <tyanboot@outlook.com>

"""
from flask import Blueprint, jsonify, make_response
from flask import request
from app.utils import *
from app.auth import login_required
from flask import g

comment = Blueprint("comment", __name__)


@comment.route("/")
@comment.route("")
def get_comments():
    args = request.args
    offset = args.get("offset", 0)
    limit = args.get("limit", 10)

    comments, total = get_all_comments(offset, limit)

    return jsonify({
        "err": 0,
        "message": "success",
        "comments": [
            {
                "id": c[0],
                "title": c[1],
                "content": c[2],
                "user": {
                    "id": c[3],
                    "name": get_username(c[3])
                },
                "create_at": c[4]
            }
            for c in comments
        ],
        "total": total
    })


@comment.route("/", methods=["POST"])
@comment.route("", methods=["POST"])
@login_required
def new_comment():
    req = request.get_json(silent=True)
    if not req:
        return make_response(jsonify({
            "err": 1,
            "message": "invalid body"
        }), 400)
    title = req.get("title")
    content = req.get("content")

    if not all([title, content]):
        return jsonify({
            "err": 1,
            "message": "missing parameters"
        })
    cid = create_comment(g.uid, title, content)

    return jsonify({
        "err": 0,
        "message": "comment succeeded",
        "cid": cid
    })


@comment.route("/<int:cid>", methods=["DELETE"])
@login_required
def delete_comment(cid):
    status = remove_comment(cid, g.uid)
    status_msg = {
        0: "delete succeeded",
        1: "not found",
        2: "permission denied"
    }
    status_code = {
        0: 200,
        1: 404,
        2: 403
    }

    return make_response(jsonify({
        "err": status,
        "message": status_msg[status]
    }), status_code[status])