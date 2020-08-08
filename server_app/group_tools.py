from .auth_tools import login_required
from quart import g, jsonify
from data.model import *
from typing import Optional


@login_required
def get_group_of_user() -> Optional[Groups]:
    user: Users = g.user
    group: Groups = Groups.query.filter_by(id=user.group_id).first()
    return group
