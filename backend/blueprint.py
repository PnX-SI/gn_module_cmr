from flask import Blueprint, request
from pypnusershub import routes as fnauth

from geonature.utils.env import DB
from geonature.utils.errors import GeonatureApiError
from geonature.utils.utilssqlalchemy import json_resp
from .models import TPrograms

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
@fnauth.check_auth_cruved('R', False, id_app=3) # TODO: Changer id_app par ID_MODULE
@json_resp
def post_programs():
    """ Ajout d'un programme (program name unique)"""
    data = dict(request.get_json())
    progname = data['program_name']
    if len(progname) >= 1:
        exists = DB.session.query(DB.exists().where(TPrograms.program_name == progname)).scalar()
        print('look4p', exists)
        if exists:
            raise GeonatureApiError('This program already exists')
        else:
            try:
                newprog = TPrograms(**data)
            except:
                raise GeonatureApiError('Cannot create program')
    else:
        raise GeonatureApiError('Program name empty')

    DB.session.add(newprog)
    DB.session.commit()
    DB.session.flush()
    return newprog.as_dict()
