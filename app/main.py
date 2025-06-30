import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from app.controller.master_controller import MasterController
from app.db.postgres.psql_conn_pool import init_pg_pool, close_pg_pool
from app.utils.app_utils import ensure
from app.utils.global_exception_handler import global_exception_handler
from app.utils.application_constants import controller_package, db_url_key, db_details_not_found, main_path_key
from app.utils.env_loader import load_environment
from app.config.logging_config import logger
from app.utils.import_util import load_package

load_environment()
load_package(controller_package)

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_url = os.getenv(db_url_key)
    ensure(lambda: db_url is not None, db_details_not_found)
    logger.info("App is starting up…")
    await init_pg_pool(db_url)
    yield
    await close_pg_pool()
    logger.info("App is shutting down…")

app = FastAPI(lifespan=lifespan)
app.add_exception_handler(Exception, global_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(MasterController.router)

def main():
    uvicorn.run(
        os.getenv(main_path_key),
        host=os.getenv("HOST", "localhost"),
        port=int(os.getenv("PORT", 8081)),
        reload=os.getenv("RELOAD", "false").lower() == "true",
        log_level=os.getenv("LOG_LEVEL", "info")
    )

if __name__ == "__main__":
    main()
