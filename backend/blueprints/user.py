from flask import Blueprint, Response, request
from backend.exceptions import NotFoundException, BadRequestException, ConflictException
from backend import model
from jsonschema import validate, ValidationError
import ldap

#############################################################################
#                                 VARIABLES                                 #
#############################################################################
bp = Blueprint('users', __name__)

#############################################################################
#                                 SCHEMAS                                   #
#############################################################################
ADD_USER_SCHEMA = {
    'type': 'object',
    'properties': {
        'uid': {
            'type': 'string'
        },
        'cn': {
            'type': 'string'
        },
        'sn': {
            'type': 'string'
        },
        'description': {
            'type': 'string'
        }
    },
    "additionalProperties": False,
    'required': [
        'uid',
        'cn',
        'sn',
    ]
}


#############################################################################
#                             HELPER FUNCTIONS                              #
#############################################################################


#############################################################################
#                                  ROUTES                                   #
#############################################################################
@bp.route('/', methods=['GET'])
def health_check():
    return 'ok'


@bp.route('/users', methods=['POST'])
def create_user():
    payload = request.get_json()
    try:
        validate(payload, ADD_USER_SCHEMA)
    except ValidationError as err:
        raise BadRequestException(str(err))

    try:
        model.create_user(
            uid=payload['uid'],
            cn=payload['cn'],
            sn=payload['sn'],
            description=payload.get('description')
        )
    except ldap.ALREADY_EXISTS as err:
        raise ConflictException(message='Already exists')

    return Response(status=201)