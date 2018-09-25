import uuid

from flask import Blueprint, request
from geoalchemy2.shape import from_shape
from pypnusershub import routes as fnauth
from shapely.geometry import Point, asShape

from geonature.utils.env import DB, get_module_id
from geonature.utils.errors import GeonatureApiError
from geonature.utils.utilssqlalchemy import json_resp
from .models import TPrograms, TOperations

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


@blueprint.route('/programs', methods=['POST'])
@fnauth.check_auth_cruved('C', False, id_app=ID_MODULE)
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


@blueprint.route('/operations/<int:id_ope>', methods=['GET'])
@json_resp
def get_operation(id_ope):
    operation = TOperations.query.get(id_ope)
    result = operation.as_dict()
    return result


@blueprint.route('/operations', methods=['POST'])
@fnauth.check_auth_cruved('C', True, id_app=ID_MODULE)
@json_resp
def post_operations(info_role):
    data = dict(request.get_json())

    if 'geometry' in data:
        geometry = data['geometry']
        data.pop('geometry')
    else:
        geometry = None

    data_operations = {}
    for field in data:
        if hasattr(TOperations, field):
            data_operations[field] = data[field]

    try:
        id_individual = data_operations['id_individual']
        try:
            ind_exists = DB.session.query(DB.exists().where(TIndividuals.id_individual == id_individual)).scalar()
        except:
            ind_exists = True
        if ind_exists:
            try:
                newoperation = TOperations(**data_operations)
            except Exception as e:
                print(e)
                raise GeonatureApiError('Cannot create operation')
        else:
            raise GeonatureApiError("Individual doesn't exists")
    except:
        raise GeonatureApiError("id_individual missing")

    if geometry:
        try:
            shape = asShape(geometry)
            newoperation.geom_point_4326 = from_shape(Point(shape), srid=4326)
        except:
            newoperation.geom_point_4326 = None

    newoperation.unique_id_sinp = uuid.uuid4()

    DB.session.add(newoperation)
    DB.session.commit()
    DB.session.flush()

    return newoperation.as_geofeature('geom_point_4326', 'id_operation')
