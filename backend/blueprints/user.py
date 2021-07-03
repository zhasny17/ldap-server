from flask import Blueprint, Response, request
from flask.json import jsonify
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

UPDATE_USER_SCHEMA = {
    'type': 'object',
    'properties': {
        'sn': {
            'type': 'string'
        },
        'description': {
            'type': 'string'
        }
    },
    "additionalProperties": False
}


#############################################################################
#                             HELPER FUNCTIONS                              #
#############################################################################
def jsonify_user(user):
    return {
        'uid': user.get('uid'),
        'cn': user.get('cn'),
        'sn': user.get('sn'),
        'description': user.get('description')
    }


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
        check_user = model.get_user(payload['uid'])
        if check_user:
            raise ldap.ALREADY_EXISTS
        model.create_user(
            uid=payload['uid'],
            cn=payload['cn'],
            sn=payload['sn'],
            description=payload.get('description')
        )
    except ldap.ALREADY_EXISTS as err:
        raise ConflictException(message='Already exists')

    return Response(status=201)


@bp.route('/users/<string:uid>', methods=['GET'])
def get_user(uid):
    user = model.get_user(uid)
    if not user:
        raise NotFoundException(message='User not found')

    return jsonify(
        jsonify_user(user)
    )


@bp.route('/users', methods=['GET'])
def get_users():
    users = model.get_users()
    for index, user in enumerate(users):
        users[index] = jsonify_user(user)
    return jsonify(
        {'users': users}
    )


@bp.route('/users/<string:uid>', methods=['DELETE'])
def delete_users(uid):
    try:
        user = model.get_user(uid)
        if not user:
            raise ldap.NO_SUCH_OBJECT
        user_cn = user.get('cn')
        model.delete_user(user_cn)
    except ldap.NO_SUCH_OBJECT:
        raise NotFoundException(message='User not found')

    return Response(status=204)


@bp.route('/users/<string:uid>', methods=['PUT'])
def update_users(uid):
    payload = request.get_json()
    try:
        validate(payload, UPDATE_USER_SCHEMA)
    except ValidationError as err:
        raise BadRequestException(str(err))

    success = model.update_user(
        uid=uid,
        sn=payload.get('sn'),
        description=payload.get('description'),
    )
    if not success:
        raise NotFoundException(message='User not found')

    return Response(status=204)