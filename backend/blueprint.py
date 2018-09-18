from flask import Blueprint

blueprint = Blueprint('cmr', __name__)


@blueprint.route('/test', methods=['GET', 'POST'])
def test():
    return 'It works'
