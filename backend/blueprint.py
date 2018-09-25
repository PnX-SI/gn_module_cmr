from flask import Blueprint

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import json_resp
from geonature.core.gn_monitoring.models import TBaseSites
from .models import TPrograms, CorSiteProgram
from geojson import FeatureCollection

blueprint = Blueprint('cmr', __name__)

@blueprint.route('/test', methods=['GET', 'POST'])
def test():
    return 'It works'

@blueprint.route('/programs', methods=['GET'])
@json_resp
def get_programs():
    pgs = DB.session.query(TPrograms).all()
    return [pg.as_dict() for pg in pgs]

@blueprint.route('/sites/<int:id_program>', methods=['GET'])
@json_resp
def get_sites(id_program):
    q = DB.session.query(TBaseSites)
    q = q.join(CorSiteProgram, CorSiteProgram.id_site==TBaseSites.id_base_site)
    sites = q.filter(CorSiteProgram.id_program == id_program).all()
    features = []
    for site in sites:
        features.append(site.get_geofeature(recursif=False))
    return FeatureCollection(features)
