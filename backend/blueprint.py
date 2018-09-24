from flask import Blueprint, request

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import json_resp
from .models import TPrograms
from pypnusershub import routes as fnauth

blueprint = Blueprint('cmr', __name__)

@blueprint.route('/test', methods=['GET', 'POST'])
def test():
    return 'It works'

@blueprint.route('/programs', methods=['GET'])
@json_resp
def get_programs():
    pgs = DB.session.query(TPrograms).all()
    return [pg.as_dict() for pg in pgs]

@blueprint.route('/programs', methods=['POST'])
@fnauth.check_auth_cruved('R', False, id_app=3)
@json_resp
def post_programs():
    """ Ajout d'un programme"""
    # TODO : Validation de la donnée
    data = dict(request.get_json())
    newprog = TPrograms(**data)
    DB.session.add(newprog)
    DB.session.commit()
    DB.session.flush()
    return newprog.as_dict()