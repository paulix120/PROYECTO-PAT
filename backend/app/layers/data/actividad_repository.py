from typing import Optional

from sqlmodel import Session, select

from app.layers.data.base_repository import BaseRepository

from app.layers.models.actividad import Actividad


class ActividadRepository:


    # ==========================================
    # CONSULTAS
    # ==========================================

    @staticmethod
    def listar(
        db: Session
    ):

        return db.exec(

            select(Actividad)

            .where(
                Actividad.activa == True
            )

        ).all()


    @staticmethod
    def obtener(
        db: Session,
        actividad_id: int
    ) -> Optional[Actividad]:

        return db.get(
            Actividad,
            actividad_id
        )


    # ==========================================
    # OPERACIONES
    # ==========================================

    @staticmethod
    def crear(
        db: Session,
        actividad: Actividad
    ):

        return BaseRepository.guardar(
            db,
            actividad
        )


    @staticmethod
    def actualizar(
        db: Session,
        actividad: Actividad
    ):

        return BaseRepository.actualizar(
            db,
            actividad
        )


    @staticmethod
    def eliminar(
        db: Session,
        actividad: Actividad
    ):

        return BaseRepository.eliminar_logico(
            db,
            actividad
        )