from fastapi import FastAPI
import uvicorn

from infrastructure.rest_api.routers.routers import routers

app = FastAPI()

app.include_router(router=routers)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8038)