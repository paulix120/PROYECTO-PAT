from fastapi import HTTPException, status
from sqlmodel import Session

from app.layers.data.transporte_repository import TransporteRepository
from app.layers.models.transporte import (
    MedioTransporte,
    MedioTransporteCreate,
    MedioTransporteUpdate
)


class TransporteService:

    # ==========================================
    # LISTAR
    # ==========================================

    @staticmethod
    def listar(
        db: Session,
        usuario
    ):

        return TransporteRepository.listar_por_usuario(
            db,
            usuario.id
        )

    # ==========================================
    # OBTENER POR ID
    # ==========================================

    @staticmethod
    def obtener_por_id(
        db: Session,
        usuario,
        transporte_id: int
    ):

        transporte = TransporteRepository.obtener_por_id(
            db,
            transporte_id
        )

        if not transporte or not transporte.activo:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El medio de transporte no existe."
            )

        # Si es global lo puede ver cualquiera
        if transporte.usuario_id is None:
            return transporte

        # Si es suyo también
        if transporte.usuario_id == usuario.id:
            return transporte

        # Si es administrador puede verlo
        if usuario.rol_id == 2:
            return transporte

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para consultar este medio de transporte."
        )

    # ==========================================
    # CREAR
    # ==========================================

    @staticmethod
    def crear(
        db: Session,
        usuario,
        data: MedioTransporteCreate
    ):

        nuevo = MedioTransporte.model_validate(data)

        # Administrador -> transporte global
        if usuario.rol_id == 2:
            nuevo.usuario_id = None

        # Usuario -> transporte propio
        else:
            nuevo.usuario_id = usuario.id

        return TransporteRepository.guardar(
            db,
            nuevo
        )

    # ==========================================
    # ACTUALIZAR
    # ==========================================

    @staticmethod
    def actualizar(
        db: Session,
        usuario,
        transporte_id: int,
        data: MedioTransporteUpdate
    ):

        transporte = TransporteRepository.obtener_por_id(
            db,
            transporte_id
        )

        if not transporte:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El medio de transporte no existe."
            )

        # Solo administrador o propietario
        if usuario.rol_id != 2:

            if transporte.usuario_id != usuario.id:

                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permisos para modificar este medio de transporte."
                )

        cambios = data.model_dump(exclude_unset=True)

        for campo, valor in cambios.items():
            setattr(transporte, campo, valor)

        return TransporteRepository.actualizar(
            db,
            transporte
        )

    # ==========================================
    # ELIMINAR
    # ==========================================

    @staticmethod
    def eliminar(
        db: Session,
        usuario,
        transporte_id: int
    ):

        transporte = TransporteRepository.obtener_por_id(
            db,
            transporte_id
        )

        if not transporte:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El medio de transporte no existe."
            )

        # Solo administrador o propietario
        if usuario.rol_id != 2:

            if transporte.usuario_id != usuario.id:

                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permisos para eliminar este medio de transporte."
                )

        return TransporteRepository.eliminar(
            db,
            transporte
        )