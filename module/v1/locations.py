from http import HTTPStatus

from sanic import Blueprint
from sanic.response import json

from database.neo4j.neomodel.locations import Locations
from module import get_file_name
from module.v1 import Constants

""" blueprint module for url handler """
module_name = get_file_name(__file__)
version = Constants().get_version()
method = Blueprint(module_name, url_prefix=version + module_name)

""" http code status """
__status = HTTPStatus


@method.route("/", methods=['GET', 'POST'])
async def index(request):
    if request.method == "GET":
        req = request.args
        page = int(req.get('page')) if req.get('page') else 0
        per_page = int(req.get('per_page')) if req.get('per_page') else 15
        uid = req.get('uid') or None
        order_by = req.get('order_by') or None
        return json(
            [location.__dict__ for location in Locations().find(page, per_page, uid=uid, order_by=order_by)],
            __status.OK
        )
