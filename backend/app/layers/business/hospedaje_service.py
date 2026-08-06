from fastapi import HTTPException
from app.layers.data.destino_repository import DestinoRepository
from sqlmodel import Session
from app.layers.data.hospedaje_repository import HospedajeRepository
from app.core.maps import obtener_coordenadas_exactas
from app.layers.models.destinos import Ciudad

from app.layers.models.hospedaje import (
    Hospedaje,
    HospedajeCreate,
    HospedajeUpdate
)


class HospedajeService:


    @staticmethod
    def listar(
        db: Session
    ):

        return HospedajeRepository.listar(db)


    @staticmethod
    def obtener(
        db: Session,
        hospedaje_id: int
    ):

        hospedaje = HospedajeRepository.obtener(
            db,
            hospedaje_id
        )

        if not hospedaje:

            raise HTTPException(
                status_code=404,
                detail="Hospedaje no encontrado."
            )

        return hospedaje


    @staticmethod
    @staticmethod
    def crear(
        db: Session,
        data: HospedajeCreate
    ):

        destino = DestinoRepository.obtener_por_id(
            db,
            data.destino_id
        )

        if not destino:

            raise HTTPException(
                status_code=404,
                detail="El destino no existe."
            )

        ciudad = DestinoRepository.obtener_ciudad(
            db,
            destino.ciudad_id
        )

        hospedaje = Hospedaje.model_validate(
            data
        )

        if ciudad:

            lat, lng = obtener_coordenadas_exactas(
                nombre=hospedaje.nombre,
                direccion=hospedaje.direccion,
                ciudad=ciudad.nombre
            )

            hospedaje.latitud = lat
            hospedaje.longitud = lng

        return HospedajeRepository.crear(
            db,
            hospedaje
        )


    @staticmethod
    @staticmethod
    def actualizar(
        db: Session,
        hospedaje_id: int,
        data: HospedajeUpdate
    ):

        hospedaje = HospedajeRepository.obtener(
            db,
            hospedaje_id
        )

        if not hospedaje:

            raise HTTPException(
                status_code=404,
                detail="Hospedaje no encontrado."
            )

        cambios = data.model_dump(
            exclude_unset=True
        )

        for campo, valor in cambios.items():

            setattr(
                hospedaje,
                campo,
                valor
            )

        destino = DestinoRepository.obtener_por_id(
            db,
            hospedaje.destino_id
        )

        if not destino:

            raise HTTPException(
                status_code=404,
                detail="El destino no existe."
            )

        ciudad = DestinoRepository.obtener_ciudad(
            db,
            destino.ciudad_id
        )

        if ciudad:

            if (
                "nombre" in cambios
                or "direccion" in cambios
                or "destino_id" in cambios
            ):

                lat, lng = obtener_coordenadas_exactas(
                    nombre=hospedaje.nombre,
                    direccion=hospedaje.direccion,
                    ciudad=ciudad.nombre
                )

                hospedaje.latitud = lat
                hospedaje.longitud = lng

        return HospedajeRepository.actualizar(
            db,
            hospedaje
        )


    @staticmethod
    def eliminar(
        db: Session,
        hospedaje_id: int
    ):

        hospedaje = HospedajeRepository.obtener(
            db,
            hospedaje_id
        )

        if not hospedaje:

            raise HTTPException(
                status_code=404,
                detail="Hospedaje no encontrado."
            )

        hospedaje.activo = False

        return HospedajeRepository.actualizar(
            db,
            hospedaje
        )