from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.authservice.routers import router as auth_router
from src.genservice.routers import router as gen_router

app = FastAPI(
    title="FeedbackGeneratorApplication"
)

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Authorization"
    ],
)

app.include_router(gen_router)
app.include_router(auth_router)
