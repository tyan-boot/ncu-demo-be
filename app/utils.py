# -*- coding: utf-8 -*-
"""
 Created by TyanBoot on 2017/10/19
 Tyan <tyanboot@outlook.com>

"""
from datetime import datetime

from itsdangerous import TimedJSONWebSignatureSerializer

from app import db


def has_user(username):
    """
     检查是否已存在用户
    :param username: 用户名
    :return: boolean
    """
    with db.cursor() as cur:
        cur.execute("SELECT id FROM users WHERE name = %s", (username,))
        result = cur.rowcount
        return result != 0


def create_user(username, password):
    """
    创建用户
    :param username: 用户名
    :param password: 密码
    :return: token: str
    """
    try:

        with db.cursor() as cur:
            cur.execute("INSERT INTO users VALUES (crypt(%s, gen_salt('md5')), %s, %s) RETURNING id",
                        (password, datetime.now(), username))
            uid = cur.fetchone()[0]
        return generate_token(uid, username), uid
    except Exception as e:
        db.rollback()
        return None


def verify_user(username, password):
    """
    验证用户
    :param username:
    :param password:
    :return: boolean
    """
    with db.cursor() as cur:
        cur.execute("SELECT id FROM users WHERE password=crypt(%s, password) AND name=%s", (password, username))
        if cur.rowcount == 0:
            return False
        else:
            return generate_token(cur.fetchone()[0], username)


def generate_token(uid, username):
    """
    生成jwt token
    :param uid: 用户id
    :param username: 用户名
    :return: token or None
    """
    s = TimedJSONWebSignatureSerializer(secret_key="demo")
    try:
        return s.dumps({
            "id": uid,
            "username": username
        }).decode("ascii")
    except Exception as e:
        print(e)
        return None


def verify_token(token):
    """
    验证token是否合法
    :param token: token
    :return: 用户id
    """
    s = TimedJSONWebSignatureSerializer(secret_key="demo")
    try:
        message = s.loads(token)
        return message["id"]
    except:
        return None


def get_all_comments(offset=0, limit=10):
    """
    获取全部留言
    :param offset: 起始id
    :param limit: 一次返回限制
    :return:
    """
    with db.cursor() as cur:
        cur.execute("SELECT * FROM comments OFFSET %s LIMIT %s", (offset, limit))
        comments = cur.fetchall()
        cur.execute("SELECT count(1) FROM comments")
        total = cur.fetchone()[0]

    return comments, total


def create_comment(uid, title, content):
    """
    新建一个留言
    :param title: 标题
    :param content: 内容
    :return:
    """

    with db.cursor() as cur:
        cur.execute("INSERT INTO comments (title, content, user_id, create_at) VALUES (%s, %s, %s, %s) RETURNING id",
                    (title, content, uid, datetime.now()))
        return cur.fetchone()[0]


def get_comment(cid):
    with db.cursor() as cur:
        cur.execute("SELECT * FROM comments WHERE id = %s", (cid,))
        if cur.rowcount == 0:
            return None
        else:
            c = cur.fetchone()
            return {
                "id": c[0],
                "title": c[1],
                "content": c[2],
                "user": {
                    "id": c[3],
                    "name": get_username(c[3])
                },
                "create_at": c[4]
            }


def remove_comment(cid, uid):
    """
    删除一条留言
    :param cid: 待删除的留言id
    :param uid: 发起删除操作的用户id
    :return:
    """
    with db.cursor() as cur:
        cur.execute("SELECT id, user_id FROM comments WHERE id = %s", (cid,))
        if cur.rowcount == 0:
            return 1
        else:
            _, user_id = cur.fetchone()
            # 判断留言是否是自己的
            if user_id != uid:
                return 2
            else:
                cur.execute("DELETE FROM comments WHERE id = %s", (cid,))
                return 0


def get_username(uid):
    """
    获取用户名
    :param uid:
    :return:
    """
    with db.cursor() as cur:
        cur.execute("SELECT name FROM users WHERE id=%s", (uid,))
        return cur.fetchone()[0]
