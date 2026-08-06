from datetime import datetime
from decimal import Decimal
from typing import Optional
from decimal import Decimal
from sqlmodel import SQLModel, Field


# ===========================================================
# TABLA HOSPEDAJES
# ===========================================================

class Hospedaje(SQLModel, table=True):
    __tablename__ = "hospedajes"

    id: Optional[int] = Field(default=None, primary_key=True)

    nombre: str

    descripcion: str

    tipo: str

    destino_id: int = Field(
        foreign_key="destinos_turisticos.id"
    )

    direccion: Optional[str] = None

    precio_noche: Decimal = Field(
        default=Decimal("0.00"),
        max_digits=10,
        decimal_places=2
    )

    pagina_oficial: Optional[str] = None

    estrellas: Optional[int] = None

    telefono: Optional[str] = None

    imagen_principal: Optional[str] = None

    activo: bool = True

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
# RESPUESTA
# ===========================================================

class HospedajeResponse(SQLModel):

    id: int

    nombre: str

    descripcion: str

    tipo: str

    destino_id: int

    direccion: Optional[str]

    precio_noche: Decimal

    pagina_oficial: Optional[str] = None

    estrellas: Optional[int]

    telefono: Optional[str]

    imagen_principal: Optional[str]

    activo: bool

    latitud: Optional[Decimal] = None

    longitud: Optional[Decimal] = None


# ===========================================================
# CREAR
# ===========================================================

class HospedajeCreate(SQLModel):

    nombre: str

    descripcion: str

    tipo: str

    destino_id: int

    direccion: Optional[str] = None

    precio_noche: Decimal

    pagina_oficial: Optional[str] = None

    estrellas: Optional[int] = None

    telefono: Optional[str] = None

    imagen_principal: Optional[str] = None


# ===========================================================
# ACTUALIZAR
# ===========================================================

class HospedajeUpdate(SQLModel):

    nombre: Optional[str] = None

    descripcion: Optional[str] = None

    tipo: Optional[str] = None

    destino_id: Optional[int] = None

    direccion: Optional[str] = None

    precio_noche: Optional[Decimal] = None

    pagina_oficial: Optional[str] = None

    estrellas: Optional[int] = None

    telefono: Optional[str] = None

    imagen_principal: Optional[str] = None

    activo: Optional[bool] = None