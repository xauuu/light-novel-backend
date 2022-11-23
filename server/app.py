from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.routes.novel import router as NovelRouter
from server.routes.chapter import router as ChapterRouter
from server.routes.auth import router as AuthRouter
from server.config.config import settings

origins = [
    settings.CLIENT_ORIGIN,
]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(AuthRouter, tags=['Auth'], prefix='/auth')
app.include_router(NovelRouter, tags=["Novel"], prefix="/novel")
app.include_router(ChapterRouter, tags=["Chapter"], prefix="/novel/chapter")
