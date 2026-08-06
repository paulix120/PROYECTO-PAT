from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.db.session import get_session

from app.layers.business.destino_service import DestinoService

from app.layers.models.destinos import (
    DestinoCreate,
    DestinoResponse,
    DestinoUpdate
)

router = APIRouter(
    prefix="/destinos",
    tags=["Destinos Turísticos"]
)


@router.get(
    "/",
    response_model=List[DestinoResponse]
)
def listar_destinos(
    db: Session = Depends(get_session)
):
    return DestinoService.listar(db)


@router.get(
    "/{destino_id}",
    response_model=DestinoResponse
)
def obtener_destino(
    destino_id: int,
    db: Session = Depends(get_session)
):
    return DestinoService.obtener_por_id(
        db,
        destino_id
    )


@router.post(
    "/",
    response_model=DestinoResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_destino(
    data: DestinoCreate,
    db: Session = Depends(get_session)
):
    return DestinoService.crear(
        db,
        data
    )


@router.put(
    "/{destino_id}",
    response_model=DestinoResponse
)
def actualizar_destino(
    destino_id: int,
    data: DestinoUpdate,
    db: Session = Depends(get_session)
):
    return DestinoService.actualizar(
        db,
        destino_id,
        data
    )


@router.delete("/{destino_id}")
def eliminar_destino(
    destino_id: int,
    db: Session = Depends(get_session)
):

    DestinoService.eliminar(
        db,
        destino_id
    )

    return {
        "mensaje": "Destino eliminado correctamente."
    }