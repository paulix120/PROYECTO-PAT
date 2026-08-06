from typing import Optional

from sqlmodel import Session, select

from app.layers.data.base_repository import BaseRepository

from app.layers.models.destinos import (
    Departamento,
    Ciudad,
    TipoTurismo
)


class UbicacionRepository:

    # ==========================
    # DEPARTAMENTOS
    # ==========================

    @staticmethod
    def listar_departamentos(db: Session):
        return db.exec(
            select(Departamento)
        ).all()

    @staticmethod
    def obtener_departamento(
        db: Session,
        departamento_id: int
    ) -> Optional[Departamento]:

        return db.get(
            Departamento,
            departamento_id
        )

    @staticmethod
    def crear_departamento(
        db: Session,
        departamento: Departamento
    ):

        return BaseRepository.guardar(
            db,
            departamento
        )

    # ==========================
    # CIUDADES
    # ==========================

    @staticmethod
    def listar_ciudades(db: Session):
        return db.exec(
            select(Ciudad)
        ).all()

    @staticmethod
    def crear_ciudad(
        db: Session,
        ciudad: Ciudad
    ):

        return BaseRepository.guardar(
            db,
            ciudad
        )

    # ==========================
    # TIPOS DE TURISMO
    # ==========================

    @staticmethod
    def listar_tipos(db: Session):
        return db.exec(
            select(TipoTurismo)
        ).all()

    @staticmethod
    def crear_tipo(
        db: Session,
        tipo: TipoTurismo
    ):

        return BaseRepository.guardar(
            db,
            tipo
        )