from typing import Optional

from sqlmodel import Session, select, or_

from app.layers.data.base_repository import BaseRepository
from app.layers.models.transporte import MedioTransporte


class TransporteRepository(BaseRepository):

    # ==========================================
    # LISTAR TRANSPORTES
    # ==========================================

    @staticmethod
    def listar_por_usuario(
        db: Session,
        usuario_id: int
    ):

        consulta = (

            select(MedioTransporte)

            .where(

                MedioTransporte.activo == True,

                or_(

                    MedioTransporte.usuario_id == None,

                    MedioTransporte.usuario_id == usuario_id

                )

            )

            .order_by(
                MedioTransporte.nombre
            )

        )

        return db.exec(
            consulta
        ).all()

    # ==========================================
    # OBTENER POR ID
    # ==========================================

    @staticmethod
    def obtener_por_id(
        db: Session,
        transporte_id: int
    ) -> Optional[MedioTransporte]:

        return BaseRepository.obtener_por_id(
            db,
            MedioTransporte,
            transporte_id
        )

    # ==========================================
    # GUARDAR
    # ==========================================

    @staticmethod
    def guardar(
        db: Session,
        transporte: MedioTransporte
    ):

        return BaseRepository.guardar(
            db,
            transporte
        )

    # ==========================================
    # ACTUALIZAR
    # ==========================================

    @staticmethod
    def actualizar(
        db: Session,
        transporte: MedioTransporte
    ):

        return BaseRepository.actualizar(
            db,
            transporte
        )

    # ==========================================
    # ELIMINACIÓN LÓGICA
    # ==========================================

    @staticmethod
    def eliminar(
        db: Session,
        transporte: MedioTransporte
    ):

        return BaseRepository.eliminar_logico(
            db,
            transporte
        )