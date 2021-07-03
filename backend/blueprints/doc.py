import json
from datetime import datetime
from flask import Blueprint, render_template
from backend.exceptions import NotFoundException

bp = Blueprint("public", __name__)

#####################################################################
# HELPER FUNCTIONS
#####################################################################


#####################################################################
# ROUTES
#####################################################################


@bp.route("/", defaults={"page": 'index.html'})
@bp.route("/<page>")
def get_page(page: str):
    if "/" in page:
        raise NotFoundException()
    import os
    print('#### ', os.getcwd())
    try:
        return render_template(page)
    except:
        raise NotFoundException()

