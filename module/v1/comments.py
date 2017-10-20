from http import HTTPStatus

from sanic import Blueprint
from sanic.response import json, text

from database.neo4j.neomodel.comments import Comments
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

        comments = Comments().find(page, per_page, uid=uid, order_by=order_by)
        __data = []

        for comment in comments:
            __comment = comment.__dict__
            __post_author = comment.post.get().author.get().__dict__
            __comment['author'] = comment.author.get().__dict__
            __comment['post'] = comment.post.get().__dict__
            __comment['post']['author'] = __post_author
            __data.append(__comment)

        return json(__data, __status.OK)

    if request.method == "POST":
        try:
            req = request.form or request.json or request.args
            post_data = Comments(
                content=req.get("content"),
            ).save(user_id=req.get("user_id"), post_id=req.get("post_id"))
            __data = post_data.__dict__
            __post_author = post_data.post.get().author.get().__dict__
            __data['author'] = post_data.author.get().__dict__
            __data['post'] = post_data.post.get().__dict__
            __data['post']['author'] = __post_author

            return json({
                "data": __data,
                "message": "Success!"
            }, __status.OK)
        except (KeyError, LookupError) as error:
            return json(str(error), __status.BAD_REQUEST)
