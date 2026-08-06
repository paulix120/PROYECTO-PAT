from fastapi import HTTPException, status
from sqlmodel import Session

from app.core.maps import obtener_coordenadas_exactas

from app.layers.data.destino_repository import DestinoRepository

from app.layers.models.destinos import (
    Destino,
    DestinoCreate,
    DestinoUpdate
)


class DestinoService: 

    @staticmethod
    def listar(db: Session):
        return DestinoRepository.listar(db)

    @staticmethod
    def obtener_por_id(
        db: Session,
        destino_id: int
    ):

        destino = DestinoRepository.obtener_por_id(
            db,
            destino_id
        )

        if not destino or not destino.activo:
            raise HTTPException(
                status_code=404,
                detail="El destino no existe."
            )

        return destino

    @staticmethod
    def crear(
        db: Session,
        data: DestinoCreate
    ):

        ciudad = DestinoRepository.obtener_ciudad(
            db,
            data.ciudad_id
        )

        if not ciudad:
            raise HTTPException(
                status_code=404,
                detail="La ciudad especificada no existe."
            )

        destino = Destino.model_validate(data)

        if destino.latitud is None or destino.longitud is None:

            lat, lng = obtener_coordenadas_exactas(
                nombre=destino.nombre,
                direccion=destino.direccion,
                ciudad=ciudad.nombre
            )

            if lat is not None and lng is not None:
                destino.latitud = lat
                destino.longitud = lng

        return DestinoRepository.crear(
            db,
            destino
        )

    @staticmethod
    def actualizar(
        db: Session,
        destino_id: int,
        data: DestinoUpdate
    ):

        destino = DestinoRepository.obtener_por_id(
            db,
            destino_id
        )

        if not destino or not destino.activo:
            raise HTTPException(
                status_code=404,
                detail="El destino no existe."
            )

        datos = data.model_dump(exclude_unset=True)

        for campo, valor in datos.items():
            setattr(destino, campo, valor)

        ciudad = DestinoRepository.obtener_ciudad(
            db,
            destino.ciudad_id
        )

        if (
            "nombre" in datos
            or "direccion" in datos
        ) and (
            "latitud" not in datos
            and "longitud" not in datos
        ):

            if ciudad:

                lat, lng = obtener_coordenadas_exactas(
                    nombre=destino.nombre,
                    direccion=destino.direccion,
                    ciudad=ciudad.nombre
                )

                if lat is not None and lng is not None:
                    destino.latitud = lat
                    destino.longitud = lng

        return DestinoRepository.actualizar(
            db,
            destino
        )

    @staticmethod
    def eliminar(
        db: Session,
        destino_id: int
    ):

        destino = DestinoRepository.obtener_por_id(
            db,
            destino_id
        )

        if not destino or not destino.activo:
            raise HTTPException(
                status_code=404,
                detail="El destino no existe."
            )

        return DestinoRepository.eliminar(
            db,
            destino
        )