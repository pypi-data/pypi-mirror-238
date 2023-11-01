import asyncio

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from sona.core.inferencer import InferencerBase
from sona.core.messages.context import Context
from sona.settings import settings

from .messages import SonaResponse

INFERENCER_CLASS = settings.SONA_INFERENCER_CLASS

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@api.on_event("startup")
async def startup():
    api.inferencer: InferencerBase = InferencerBase.load_class(INFERENCER_CLASS)()
    api.inferencer.on_load()


@api.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, err: RequestValidationError):
    logger.warning(f"Client Error: {request}, {err.errors()}")
    resp = SonaResponse(code="400", message=str(err.errors()))
    return JSONResponse(status_code=400, content=resp.model_dump())


@api.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, err: Exception):
    logger.exception(f"Server Error: {request}")
    resp = SonaResponse(code="500", message=str(err))
    return JSONResponse(status_code=500, content=resp.model_dump())


@api.get("/ping")
async def ping():
    return SonaResponse(message="pong")


@api.post("/inference")
async def inference(ctx: Context):
    inferencer: InferencerBase = api.inferencer
    loop = asyncio.get_running_loop()
    next_ctx: Context = await loop.run_in_executor(None, inferencer.process, ctx)
    if next_ctx.is_failed:
        raise Exception("Internal Server Error")
    return SonaResponse(result=list(next_ctx.results.values())[0])
