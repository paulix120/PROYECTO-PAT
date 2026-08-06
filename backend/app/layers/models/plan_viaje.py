from datetime import date
from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field


# ===========================================================
# TABLA PLANES DE VIAJE
# ===========================================================

class PlanViaje(SQLModel, table=True):
    __tablename__ = "planes_viaje"

    id: Optional[int] = Field(default=None, primary_key=True)

    usuario_id: int = Field(
        foreign_key="usuarios.id"
    )

    nombre_viaje: str

    origen: str

    latitud_origen: Optional[Decimal] = Field(
        default=None,
        max_digits=10,
        decimal_places=8
    )

    longitud_origen: Optional[Decimal] = Field(
        default=None,
        max_digits=11,
        decimal_places=8
    )

    destino_id: int = Field(
        foreign_key="destinos_turisticos.id"
    )

    medio_transporte_id: int = Field(
        foreign_key="medios_transporte.id"
    )

    fecha_inicio: Optional[date] = None

    fecha_fin: Optional[date] = None

    presupuesto: Optional[Decimal] = Field(
        default=None,
        max_digits=12,
        decimal_places=2
    )

    estado: str = "planificado"

    num_personas: int = 1

    distancia_km: Optional[Decimal] = Field(
        default=None,
        max_digits=10,
        decimal_places=2
    )

    tiempo_horas: Optional[Decimal] = Field(
        default=None,
        max_digits=6,
        decimal_places=2
    )

    costo_transporte: Optional[Decimal] = Field(
        default=None,
        max_digits=10,
        decimal_places=2
    )

    notas: Optional[str] = None

# ===========================================================
# RESPONSE
# ===========================================================

class PlanViajeResponse(SQLModel):

    id: int

    usuario_id: int

    nombre_viaje: str

    origen: str

    latitud_origen: Optional[Decimal]

    longitud_origen: Optional[Decimal]

    destino_id: int

    medio_transporte_id: int

    fecha_inicio: Optional[date]

    fecha_fin: Optional[date]

    presupuesto: Optional[Decimal]

    estado: str

    num_personas: int

    distancia_km: Optional[Decimal]

    tiempo_horas: Optional[Decimal]

    costo_transporte: Optional[Decimal]

    notas: Optional[str]

# ===========================================================
# CREATE
# ===========================================================

class PlanViajeCreate(SQLModel):

    nombre_viaje: str

    origen: str

    destino_id: int

    medio_transporte_id: int

    fecha_inicio: Optional[date] = None

    fecha_fin: Optional[date] = None

    presupuesto: Optional[Decimal] = None

    num_personas: int = 1

    notas: Optional[str] = None

# ===========================================================
# UPDATE
# ===========================================================

class PlanViajeUpdate(SQLModel):

    nombre_viaje: Optional[str] = None

    origen: Optional[str] = None

    destino_id: Optional[int] = None

    medio_transporte_id: Optional[int] = None

    fecha_inicio: Optional[date] = None

    fecha_fin: Optional[date] = None

    presupuesto: Optional[Decimal] = None

    estado: Optional[str] = None

    num_personas: Optional[int] = None

    notas: Optional[str] = None