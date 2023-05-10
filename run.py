import uvicorn

from src.config import (
    LOCAL_APP,
    APP_WORKER,
    APP_HOST,
    APP_PORT
)

if __name__ == "__main__":
    if LOCAL_APP:
        uvicorn.run("src.main:app", host=APP_HOST,
                    port=APP_PORT, workers=APP_WORKER, reload=True)
    else:
        uvicorn.run("src.main:app", host=APP_HOST,
                    port=APP_PORT, workers=APP_WORKER)
