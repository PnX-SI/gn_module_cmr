from geoalchemy2 import Geometry

from geonature.utils.env import DB
from geonature.utils.utilssqlalchemy import serializable, geoserializable
from flask import current_app
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey

local_srid = current_app.config['LOCAL_SRID']

@serializable
class TPrograms(DB.Model):
    """Table des protocoles de CMR du module"""
    __tablename__ = 't_programs'
    __table_args__ = {'schema': 'pr_cmr'}
    id_program = DB.Column(
        DB.Integer,
        primary_key=True,
    )
    program_name = DB.Column(DB.Unicode)
    program_desc = DB.Column(DB.Unicode)

@serializable
@geoserializable
class TOperations(DB.Model):
    """Table des opérations sur un individu"""
    __tablename__ = 't_operations'
    __table_args__ = {'schema': 'pr_cmr'}
    id_operation = DB.Column(
        DB.Integer,
        primary_key=True
    )
    id_individual = DB.Column(DB.Integer,
                              nullable=False)
    id_site = DB.Column(
        DB.Integer,
        nullable=False
    )
    geom_point_4326 = DB.Column(Geometry(geometry_type='POINT', srid=4326))
    geom_point_local = DB.Column(Geometry(geometry_type='POINT', srid=local_srid))
    date_min = DB.Column(DB.TIMESTAMP, nullable=False)
    date_max = DB.Column(DB.TIMESTAMP, nullable=False)
    id_nomenclature_cmr_action = DB.Column(DB.Integer)
    id_nomenclature_obs_method = DB.Column(DB.Integer)
    id_nomenclature_life_stage = DB.Column(DB.Integer)
    id_nomenclature_bio_condition = DB.Column(DB.Integer)
    id_nomenclature_determination_method = DB.Column(DB.Integer)
    determiner = DB.Column(DB.Unicode)
    unique_id_sinp = DB.Column(UUID(as_uuid=True))
	
    def get_geofeature(self, recursif=True, columns=None):
        return self.as_geofeature('geom_point_4326', 'id_operation', recursif, columns=columns)

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

@serializable
class Taxonomie(DB.Model):
    __tablename__ = 'taxref'
    __table_args__ = {
        'schema': 'taxonomie',
        'extend_existing': True
    }

    cd_nom = DB.Column(
        DB.Integer,
        primary_key=True
    )
    nom_complet = DB.Column(DB.Unicode)
    nom_vern = DB.Column(DB.Unicode)
