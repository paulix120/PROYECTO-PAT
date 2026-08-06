from datetime import datetime, timedelta, timezone
import bcrypt
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from app.core.config import settings
from app.db.session import get_session
from app.layers.data.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

# ============================================
# PASSWORD
# ============================================

def verify_password(
    plain_password: str,
    hashed_password: str
):

    return bcrypt.checkpw(
        plain_password.encode(),
        hashed_password.encode()
    )


def get_password_hash(password: str):

    salt = bcrypt.gensalt()

    return bcrypt.hashpw(
        password.encode(),
        salt
    ).decode()


# ============================================
# JWT
# ============================================

def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
):

    to_encode = data.copy()

    if expires_delta:

        expire = datetime.now(
            timezone.utc
        ) + expires_delta

    else:

        expire = datetime.now(
            timezone.utc
        ) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update(
        {
            "exp": expire
        }
    )

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


# ============================================
# DECODIFICAR TOKEN
# ============================================

def decode_token(token: str):

    try:

        payload = jwt.decode(

            token,

            settings.SECRET_KEY,

            algorithms=[settings.ALGORITHM]

        )

        return payload

    except JWTError:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Token inválido."

        )


# ============================================
# USUARIO ACTUAL
# ============================================

def get_current_user(

    token: str = Depends(oauth2_scheme),

    db: Session = Depends(get_session)

):

    payload = decode_token(token)

    usuario_id = payload.get("sub")

    if usuario_id is None:

        raise HTTPException(

            status_code=401,

            detail="Token inválido."

        )

    usuario = UserRepository.obtener_usuario_activo(

        db,

        int(usuario_id)

    )

    if usuario is None:

        raise HTTPException(

            status_code=401,

            detail="Usuario no encontrado."

        )

    return usuario


# ============================================
# ROLES
# ============================================

def require_role(*roles):

    def validator(

        usuario=Depends(get_current_user)

    ):

        if usuario.rol_id not in roles:

            raise HTTPException(

                status_code=403,

                detail="No tienes permisos."

            )

        return usuario

    return validator