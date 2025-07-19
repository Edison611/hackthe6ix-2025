from fastapi import FastAPI
from routes.ribbon import router as interview_router
from routes.test import router as test_router
from routes.recipients import router as recipients_router

app = FastAPI()

app.include_router(interview_router, prefix="")
app.include_router(test_router)
app.include_router(recipients_router)
