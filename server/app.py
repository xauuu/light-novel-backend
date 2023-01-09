from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from server.routes.novel import router as NovelRouter
from server.routes.chapter import router as ChapterRouter
from server.routes.auth import router as AuthRouter
from server.routes.summarize import router as SummarizeRouter
from server.config.config import settings

app = FastAPI()

origins = ["https://light-novel.vercel.app","http://localhost:3000", "http://localhost:8000", "light-novel.vercel.app", "localhost:3000", "localhost:8000"]
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
app.include_router(SummarizeRouter, tags=["Summarize"], prefix="/summarize")

@app.get("/audio/{file_name}")
async def get_audio(file_name: str):
    return FileResponse(f"server/audio/{file_name}")
