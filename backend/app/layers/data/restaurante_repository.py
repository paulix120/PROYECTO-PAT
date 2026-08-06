from typing import Optional

from sqlmodel import Session, select

from app.layers.data.base_repository import BaseRepository

from app.layers.models.restaurante import Restaurante


class RestauranteRepository:


    # ==========================================
    # CONSULTAS
    # ==========================================

    @staticmethod
    def listar(
        db: Session
    ):

        return db.exec(

            select(Restaurante)

            .where(
                Restaurante.activo == True
            )

        ).all()


    @staticmethod
    def obtener(
        db: Session,
        restaurante_id: int
    ) -> Optional[Restaurante]:

        return db.get(
            Restaurante,
            restaurante_id
        )


    # ==========================================
    # OPERACIONES
    # ==========================================

    @staticmethod
    def crear(
        db: Session,
        restaurante: Restaurante
    ):

        return BaseRepository.guardar(
            db,
            restaurante
        )


    @staticmethod
    def actualizar(
        db: Session,
        restaurante: Restaurante
    ):

        return BaseRepository.actualizar(
            db,
            restaurante
        )


    @staticmethod
    def eliminar(
        db: Session,
        restaurante: Restaurante
    ):

        return BaseRepository.eliminar_logico(
            db,
            restaurante
        )