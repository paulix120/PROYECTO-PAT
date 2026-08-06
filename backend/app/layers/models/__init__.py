from .auth import (
    User,
    UserCreate,
    UserLogin,
    UserResponse,
    Token,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from .destinos import (
    Departamento,
    DepartamentoCreate,
    DepartamentoResponse,

    Ciudad,
    CiudadCreate,
    CiudadResponse,

    TipoTurismo,
    TipoTurismoCreate,
    TipoTurismoResponse,

    Destino,
    DestinoResponse,
    DestinoCreate,
    DestinoUpdate,
)

from .hospedaje import (
    Hospedaje,
    HospedajeCreate,
    HospedajeUpdate,
    HospedajeResponse,
)
from .restaurante import (
    Restaurante,
    RestauranteCreate,
    RestauranteUpdate,
    RestauranteResponse
)
from .actividad import (
    Actividad,
    ActividadCreate,
    ActividadUpdate,
    ActividadResponse
)
from .plan_viaje import (
    PlanViaje,
    PlanViajeCreate,
    PlanViajeUpdate,
    PlanViajeResponse,
)