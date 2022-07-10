from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from multiprocessing import Manager
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import logging

logger = logging.getLogger('uvicorn')

app = FastAPI()

origins = [
    "http://127.0.0.1",
    "http://127.0.0.1:8080",
    "http://localhost",
    "http://localhost:8080",
    "http://192.168.0.72:8080",
    "http://192.168.0.72",
    # "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        logger.info(f"ws client '{client_id}' connected")
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket, client_id: str):
        logger.info(f"ws client '{client_id}' disconnected")
        self.active_connections.remove(websocket)

    async def send_resposnse(self, message: str, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = Manager()
store = manager.dict()
store["counter"] = 0

manager = ConnectionManager()



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/counter")
async def getCounter():
    return {"counter": store["counter"]}


@app.post("/counter")
async def setCounter(counter: int):
    store["counter"] = counter

    await manager.broadcast({
        "type": f"database-update-event",
        "counter": store["counter"]
    })

    return {"counter": store["counter"]}


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)

    try:
        while True:
            data = await websocket.receive_text()
            # await manager.send_resposnse({
            #     "message": f"You wrote: {data}"
            # }, websocket)
            await manager.broadcast({
                "message": f"Client #{client_id} says: {data}",
                "counter": store["counter"]
            })
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)
        await manager.broadcast({
            "message": f"Client #{client_id} left the chat"
        })