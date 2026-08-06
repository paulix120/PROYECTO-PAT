from typing import Optional

from sqlmodel import Session, select

from app.layers.data.base_repository import BaseRepository
from app.layers.models.destinos import (
    Destino,
    Ciudad
)


class DestinoRepository:

    @staticmethod
    def listar(db: Session):
        return db.exec(
            select(Destino).where(Destino.activo == True)
        ).all()

    @staticmethod
    def obtener_por_id(
        db: Session,
        destino_id: int
    ) -> Optional[Destino]:

        return db.get(Destino, destino_id)

    @staticmethod
    def obtener_ciudad(
        db: Session,
        ciudad_id: int
    ) -> Optional[Ciudad]:

        return db.get(Ciudad, ciudad_id)

    @staticmethod
    def crear(
        db: Session,
        destino: Destino
    ):
        return BaseRepository.guardar(db, destino)

    @staticmethod
    def actualizar(
        db: Session,
        destino: Destino
    ):
        return BaseRepository.actualizar(db, destino)

    @staticmethod
    def eliminar(
        db: Session,
        destino: Destino
    ):
        return BaseRepository.eliminar_logico(db, destino)