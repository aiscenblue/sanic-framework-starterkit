import random
import string
import weakref
from http import HTTPStatus

import jwt
from sanic import Blueprint
from sanic.response import json

from database.neo4j.neomodel.users import Users
from module import get_file_name
from module.v1 import Constants

""" blueprint module for url handler """
module_name = get_file_name(__file__)
version = Constants().get_version()
method = Blueprint(module_name, url_prefix=version + module_name)

""" http code status """
__status = HTTPStatus


@method.route("/py2neo", methods=['GET', 'POST'])
async def user_index_py2neo(request):
    if request.method == "GET":
        from database.neo4j.py2neo.users import Users
        return json(Users().list())


@method.route("/", methods=['GET', 'POST'])
async def user_index(request):
    if request.method == "GET":
        try:
            req = request.args
            page = int(req.get('page')) if req.get('page') else 0
            per_page = int(req.get('per_page')) if req.get('per_page') else 15
            uid = req.get('uid') or None
            order_by = req.get('order_by') or None
            users = Users().find(page, per_page, uid=uid, order_by=order_by)

            return json([user.__dict__ for user in users], __status.OK)

        except (KeyError, LookupError, ValueError) as error:
            return json(str(error), __status.BAD_REQUEST)

    if request.method == "POST":
        try:
            req = request.form
            user_data = Users(
                firstname=req.get("firstname"),
                lastname=req.get("lastname"),
                email=req.get("email"),
                password=req.get("password")
            ).save()

            del user_data.__dict__["password"]
            user_data.__dict__["created_at"] = str(user_data.__dict__["created_at"])
            user_data.__dict__["updated_at"] = str(user_data.__dict__["updated_at"])
            secret_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(50))
            encoded_jwt = jwt.encode(user_data.__dict__, secret_key, algorithm='HS256')

            return json({
                "data": user_data.__dict__,
                "secret_key": secret_key,
                "access_token": encoded_jwt,
                "message": "Successfully created!"
            }, __status.OK)

        except (KeyError, LookupError, ValueError) as error:
            return json(str(error), __status.BAD_REQUEST)
        except TypeError:
            return json("Missing parameter.", __status.BAD_REQUEST)


@method.route("/authenticate", methods=['POST'])
async def user_authenticate(request):
    try:
        req = request.form
        users = Users(email=req.get("email"), password=req.get("password")).authenticate()
        user_ref = weakref.ref(users)

        del user_ref().__dict__["password"]
        secret_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(50))
        encoded_jwt = jwt.encode(user_ref().__dict__, secret_key, algorithm='HS256')

        return json({"data": user_ref().__dict__, "secret_key": secret_key, "access_token": encoded_jwt}, __status.OK)
    except (PermissionError, LookupError, ValueError) as error:
        return json(str(error), __status.BAD_REQUEST)
