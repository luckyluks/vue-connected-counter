from fastapi import FastAPI
from multiprocessing import Manager
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    # "http://127.0.0.1",
    # "http://127.0.0.1:8080",
    # "http://localhost",
    # "http://localhost:8080
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = Manager()

store = manager.dict()

store["counter"] = 0

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/counter")
async def getCounter():
    return {"counter": store["counter"]}

@app.post("/counter")
async def setCounter(counter: int):
    store["counter"] = counter
    return {"counter": store["counter"]}
