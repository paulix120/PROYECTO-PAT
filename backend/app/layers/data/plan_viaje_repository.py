from typing import Optional

from sqlmodel import Session, select

from app.layers.data.base_repository import BaseRepository
from app.layers.models.plan_viaje import PlanViaje


class PlanViajeRepository:


    # =====================================================
    # CONSULTAS
    # =====================================================

    @staticmethod
    def listar(
        db: Session
    ):

        return db.exec(

            select(PlanViaje)

            .where(
                PlanViaje.estado != "cancelado"
            )

            .order_by(
                PlanViaje.id.desc()
            )

        ).all()


    @staticmethod
    def obtener_por_id(
        db: Session,
        plan_id: int
    ) -> Optional[PlanViaje]:

        return db.get(
            PlanViaje,
            plan_id
        )


    @staticmethod
    def listar_por_usuario(
        db: Session,
        usuario_id: int
    ):

        return db.exec(

            select(PlanViaje)

            .where(
                PlanViaje.usuario_id == usuario_id,
                PlanViaje.estado != "cancelado"
            )

            .order_by(
                PlanViaje.id.desc()
            )

        ).all()


    # =====================================================
    # OPERACIONES
    # =====================================================

    @staticmethod
    def crear(
        db: Session,
        plan: PlanViaje
    ):

        return BaseRepository.guardar(
            db,
            plan
        )


    @staticmethod
    def actualizar(
        db: Session,
        plan: PlanViaje
    ):

        return BaseRepository.actualizar(
            db,
            plan
        )


    @staticmethod
    def eliminar(
        db: Session,
        plan: PlanViaje
    ):

        plan.estado = "cancelado"

        return BaseRepository.actualizar(
            db,
            plan
        )