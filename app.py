#!/bin/env python3

"""
 Created by TyanBoot on 2017/10/19
 Tyan <tyanboot@outlook.com>

"""

from app import create_app

app = create_app()


if __name__ == '__main__':
    app.run()