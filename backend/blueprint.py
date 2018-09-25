import uuid

from flask import Blueprint, request
from geoalchemy2.shape import from_shape
from geojson import FeatureCollection
from pypnusershub import routes as fnauth
from shapely.geometry import Point, asShape


from geonature.utils.errors import GeonatureApiError
from geonature.utils.env import DB, get_module_id
from geonature.utils.utilssqlalchemy import json_resp
from .models import TPrograms, TOperations, TIndividuals, Taxonomie

from pypnnomenclature.models import TNomenclatures


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


@blueprint.route('/operations', methods=['GET'])
@json_resp
def get_operations():
    operations = DB.session.query(TOperations).all()
    result = FeatureCollection([ope.get_geofeature() for ope in operations])
    return result


@blueprint.route('/operations/<int:id_ope>', methods=['GET'])
@json_resp
def get_operation(id_ope):
    operation = TOperations.query.get(id_ope)
    # result = operation.as_dict()
    return operation.get_geofeature()




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

    return newoperation.get_geofeature()


@blueprint.route('/nomenclature_display/<int:id_nomenclature>', methods=['GET'])
@json_resp
def get_nomenclature_label(id_nomenclature):

    try:
        data = DB.session.query(TNomenclatures).filter(TNomenclatures.id_nomenclature == id_nomenclature).first()
    except:
        raise GeonatureApiError("Erreur id_nomenclature")

    return data.as_dict()


@blueprint.route('/individuals', methods=['GET'])
@blueprint.route('/individuals/<id_individual>', methods=['GET'])
@json_resp
def get_individuals(id_individual=None):
    if id_individual is None:
        q = DB.session.query(TIndividuals, Taxonomie.nom_complet, Taxonomie.nom_vern, TNomenclatures.mnemonique).join(
            Taxonomie, Taxonomie.cd_nom == TIndividuals.cd_nom).join(
                TNomenclatures, TNomenclatures.id_nomenclature == TIndividuals.id_nomenclature_sex)
        data = q.all()
        res = []
        for ind, nom_complet, nom_vern, sex in data:
            d = ind.as_dict()
            d.update({'nom_complet': nom_complet, 'nom_vern': nom_vern, 'sexe': sex})
            res.append(d)
    else:
        q = DB.session.query(TIndividuals, Taxonomie.nom_complet, Taxonomie.nom_vern, TNomenclatures.mnemonique).join(
            Taxonomie, Taxonomie.cd_nom == TIndividuals.cd_nom).join(
                TNomenclatures, TNomenclatures.id_nomenclature == TIndividuals.id_nomenclature_sex
            ).filter(TIndividuals.id_individual == id_individual)
        ind, nom_complet, nom_vern, sex = q.one()
        res = ind.as_dict()
        res.update({'nom_complet': nom_complet, 'nom_vern': nom_vern, 'sexe': sex})
    return res

@blueprint.route('/individuals/operations/<int:id_indiv>', methods=['GET'])
@json_resp
def get_operations_by_individual(id_indiv):
    """Récupération de toutes les opérations réalisées sur un individu"""
    try:
        datas = TOperations.query.filter(TOperations.id_individual == id_indiv).all()
        operations = FeatureCollection([ope.get_geofeature() for ope in datas])
        return operations
    except Exception as e:
        raise GeonatureApiError(e)