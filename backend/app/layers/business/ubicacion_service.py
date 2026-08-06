from fastapi import HTTPException, status
from sqlmodel import Session

from app.layers.data.ubicacion_repository import UbicacionRepository

from app.layers.models.destinos import (
    Departamento,
    DepartamentoCreate,

    Ciudad,
    CiudadCreate,

    TipoTurismo,
    TipoTurismoCreate
)


class UbicacionService:

    # =====================================================
    # DEPARTAMENTOS
    # =====================================================

    @staticmethod
    def listar_departamentos(db: Session):
        return UbicacionRepository.listar_departamentos(db)

    @staticmethod
    def crear_departamento(
        db: Session,
        data: DepartamentoCreate
    ):

        departamento = Departamento.model_validate(data)

        return UbicacionRepository.crear_departamento(
            db,
            departamento
        )

    # =====================================================
    # CIUDADES
    # =====================================================

    @staticmethod
    def listar_ciudades(db: Session):
        return UbicacionRepository.listar_ciudades(db)

    @staticmethod
    def crear_ciudad(
        db: Session,
        data: CiudadCreate
    ):

        departamento = UbicacionRepository.obtener_departamento(
            db,
            data.departamento_id
        )

        if not departamento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El departamento especificado no existe."
            )

        ciudad = Ciudad.model_validate(data)

        return UbicacionRepository.crear_ciudad(
            db,
            ciudad
        )

    # =====================================================
    # TIPOS DE TURISMO
    # =====================================================

    @staticmethod
    def listar_tipos(db: Session):
        return UbicacionRepository.listar_tipos(db)

    @staticmethod
    def crear_tipo(
        db: Session,
        data: TipoTurismoCreate
    ):

        tipo = TipoTurismo.model_validate(data)

        return UbicacionRepository.crear_tipo(
            db,
            tipo
        )