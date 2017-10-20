from http import HTTPStatus

from sanic import Blueprint
from sanic.response import json, text

from database.neo4j.neomodel.posts import Posts
from database.neo4j.neomodel.media import Media
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

        posts = Posts().find(page, per_page, uid=uid, order_by=order_by)
        data = []

        for post in posts:
            __post = post.__dict__
            __post['author'] = post.author.get().__dict__
            data.append(__post)

        return json(data, __status.OK)

    if request.method == "POST":
        try:
            req = request.form
            # check if the post request has the file part
            if request.files:
                print(Media().upload(files=request.files))
            post_data = Posts(
                content=req.get("content"),
            ).save(user_id=req.get("user_id"))
            data = post_data.__dict__
            data['author'] = post_data.author.get().__dict__

            return json({
                "data": data,
                "message": "Success!"
            }, __status.OK)
        except (KeyError, LookupError) as error:
            return json(str(error), __status.BAD_REQUEST)
