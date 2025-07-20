from fastapi import FastAPI
from routes.ribbon import router as interview_router
from routes.test import router as test_router
from routes.recipients import router as recipients_router
from routes.roles import router as roles_router
from routes.questions import router as questions_router
from routes.responses import router as responses_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",  # your frontend origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # you can also use ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(interview_router, prefix="")
app.include_router(test_router)
app.include_router(recipients_router)
app.include_router(roles_router)  
app.include_router(questions_router)
app.include_router(responses_router)