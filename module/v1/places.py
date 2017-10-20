from http import HTTPStatus

from sanic import Blueprint
from sanic.response import json, text

from database.neo4j.neomodel.places import Places
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

        places = Places().find(page, per_page, uid=uid, order_by=order_by)
        data = []

        for place in places:
            __place = place.__dict__
            __place['locations'] = place.locations.get().__dict__
            data.append(__place)

        return json(data)
