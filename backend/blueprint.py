from flask import Blueprint, request
from pypnusershub import routes as fnauth

from geonature.utils.env import DB, get_module_id
from geonature.utils.errors import GeonatureApiError
from geonature.utils.utilssqlalchemy import json_resp
from .models import TPrograms, TOperations, TIndividuals

blueprint = Blueprint('cmr', __name__)

try:
    ID_MODULE = get_module_id('cmr')
except Exception as e:
    ID_MODULE = 'Error'

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

@blueprint.route('/programs', methods=['POST'])
@fnauth.check_auth_cruved('R', False, id_app=ID_MODULE)
@json_resp
def post_programs():
    """ Ajout d'un programme (program name unique)"""
    data = dict(request.get_json())
    progname = data['program_name']
    if len(progname) >= 1:
        exists = DB.session.query(DB.exists().where(TPrograms.program_name == progname)).scalar()
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

@blueprint.route('/operations', methods=['GET'])
@json_resp
def get_operations():
    operations = DB.session.query(TOperations).all()
    result = [ope.as_dict() for ope in operations]
    return result
