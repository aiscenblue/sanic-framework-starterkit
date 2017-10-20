from sanic import Blueprint
from sanic.response import json
from http import HTTPStatus
from module import get_file_name

""" blueprint module for url handler """
module_name = get_file_name(__file__)
method = Blueprint(module_name, url_prefix='/')

""" http code status """
__status = HTTPStatus


@method.route("/", methods=['GET'])
async def index(requests):
    return json("Welcome to sanic!", __status.OK)
