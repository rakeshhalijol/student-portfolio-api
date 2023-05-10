# Fastapi imports here.
from fastapi import Body, Depends, FastAPI, Request
from fastapi import status as http_resp_status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse, Response
from starlette.exceptions import HTTPException as StarletteHTTPException


# Any other imports which are not related to fastapi.
import os

# Folder based imports here
from src.config import (
    APP_NAME,
    APP_DESCRIPTION
)
from src.urls import (
    WELCOME_PATH,
    USER_CREATE_PATH
)
from src.utils.openapi import (
    _patch_http_validation_error,
    setup_swagger_auth
)
from src.database.interaction import (create_user)
from src.models.requests import (
    UserDataModel
)
from src.models.responses import (
    UserDataModelResponse
)

# Intialise a instance of a FastAPI with proper conventions.
app = FastAPI(title=APP_NAME, description=APP_DESCRIPTION)
app.openapi = _patch_http_validation_error(app, app.openapi)

# Permissions for CORS when app running locally.
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---Handle exceptions ---


@app.exception_handler(StarletteHTTPException)
async def handle_http_exception(request: Request, exc: StarletteHTTPException):
    return JSONResponse(content=exc.detail, status_code=exc.status_code, media_type="application/problem+json")


@app.exception_handler(Exception)
async def handle_unexpected_exception(request: Request, exc: Exception):
    return JSONResponse(
        content={
            "title": "Unexpected exception occurred",
            "detail": f"{type(exc).__name__}: {exc}",
            "status": http_resp_status.HTTP_500_INTERNAL_SERVER_ERROR,
        },
        status_code=http_resp_status.HTTP_500_INTERNAL_SERVER_ERROR,
        media_type="application/problem+json",
    )


@app.exception_handler(RequestValidationError)
async def handle_validation_exception(request: Request, exc: RequestValidationError):
    return JSONResponse(
        content={
            "title": "Validation Error",
            "detail": "Invalid endpoint input(s) detected",
            "status": http_resp_status.HTTP_422_UNPROCESSABLE_ENTITY,
            "error_specs": exc.errors(),
        },
        status_code=http_resp_status.HTTP_422_UNPROCESSABLE_ENTITY,
        media_type="application/problem+json",
    )
SWAGGER_ENDPOINT = os.getenv("SWAGGER_ENDPOINT", "/docs")


@app.get("/", include_in_schema=False)
def redirect_to_swagger():
    """Redirect to Swagger UI when accessing the root endpoint"""
    return RedirectResponse(SWAGGER_ENDPOINT)

# --- END-POINTS ---


@app.get(WELCOME_PATH)
def welcome():
    return {"msg": "Welcome to student-portfolio-api"}


@app.post(
    USER_CREATE_PATH,
    tags=["Credentials"],
    description="This end point helps to store user data in database"

)
def create_new_user(userData: UserDataModel) -> UserDataModelResponse:
    inserted_id = create_user(dict(userData))
    return {"status": "OK", "inserted_id": inserted_id}


# --- WEB-SOCKETS ---
