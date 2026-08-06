from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.db.session import get_session
from app.core.dependencies import get_current_user

from app.layers.models.auth import User
from app.layers.models.transporte import (
    MedioTransporteCreate,
    MedioTransporteResponse,
    MedioTransporteUpdate
)

from app.layers.business.transporte_service import TransporteService


router = APIRouter(
    prefix="/transporte",
    tags=["Medios de Transporte"]
)


# ==========================================
# LISTAR
# ==========================================

@router.get(
    "/",
    response_model=List[MedioTransporteResponse]
)
def listar_medios_transporte(
    db: Session = Depends(get_session),
    usuario: User = Depends(get_current_user)
):

    return TransporteService.listar(
        db,
        usuario
    )


# ==========================================
# OBTENER POR ID
# ==========================================

@router.get(
    "/{transporte_id}",
    response_model=MedioTransporteResponse
)
def obtener_medio_transporte(
    transporte_id: int,
    db: Session = Depends(get_session),
    usuario: User = Depends(get_current_user)
):

    return TransporteService.obtener_por_id(
        db,
        usuario,
        transporte_id
    )


# ==========================================
# CREAR
# ==========================================

@router.post(
    "/",
    response_model=MedioTransporteResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_medio_transporte(
    data: MedioTransporteCreate,
    db: Session = Depends(get_session),
    usuario: User = Depends(get_current_user)
):

    return TransporteService.crear(
        db,
        usuario,
        data
    )


# ==========================================
# ACTUALIZAR
# ==========================================

@router.put(
    "/{transporte_id}",
    response_model=MedioTransporteResponse
)
def actualizar_medio_transporte(
    transporte_id: int,
    data: MedioTransporteUpdate,
    db: Session = Depends(get_session),
    usuario: User = Depends(get_current_user)
):

    return TransporteService.actualizar(
        db,
        usuario,
        transporte_id,
        data
    )


# ==========================================
# ELIMINAR
# ==========================================

@router.delete(
    "/{transporte_id}"
)
def eliminar_medio_transporte(
    transporte_id: int,
    db: Session = Depends(get_session),
    usuario: User = Depends(get_current_user)
):

    TransporteService.eliminar(
        db,
        usuario,
        transporte_id
    )

    return {
        "mensaje": "Medio de transporte eliminado correctamente."
    }