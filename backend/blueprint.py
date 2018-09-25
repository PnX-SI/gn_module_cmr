from flask import Blueprint

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import json_resp
from .models import TPrograms, TIndividuals

blueprint = Blueprint('cmr', __name__)

@blueprint.route('/test', methods=['GET', 'POST'])
def test():
    return 'It works'

@blueprint.route('/programs', methods=['GET'])
@json_resp
def get_programs():
    pgs = DB.session.query(TPrograms).all()
    return [pg.as_dict() for pg in pgs]


@blueprint.route('/individuals', methods=['GET'])
@json_resp
def get_individuals():
    data = DB.session.query(TIndividuals).all()
    return [d.as_dict() for d in data]