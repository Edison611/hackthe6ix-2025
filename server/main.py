from fastapi import FastAPI
from routes.ribbon import router as interview_router

app = FastAPI()

app.include_router(interview_router, prefix="")
