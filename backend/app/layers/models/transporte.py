from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class MedioTransporteBase(SQLModel):
    nombre: str = Field(index=True, max_length=100)
    velocidad_kmh: float = Field(default=60.0)
    costo_por_km: float
    icono: Optional[str] = None


class MedioTransporte(MedioTransporteBase, table=True):
    __tablename__ = "medios_transporte"

    id: Optional[int] = Field(default=None, primary_key=True)

    usuario_id: Optional[int] = Field(
        default=None,
        foreign_key="usuarios.id"
    )

    activo: bool = Field(default=True)



class MedioTransporteCreate(MedioTransporteBase):
    pass


class MedioTransporteUpdate(SQLModel):
    nombre: Optional[str] = None
    velocidad_kmh: Optional[float] = None
    costo_por_km: Optional[float] = None
    icono: Optional[str] = None
    activo: Optional[bool] = None


class MedioTransporteResponse(MedioTransporteBase):
    id: int
    usuario_id: Optional[int]
    activo: bool