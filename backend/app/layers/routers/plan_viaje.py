from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.db.session import get_session

from app.core.security import get_current_user

from app.layers.business.plan_viaje_service import PlanViajeService

from app.layers.models.auth import User

from app.layers.models.plan_viaje import (
    PlanViajeCreate,
    PlanViajeUpdate,
    PlanViajeResponse
)

router = APIRouter(
    prefix="/planes-viaje",
    tags=["Planes de Viaje"]
)


# =====================================================
# LISTAR MIS PLANES
# =====================================================

@router.get(
    "/",
    response_model=list[PlanViajeResponse]
)
def listar_planes(
    db: Session = Depends(get_session),
    usuario: User = Depends(get_current_user)
):

    return PlanViajeService.listar(
        db,
        usuario.id
    )


# =====================================================
# OBTENER PLAN
# =====================================================

@router.get(
    "/{plan_id}",
    response_model=PlanViajeResponse
)
def obtener_plan(
    plan_id: int,
    db: Session = Depends(get_session),
    usuario: User = Depends(get_current_user)
):

    return PlanViajeService.obtener(
        db,
        plan_id,
        usuario.id
    )


# =====================================================
# CREAR PLAN
# =====================================================

@router.post(
    "/",
    response_model=PlanViajeResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_plan(
    data: PlanViajeCreate,
    db: Session = Depends(get_session),
    usuario: User = Depends(get_current_user)
):

    return PlanViajeService.crear(
        db,
        usuario.id,
        data
    )


# =====================================================
# ACTUALIZAR PLAN
# =====================================================

@router.put(
    "/{plan_id}",
    response_model=PlanViajeResponse
)
def actualizar_plan(
    plan_id: int,
    data: PlanViajeUpdate,
    db: Session = Depends(get_session),
    usuario: User = Depends(get_current_user)
):

    return PlanViajeService.actualizar(
        db,
        plan_id,
        usuario.id,
        data
    )


# =====================================================
# ELIMINAR PLAN
# =====================================================

@router.delete(
    "/{plan_id}"
)
def eliminar_plan(
    plan_id: int,
    db: Session = Depends(get_session),
    usuario: User = Depends(get_current_user)
):

    return PlanViajeService.eliminar(
        db,
        plan_id,
        usuario.id
    )