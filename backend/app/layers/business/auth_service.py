from datetime import datetime, timedelta, timezone
import secrets

from fastapi import HTTPException, status
from sqlmodel import Session

from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token
)

from app.layers.data.user_repository import UserRepository

from app.layers.models.auth import (
    User,
    UserCreate,
    UserLogin,
    ForgotPasswordRequest,
    ResetPasswordRequest
)


class AuthService:

    # =====================================================
    # REGISTRO
    # =====================================================

    @staticmethod
    def registrar_usuario(
        db: Session,
        data: UserCreate
    ):

        usuario_existente = UserRepository.obtener_por_email(
            db,
            data.email
        )

        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya se encuentra registrado."
            )

        nuevo_usuario = User(
            nombre=data.nombre,
            apellido=data.apellido,
            email=data.email,
            password_hash=get_password_hash(data.password),
            rol_id=1,
            activo=True
        )

        return UserRepository.crear(
            db,
            nuevo_usuario
        )

    # =====================================================
    # LOGIN
    # =====================================================

    @staticmethod
    def login(
        db: Session,
        data: UserLogin
    ):

        usuario = UserRepository.obtener_por_email(
            db,
            data.email
        )

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Correo o contraseña incorrectos."
            )

        if not verify_password(
            data.password,
            usuario.password_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Correo o contraseña incorrectos."
            )

        if not usuario.activo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario se encuentra inactivo."
            )

        token = create_access_token(
            data={
                "sub": str(usuario.id),
                "email": usuario.email,
                "rol_id": usuario.rol_id,
                "nombre": usuario.nombre
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    # =====================================================
    # RECUPERAR CONTRASEÑA
    # =====================================================

    @staticmethod
    def forgot_password(
        db: Session,
        data: ForgotPasswordRequest
    ):

        usuario = UserRepository.obtener_por_email(
            db,
            data.email
        )

        if not usuario:

            return {
                "mensaje": "Si el correo está registrado, se enviaron las instrucciones."
            }

        token = secrets.token_urlsafe(32)

        expiracion = datetime.now(
            timezone.utc
        ) + timedelta(minutes=15)

        usuario.token_recuperacion = token
        usuario.token_expiracion = expiracion

        UserRepository.actualizar(
            db,
            usuario
        )

        return {
            "mensaje": "Instrucciones generadas correctamente.",
            "token_desarrollo": token
        }

    # =====================================================
    # RESTABLECER CONTRASEÑA
    # =====================================================

    @staticmethod
    def reset_password(
        db: Session,
        data: ResetPasswordRequest
    ):

        usuario = UserRepository.obtener_por_token(
            db,
            data.token
        )

        if not usuario:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token inválido."
            )

        expiracion = usuario.token_expiracion

        if expiracion is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El token ya no es válido."
            )

        if expiracion.tzinfo is None:
            expiracion = expiracion.replace(
                tzinfo=timezone.utc
            )

        if datetime.now(
            timezone.utc
        ) > expiracion:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El token expiró."
            )

        usuario.password_hash = get_password_hash(
            data.new_password
        )

        usuario.token_recuperacion = None
        usuario.token_expiracion = None

        UserRepository.actualizar(
            db,
            usuario
        )

        return {
            "mensaje": "Contraseña actualizada correctamente."
        }