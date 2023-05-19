# Fastapi imports here.
from fastapi import Depends, FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.security import OAuth2PasswordRequestForm

# Any other imports which are not related to fastapi.
import os

# Folder based imports here
from src.utils.auth import (
    authenticate_user,
    validate_token
)

from src.config import (
    APP_NAME,
    APP_DESCRIPTION
)

from src.utils.openapi import (
    _patch_http_validation_error
)
from src.apps.exceptions.exception import (
    handle_validation_exception,
    handle_http_exception,
    handle_unexpected_exception)
from src.apps.credentials.views import router as credentials_router


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
app.add_exception_handler(StarletteHTTPException, handle_http_exception)
app.add_exception_handler(Exception, handle_unexpected_exception)
app.add_exception_handler(RequestValidationError, handle_validation_exception)
SWAGGER_ENDPOINT = os.getenv("SWAGGER_ENDPOINT", "/docs")


@app.get("/", include_in_schema=False)
def redirect_to_swagger():
    """Redirect to Swagger UI when accessing the root endpoint"""
    return RedirectResponse(SWAGGER_ENDPOINT)

# --- END-POINTS ---


@app.post("/oauth/token", include_in_schema=False)
def token(formData: OAuth2PasswordRequestForm = Depends()):
    access_token = authenticate_user(formData.username, formData.password)
    if access_token is not None:
        return {"access_token": access_token}
    raise HTTPException(
        status_code=401,
        detail={
            "title": "Authorization Header Missing",
            "details": "Authorization token not found in request header",
            "status": 401,
        },
    )


app.include_router(credentials_router, prefix="/credentials",
                   dependencies=[Depends(validate_token)])


# --- WEB-SOCKETS ---
