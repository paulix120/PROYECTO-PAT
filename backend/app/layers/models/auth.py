from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


# ======================================================
# MODELO DE BASE DE DATOS
# ======================================================

class User(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: Optional[int] = Field(default=None, primary_key=True)

    nombre: str

    apellido: str

    email: str = Field(index=True)

    password_hash: str

    rol_id: int = Field(default=1)

    activo: bool = Field(default=True)

    token_recuperacion: Optional[str] = None

    token_expiracion: Optional[datetime] = None


# ======================================================
# DTO CREAR USUARIO
# ======================================================

class UserCreate(SQLModel):

    nombre: str

    apellido: str

    email: str

    password: str


# ======================================================
# DTO LOGIN
# ======================================================

class UserLogin(SQLModel):

    email: str

    password: str


# ======================================================
# DTO RESPUESTA
# ======================================================

class UserResponse(SQLModel):

    id: int

    nombre: str

    apellido: str

    email: str

    rol_id: int

    activo: bool


# ======================================================
# TOKEN JWT
# ======================================================

class Token(SQLModel):

    access_token: str

    token_type: str


# ======================================================
# RECUPERAR CONTRASEÑA
# ======================================================

class ForgotPasswordRequest(SQLModel):

    email: str


class ResetPasswordRequest(SQLModel):

    token: str

    new_password: str