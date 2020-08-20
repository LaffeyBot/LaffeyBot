from quart import Blueprint, request, jsonify, g
import datetime
from ..auth_tools import login_required
from data.model import *
from ..group_tools import get_group_of_user

group_blueprint = Blueprint(
    "group_v1",
    __name__,
    url_prefix='/v1/group'
)


@group_blueprint.route('/get_members', methods=['GET'])
@login_required
def get_members():
    """
    @api {get} /v1/group/get_members 获取公会成员信息
    @apiVersion 1.0.0
    @apiName get_members
    @apiGroup Groups

    @apiSuccess (回参) {String}     msg     为"Successful!"
    @apiSuccess (回参) {List}       data    公会成员列表

    @apiErrorExample {json} 参数不存在
        HTTP/1.1 400 Bad Request
        {"msg": "Parameter is missing", "code": 401}

    @apiErrorExample {json} 用户没有加入公会
        HTTP/1.1 403 Forbidden
        {"msg": "User is not in any group.", "code": 402}

    @apiErrorExample {json} 用户的公会不存在
        HTTP/1.1 403 Forbidden
        {"msg": "User's group not found.", "code": 403}

    """
    user: Users = g.user

    return jsonify({
        "msg": "Successful!"
    }), 200
