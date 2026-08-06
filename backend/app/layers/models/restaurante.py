from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field


# ===========================================================
# TABLA RESTAURANTES
# ===========================================================

class Restaurante(SQLModel, table=True):
    __tablename__ = "restaurantes"

    id: Optional[int] = Field(default=None, primary_key=True)

    nombre: str

    descripcion: str

    tipo_cocina: str

    destino_id: int = Field(
        foreign_key="destinos_turisticos.id"
    )

    direccion: Optional[str] = None

    precio_promedio: Decimal = Field(
        default=Decimal("0.00"),
        max_digits=10,
        decimal_places=2
    )

    pagina_oficial: Optional[str] = None

    telefono: Optional[str] = None

    horario: Optional[str] = None

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
# RESPONSE
# ===========================================================

class RestauranteResponse(SQLModel):

    id: int

    nombre: str

    descripcion: str

    tipo_cocina: str

    destino_id: int

    direccion: Optional[str]

    precio_promedio: Decimal

    pagina_oficial: Optional[str] = None

    telefono: Optional[str]

    horario: Optional[str]

    imagen_principal: Optional[str]

    activo: bool

    latitud: Optional[Decimal] = None

    longitud: Optional[Decimal] = None


# ===========================================================
# CREATE
# ===========================================================

class RestauranteCreate(SQLModel):

    nombre: str

    descripcion: str

    tipo_cocina: str

    destino_id: int

    direccion: Optional[str] = None

    precio_promedio: Decimal

    pagina_oficial: Optional[str] = None

    telefono: Optional[str] = None

    horario: Optional[str] = None

    imagen_principal: Optional[str] = None


# ===========================================================
# UPDATE
# ===========================================================

class RestauranteUpdate(SQLModel):

    nombre: Optional[str] = None

    descripcion: Optional[str] = None

    tipo_cocina: Optional[str] = None

    destino_id: Optional[int] = None

    direccion: Optional[str] = None

    precio_promedio: Optional[Decimal] = None

    pagina_oficial: Optional[str] = None

    telefono: Optional[str] = None

    horario: Optional[str] = None

    imagen_principal: Optional[str] = None

    activo: Optional[bool] = None