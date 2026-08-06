from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.db.session import get_session

from app.layers.business.actividad_service import ActividadService

from app.layers.models.actividad import (
    ActividadCreate,
    ActividadUpdate,
    ActividadResponse
)

router = APIRouter(
    prefix="/actividades",
    tags=["Actividades"]
)


# =====================================
# GET
# =====================================

@router.get(
    "/",
    response_model=List[ActividadResponse]
)
def listar_actividades(
    db: Session = Depends(get_session)
):

    return ActividadService.listar(
        db
    )


# =====================================
# GET POR ID
# =====================================

@router.get(
    "/{actividad_id}",
    response_model=ActividadResponse
)
def obtener_actividad(
    actividad_id: int,
    db: Session = Depends(get_session)
):

    return ActividadService.obtener(
        db,
        actividad_id
    )


# =====================================
# POST
# =====================================

@router.post(
    "/",
    response_model=ActividadResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_actividad(
    data: ActividadCreate,
    db: Session = Depends(get_session)
):

    return ActividadService.crear(
        db,
        data
    )


# =====================================
# PUT
# =====================================

@router.put(
    "/{actividad_id}",
    response_model=ActividadResponse
)
def actualizar_actividad(
    actividad_id: int,
    data: ActividadUpdate,
    db: Session = Depends(get_session)
):

    return ActividadService.actualizar(
        db,
        actividad_id,
        data
    )


# =====================================
# DELETE
# =====================================

@router.delete(
    "/{actividad_id}"
)
def eliminar_actividad(
    actividad_id: int,
    db: Session = Depends(get_session)
):

    ActividadService.eliminar(
        db,
        actividad_id
    )

    return {
        "mensaje": "Actividad eliminada correctamente."
    }