from flask import Blueprint

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import json_resp

from pypnnomenclature.models import TNomenclatures

from .models import TPrograms, TIndividuals, Taxonomie

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
    q = DB.session.query(TIndividuals, Taxonomie.nom_complet, Taxonomie.nom_vern, TNomenclatures.mnemonique).join(
        Taxonomie, Taxonomie.cd_nom == TIndividuals.cd_nom).join(
            TNomenclatures, TNomenclatures.id_nomenclature == TIndividuals.id_nomenclature_sex)
    data = q.all()
    res = []
    for ind, nom_complet, nom_vern, sex in data:
        d = ind.as_dict()
        d.update({'nom_complet': nom_complet, 'nom_vern': nom_vern, 'sexe': sex})
        res.append(d)
    return res
