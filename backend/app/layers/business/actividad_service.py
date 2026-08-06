from fastapi import HTTPException
from sqlmodel import Session

from app.core.maps import obtener_coordenadas_exactas

from app.layers.data.actividad_repository import ActividadRepository
from app.layers.data.destino_repository import DestinoRepository

from app.layers.models.actividad import (
    Actividad,
    ActividadCreate,
    ActividadUpdate
)


class ActividadService:


    @staticmethod
    def listar(
        db: Session
    ):

        return ActividadRepository.listar(db)


    @staticmethod
    def obtener(
        db: Session,
        actividad_id: int
    ):

        actividad = ActividadRepository.obtener(
            db,
            actividad_id
        )

        if not actividad:

            raise HTTPException(
                status_code=404,
                detail="Actividad no encontrada."
            )

        return actividad


    @staticmethod
    def crear(
        db: Session,
        data: ActividadCreate
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

        actividad = Actividad.model_validate(data)

        if ciudad:

            latitud, longitud = obtener_coordenadas_exactas(
                nombre=actividad.nombre,
                direccion=actividad.direccion,
                ciudad=ciudad.nombre
            )

            actividad.latitud = latitud
            actividad.longitud = longitud

        return ActividadRepository.crear(
            db,
            actividad
        )


    @staticmethod
    def actualizar(
        db: Session,
        actividad_id: int,
        data: ActividadUpdate
    ):

        actividad = ActividadRepository.obtener(
            db,
            actividad_id
        )

        if not actividad:

            raise HTTPException(
                status_code=404,
                detail="Actividad no encontrada."
            )

        cambios = data.model_dump(
            exclude_unset=True
        )

        for campo, valor in cambios.items():

            setattr(
                actividad,
                campo,
                valor
            )

        if actividad.destino_id:

            destino = DestinoRepository.obtener_por_id(
                db,
                actividad.destino_id
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

                latitud, longitud = obtener_coordenadas_exactas(
                    nombre=actividad.nombre,
                    direccion=actividad.direccion,
                    ciudad=ciudad.nombre
                )

                actividad.latitud = latitud
                actividad.longitud = longitud

        return ActividadRepository.actualizar(
            db,
            actividad
        )


    @staticmethod
    def eliminar(
        db: Session,
        actividad_id: int
    ):

        actividad = ActividadRepository.obtener(
            db,
            actividad_id
        )

        if not actividad:

            raise HTTPException(
                status_code=404,
                detail="Actividad no encontrada."
            )

        actividad.activa = False

        return ActividadRepository.actualizar(
            db,
            actividad
        )