from flask import Blueprint, request

from geonature.utils.errors import GeonatureApiError
from geonature.utils.env import DB, get_module_id
from geonature.utils.utilssqlalchemy import json_resp

from pypnusershub import routes as fnauth

from .models import TPrograms

blueprint = Blueprint('cmr', __name__)

try:
    ID_MODULE = get_module_id('cmr')
except Exception as e:
    ID_MODULE = 'Error'

@blueprint.route('/test', methods=['GET', 'POST'])
def test():
    return 'It works'

@blueprint.route('/programs', methods=['GET'])
@fnauth.check_auth_cruved('R', False, id_app=ID_MODULE)
@json_resp
def get_programs():
    pgs = DB.session.query(TPrograms).all()
    return [pg.as_dict() for pg in pgs]

@blueprint.route('/programs/<int:id_program>', methods=['GET'])
@fnauth.check_auth_cruved('R', False, id_app=ID_MODULE)
@json_resp
def get_program_by_id(id_program):
    pg = (DB.session.query(TPrograms)
        .filter(TPrograms.id_program == id_program)
        .one()
    )
    return pg.as_dict()

@blueprint.route('/programs', methods=['POST'])
@blueprint.route('/programs/<int:id_program>', methods=['POST'])
@fnauth.check_auth_cruved('C', False, id_app=ID_MODULE)
@json_resp
def post_programs(id_program = None):
    """ 
        Ajout d'un programme (program name unique)
    """
    data = dict(request.get_json())
    program = data['program_name']
    
    newpg = TPrograms(**data)

    exists = (
        DB.session.query(TPrograms)
        .filter(TPrograms.program_name == program)
        .all()
    )
    if exists:
        if not exists[0].id_program == id_program :
            raise GeonatureApiError('This program already exists')

    if newpg.id_program:
        DB.session.merge(newpg)
    else:
        DB.session.add(newpg)

    try:
        DB.session.commit()
    except:
        raise GeonatureApiError('Cannot create program')
    
    return newpg.as_dict(True)