from sqlalchemy import ForeignKey

from geonature.utils.utilssqlalchemy import serializable
from geonature.utils.env import DB

@serializable
class TPrograms(DB.Model):
    __tablename__ = 't_programs'
    __table_args__ = {'schema': 'pr_cmr'}
    id_program = DB.Column(
        DB.Integer,
        primary_key=True,
    )
    program_name = DB.Column(DB.Unicode)
    program_desc = DB.Column(DB.Unicode)


@serializable
class TIndividuals(DB.Model):
    __tablename__ = 't_individuals'
    __table_args__ = {'schema': 'pr_cmr'}
    id_individual = DB.Column(
        DB.Integer,
        primary_key=True,
    )
    cd_nom = DB.Column(DB.Integer)
    tag_code = DB.Column(DB.Unicode)
    tag_location = DB.Column(DB.Unicode)
    id_site_tag = DB.Column( 
        DB.Integer,
        ForeignKey('gn_monitoring.t_base_sites.id_base_site')
    )
    id_nomenclature_sex = DB.Column(
        DB.Integer,
        ForeignKey('ref_nomenclatures.t_nomenclatures.id_nomenclature')
    )