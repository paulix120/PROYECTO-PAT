from fastapi import HTTPException
from sqlmodel import Session

from app.core.travel import (
    obtener_coordenadas_origen,
    calcular_distancia_km,
    calcular_tiempo,
    calcular_costo_transporte
)

from app.layers.data.plan_viaje_repository import PlanViajeRepository
from app.layers.data.destino_repository import DestinoRepository
from app.layers.data.transporte_repository import TransporteRepository

from app.layers.models.plan_viaje import (
    PlanViaje,
    PlanViajeCreate,
    PlanViajeUpdate
)


class PlanViajeService:


    # =====================================================
    # LISTAR
    # =====================================================

    @staticmethod
    def listar(
        db: Session,
        usuario_id: int
    ):

        return PlanViajeRepository.listar_por_usuario(
            db,
            usuario_id
        )


    # =====================================================
    # OBTENER
    # =====================================================

    @staticmethod
    def obtener(
        db: Session,
        plan_id: int,
        usuario_id: int
    ):

        plan = PlanViajeRepository.obtener_por_id(
            db,
            plan_id
        )

        if not plan:

            raise HTTPException(
                status_code=404,
                detail="Plan de viaje no encontrado."
            )

        if plan.usuario_id != usuario_id:

            raise HTTPException(
                status_code=403,
                detail="No tienes permisos."
            )

        return plan


    # =====================================================
    # CREAR
    # =====================================================

    @staticmethod
    def crear(
        db: Session,
        usuario_id: int,
        data: PlanViajeCreate
    ):

        # -----------------------------
        # Verificar destino
        # -----------------------------

        destino = DestinoRepository.obtener_por_id(
            db,
            data.destino_id
        )

        if not destino:

            raise HTTPException(
                status_code=404,
                detail="Destino no encontrado."
            )

        # -----------------------------
        # Verificar transporte
        # -----------------------------

        transporte = TransporteRepository.obtener_por_id(
            db,
            data.medio_transporte_id
        )

        if not transporte:

            raise HTTPException(
                status_code=404,
                detail="Medio de transporte no encontrado."
            )

        # -----------------------------
        # Obtener coordenadas del origen
        # -----------------------------

        lat_origen, lon_origen = obtener_coordenadas_origen(
            data.origen
        )

        if lat_origen is None:

            raise HTTPException(
                status_code=400,
                detail="No fue posible encontrar el origen."
            )

        # -----------------------------
        # Calcular distancia
        # -----------------------------

        distancia = calcular_distancia_km(
            lat_origen,
            lon_origen,
            destino.latitud,
            destino.longitud
        )

        # -----------------------------
        # Calcular tiempo
        # -----------------------------

        tiempo = calcular_tiempo(
            distancia,
            transporte.velocidad_kmh
        )

        # -----------------------------
        # Calcular costo
        # -----------------------------

        costo = calcular_costo_transporte(
            distancia,
            transporte.costo_por_km
        )

        # -----------------------------
        # Crear plan
        # -----------------------------

        plan = PlanViaje.model_validate(data)

        plan.usuario_id = usuario_id

        plan.latitud_origen = lat_origen
        plan.longitud_origen = lon_origen

        plan.distancia_km = distancia
        plan.tiempo_horas = tiempo
        plan.costo_transporte = costo

        return PlanViajeRepository.crear(
            db,
            plan
        )


    # =====================================================
    # ACTUALIZAR
    # =====================================================

    @staticmethod
    def actualizar(
        db: Session,
        plan_id: int,
        usuario_id: int,
        data: PlanViajeUpdate
    ):

        plan = PlanViajeRepository.obtener_por_id(
            db,
            plan_id
        )

        if not plan:

            raise HTTPException(
                status_code=404,
                detail="Plan no encontrado."
            )

        if plan.usuario_id != usuario_id:

            raise HTTPException(
                status_code=403,
                detail="No tienes permisos."
            )

        cambios = data.model_dump(
            exclude_unset=True
        )

        for campo, valor in cambios.items():

            setattr(
                plan,
                campo,
                valor
            )

        return PlanViajeRepository.actualizar(
            db,
            plan
        )


    # =====================================================
    # ELIMINAR
    # =====================================================

    @staticmethod
    def eliminar(
        db: Session,
        plan_id: int,
        usuario_id: int
    ):

        plan = PlanViajeRepository.obtener_por_id(
            db,
            plan_id
        )

        if not plan:

            raise HTTPException(
                status_code=404,
                detail="Plan no encontrado."
            )

        if plan.usuario_id != usuario_id:

            raise HTTPException(
                status_code=403,
                detail="No tienes permisos."
            )

        return PlanViajeRepository.eliminar(
            db,
            plan
        )