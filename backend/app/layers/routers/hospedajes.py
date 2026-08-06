from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.db.session import get_session

from app.layers.business.hospedaje_service import HospedajeService

from app.layers.models.hospedaje import (
    HospedajeCreate,
    HospedajeUpdate,
    HospedajeResponse
)

router = APIRouter(
    prefix="/hospedajes",
    tags=["Hospedajes"]
)


# ==========================================
# LISTAR
# ==========================================

@router.get(
    "/",
    response_model=List[HospedajeResponse]
)
def listar_hospedajes(
    db: Session = Depends(get_session)
):

    return HospedajeService.listar(db)


# ==========================================
# OBTENER POR ID
# ==========================================

@router.get(
    "/{hospedaje_id}",
    response_model=HospedajeResponse
)
def obtener_hospedaje(
    hospedaje_id: int,
    db: Session = Depends(get_session)
):

    return HospedajeService.obtener(
        db,
        hospedaje_id
    )


# ==========================================
# CREAR
# ==========================================

@router.post(
    "/",
    response_model=HospedajeResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_hospedaje(
    data: HospedajeCreate,
    db: Session = Depends(get_session)
):

    return HospedajeService.crear(
        db,
        data
    )


# ==========================================
# ACTUALIZAR
# ==========================================

@router.put(
    "/{hospedaje_id}",
    response_model=HospedajeResponse
)
def actualizar_hospedaje(
    hospedaje_id: int,
    data: HospedajeUpdate,
    db: Session = Depends(get_session)
):

    return HospedajeService.actualizar(
        db,
        hospedaje_id,
        data
    )


# ==========================================
# ELIMINAR
# ==========================================

@router.delete(
    "/{hospedaje_id}"
)
def eliminar_hospedaje(
    hospedaje_id: int,
    db: Session = Depends(get_session)
):

    HospedajeService.eliminar(
        db,
        hospedaje_id
    )

    return {
        "mensaje": "Hospedaje eliminado correctamente."
    }