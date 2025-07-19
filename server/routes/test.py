from fastapi import APIRouter

router = APIRouter()    

@router.get("/")
def test():
    return { "test": "test" }

@router.post("/")
def post_test(test: str):
    return { "test": test }
