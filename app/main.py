from fastapi import APIRouter, FastAPI

app = FastAPI()
router = APIRouter(prefix='/api')

# test
@app.get("/")
def test():
    return {"ping": "pong"}

app.include_router(router)