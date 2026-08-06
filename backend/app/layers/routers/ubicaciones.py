from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.db.session import get_session

from app.layers.business.ubicacion_service import UbicacionService

from app.layers.models.destinos import (

    DepartamentoCreate,
    DepartamentoResponse,

    CiudadCreate,
    CiudadResponse,

    TipoTurismoCreate,
    TipoTurismoResponse

)

router = APIRouter(
    prefix="/ubicaciones",
    tags=["Ubicaciones"]
)

# =====================================================
# DEPARTAMENTOS
# =====================================================

@router.get(
    "/departamentos",
    response_model=List[DepartamentoResponse]
)
def listar_departamentos(
    db: Session = Depends(get_session)
):
    return UbicacionService.listar_departamentos(db)


@router.post(
    "/departamentos",
    response_model=DepartamentoResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_departamento(
    data: DepartamentoCreate,
    db: Session = Depends(get_session)
):
    return UbicacionService.crear_departamento(
        db,
        data
    )


# =====================================================
# CIUDADES
# =====================================================

@router.get(
    "/ciudades",
    response_model=List[CiudadResponse]
)
def listar_ciudades(
    db: Session = Depends(get_session)
):
    return UbicacionService.listar_ciudades(db)


@router.post(
    "/ciudades",
    response_model=CiudadResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_ciudad(
    data: CiudadCreate,
    db: Session = Depends(get_session)
):
    return UbicacionService.crear_ciudad(
        db,
        data
    )


# =====================================================
# TIPOS DE TURISMO
# =====================================================

@router.get(
    "/tipos-turismo",
    response_model=List[TipoTurismoResponse]
)
def listar_tipos(
    db: Session = Depends(get_session)
):
    return UbicacionService.listar_tipos(db)


@router.post(
    "/tipos-turismo",
    response_model=TipoTurismoResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_tipo(
    data: TipoTurismoCreate,
    db: Session = Depends(get_session)
):
    return UbicacionService.crear_tipo(
        db,
        data
    )