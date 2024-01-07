from fastapi import APIRouter, Header, Depends, HTTPException
from sqlalchemy.orm import Session
from piro_api.database import get_db
from piro_api.models.auth import AuthRequest, UserClaims
from piro_api import get_settings, AppGenericException
from piro_api.orm import User, Attribute, RoleAttribute
from datetime import datetime
from jose import jwt
from jose.constants import ALGORITHMS
import uuid
import bcrypt
from typing import List




from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=15000,
)


@router.post('/auth')
def auth(request_data: AuthRequest,
         accept_language: str = Header(default='en'),
         db: Session = Depends(get_db)):
    config = get_settings()
    print ("Holaaa")
    username = request_data.username
    password = request_data.password
    print (password)

    user = db.query(User).filter_by(username=username).first()

    if not user:
        raise AppGenericException(0, 'User not found.', 404)

    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise AppGenericException(0, 'Invalid username or password. Please try again.', 400)


    user_role = user.roles[0].id
    attribute = db.query(Attribute).filter(Attribute.code == 'VIEW_ADMIN_SYS').first()

    user_role_admin = db.query(RoleAttribute) \
        .filter(RoleAttribute.roleId == user_role) \
        .filter(RoleAttribute.attributeId == attribute.id) \
        .first()

    if user_role_admin is not None:
        # todo: define or remove employee_id and store from UserClaims
        now_seconds = int(datetime.now().timestamp())
        token = jwt.encode({
            'iat': now_seconds,
            'nbf': now_seconds,
            'jti': str(uuid.uuid4()),
            'identity': user.id,
            'name': user.username,
            'fresh': False,
            'type': 'access',
        }, config.secret, algorithm=ALGORITHMS.HS256)
        print (token)
        return {'token': token}
    else:
        raise AppGenericException(0, "Can't start session.", 400)
    



@router.get('/api/user/{user_id}/attributes', tags=['auth'])
def get_user_attributes(user_id: int,
                        accept_language: str = Header(default='en'),
                        db: Session = Depends(get_db)):
    config = get_settings()

    user: User = db.query(User).get(user_id)

    attributes: List[str] = []
    for user_role in user.roles:
        role_attributes: List[RoleAttribute] = db.query(RoleAttribute) \
            .filter(RoleAttribute.roleId == user_role.id) \
            .all()

        for role_attribute in role_attributes:
            attribute: Attribute = db.query(Attribute).get(role_attribute.attributeId)
            attributes.append(attribute.code)

    return {'data': list(set(attributes))}
