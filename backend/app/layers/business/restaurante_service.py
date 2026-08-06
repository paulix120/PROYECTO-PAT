from fastapi import HTTPException
from sqlmodel import Session

from app.layers.data.restaurante_repository import RestauranteRepository
from app.layers.data.destino_repository import DestinoRepository

from app.layers.models.restaurante import (
    Restaurante,
    RestauranteCreate,
    RestauranteUpdate
)

from app.core.maps import obtener_coordenadas_exactas


class RestauranteService:


    @staticmethod
    def listar(
        db: Session
    ):

        return RestauranteRepository.listar(db)


    @staticmethod
    def obtener(
        db: Session,
        restaurante_id: int
    ):

        restaurante = RestauranteRepository.obtener(
            db,
            restaurante_id
        )

        if not restaurante:

            raise HTTPException(
                status_code=404,
                detail="Restaurante no encontrado."
            )

        return restaurante


    @staticmethod
    def crear(
        db: Session,
        data: RestauranteCreate
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

        restaurante = Restaurante.model_validate(data)

        if ciudad:

            latitud, longitud = obtener_coordenadas_exactas(
                nombre=restaurante.nombre,
                direccion=restaurante.direccion,
                ciudad=ciudad.nombre
            )

            restaurante.latitud = latitud
            restaurante.longitud = longitud

        return RestauranteRepository.crear(
            db,
            restaurante
        )


    @staticmethod
    def actualizar(
        db: Session,
        restaurante_id: int,
        data: RestauranteUpdate
    ):

        restaurante = RestauranteRepository.obtener(
            db,
            restaurante_id
        )

        if not restaurante:

            raise HTTPException(
                status_code=404,
                detail="Restaurante no encontrado."
            )

        cambios = data.model_dump(
            exclude_unset=True
        )

        for campo, valor in cambios.items():

            setattr(
                restaurante,
                campo,
                valor
            )

        if restaurante.destino_id:

            destino = DestinoRepository.obtener_por_id(
                db,
                restaurante.destino_id
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
                    nombre=restaurante.nombre,
                    direccion=restaurante.direccion,
                    ciudad=ciudad.nombre
                )

                restaurante.latitud = latitud
                restaurante.longitud = longitud

        return RestauranteRepository.actualizar(
            db,
            restaurante
        )


    @staticmethod
    def eliminar(
        db: Session,
        restaurante_id: int
    ):

        restaurante = RestauranteRepository.obtener(
            db,
            restaurante_id
        )

        if not restaurante:

            raise HTTPException(
                status_code=404,
                detail="Restaurante no encontrado."
            )

        restaurante.activo = False

        return RestauranteRepository.actualizar(
            db,
            restaurante
        )