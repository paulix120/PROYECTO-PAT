from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.db.session import get_session

from app.layers.business.restaurante_service import RestauranteService

from app.layers.models.restaurante import (
    RestauranteCreate,
    RestauranteUpdate,
    RestauranteResponse
)

router = APIRouter(
    prefix="/restaurantes",
    tags=["Restaurantes"]
)


# =====================================
# GET
# =====================================

@router.get(
    "/",
    response_model=List[RestauranteResponse]
)
def listar_restaurantes(
    db: Session = Depends(get_session)
):

    return RestauranteService.listar(db)


# =====================================
# GET POR ID
# =====================================

@router.get(
    "/{restaurante_id}",
    response_model=RestauranteResponse
)
def obtener_restaurante(
    restaurante_id: int,
    db: Session = Depends(get_session)
):

    return RestauranteService.obtener(
        db,
        restaurante_id
    )


# =====================================
# POST
# =====================================

@router.post(
    "/",
    response_model=RestauranteResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_restaurante(
    data: RestauranteCreate,
    db: Session = Depends(get_session)
):

    return RestauranteService.crear(
        db,
        data
    )


# =====================================
# PUT
# =====================================

@router.put(
    "/{restaurante_id}",
    response_model=RestauranteResponse
)
def actualizar_restaurante(
    restaurante_id: int,
    data: RestauranteUpdate,
    db: Session = Depends(get_session)
):

    return RestauranteService.actualizar(
        db,
        restaurante_id,
        data
    )


# =====================================
# DELETE
# =====================================

@router.delete(
    "/{restaurante_id}"
)
def eliminar_restaurante(
    restaurante_id: int,
    db: Session = Depends(get_session)
):

    RestauranteService.eliminar(
        db,
        restaurante_id
    )

    return {
        "mensaje": "Restaurante eliminado correctamente."
    }