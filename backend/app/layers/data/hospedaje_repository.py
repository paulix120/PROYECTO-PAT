from sqlmodel import Session, select

from app.layers.data.base_repository import BaseRepository
from app.layers.models.hospedaje import Hospedaje


class HospedajeRepository:


    @staticmethod
    def listar(db: Session):

        return db.exec(

            select(Hospedaje)

            .where(Hospedaje.activo == True)

            .order_by(Hospedaje.nombre)

        ).all()


    @staticmethod
    def obtener(
        db: Session,
        hospedaje_id: int
    ):

        return db.get(
            Hospedaje,
            hospedaje_id
        )


    @staticmethod
    def crear(
        db: Session,
        hospedaje: Hospedaje
    ):

        return BaseRepository.guardar(
            db,
            hospedaje
        )


    @staticmethod
    def actualizar(
        db: Session,
        hospedaje: Hospedaje
    ):

        return BaseRepository.actualizar(
            db,
            hospedaje
        )