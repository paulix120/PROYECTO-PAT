from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field


# ===========================================================
# TABLA ACTIVIDADES
# ===========================================================

class Actividad(SQLModel, table=True):
    __tablename__ = "actividades"

    id: Optional[int] = Field(default=None, primary_key=True)

    nombre: str

    descripcion: Optional[str] = None

    destino_id: int = Field(
        foreign_key="destinos_turisticos.id"
    )

    direccion: Optional[str] = None

    precio: Decimal = Field(
        default=Decimal("0.00"),
        max_digits=10,
        decimal_places=2
    )

    pagina_oficial: Optional[str] = None

    telefono: Optional[str] = None

    imagen_principal: Optional[str] = None

    duracion_horas: Decimal = Field(
        default=Decimal("1.00"),
        max_digits=5,
        decimal_places=2
    )

    dificultad: str = "facil"

    activa: bool = True

    latitud: Optional[Decimal] = Field(
        default=None,
        max_digits=10,
        decimal_places=8
    )

    longitud: Optional[Decimal] = Field(
        default=None,
        max_digits=11,
        decimal_places=8
    )


# ===========================================================
# RESPONSE
# ===========================================================

class ActividadResponse(SQLModel):

    id: int

    nombre: str

    descripcion: Optional[str]

    destino_id: int

    direccion: Optional[str]

    precio: Decimal

    pagina_oficial: Optional[str]

    telefono: Optional[str]

    imagen_principal: Optional[str]

    duracion_horas: Decimal

    dificultad: str

    activa: bool

    latitud: Optional[Decimal]

    longitud: Optional[Decimal]


# ===========================================================
# CREATE
# ===========================================================

class ActividadCreate(SQLModel):

    nombre: str

    descripcion: Optional[str] = None

    destino_id: int

    direccion: Optional[str] = None

    precio: Decimal

    pagina_oficial: Optional[str] = None

    telefono: Optional[str] = None

    imagen_principal: Optional[str] = None

    duracion_horas: Decimal

    dificultad: str = "facil"


# ===========================================================
# UPDATE
# ===========================================================

class ActividadUpdate(SQLModel):

    nombre: Optional[str] = None

    descripcion: Optional[str] = None

    destino_id: Optional[int] = None

    direccion: Optional[str] = None

    precio: Optional[Decimal] = None

    pagina_oficial: Optional[str] = None

    telefono: Optional[str] = None

    imagen_principal: Optional[str] = None

    duracion_horas: Optional[Decimal] = None

    dificultad: Optional[str] = None

    activa: Optional[bool] = None