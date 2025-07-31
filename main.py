# main.py

from fastapi import FastAPI
from pydantic import BaseModel
from manager import SongQueueManager
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins. You can replace with specific domains like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dummy library
song_library = [
    "Shape of You", "Believer", "Blinding Lights", "Perfect", "Despacito",
    "Rockstar", "Havana", "Closer", "Faded", "Let Her Go"
]
manager = SongQueueManager(song_library)

class SongRequest(BaseModel):
    user_id: str
    song_name: str
    from_user: str = ''
    dedicated_to: str = ''

class ReplaceSongRequest(BaseModel):
    user_id: str
    old_song: str
    new_song: str

@app.post("/add_song")
def add_song(req: SongRequest):
    return {"message": manager.add_song(req.user_id, req.song_name, req.from_user, req.dedicated_to)}

@app.post("/replace_song")
def replace_song(req: ReplaceSongRequest):
    return {"message": manager.remove_or_replace_song(req.user_id, req.old_song, req.new_song)}

@app.post("/disconnect/{user_id}")
def disconnect(user_id: str):
    manager.handle_disconnect(user_id)
    return {"message": f"{user_id} disconnected."}

@app.post("/reconnect/{user_id}")
def reconnect(user_id: str):
    manager.handle_reconnect(user_id)
    return {"message": f"{user_id} reconnected."}

@app.get("/queue")
def get_queue():
    return manager.get_queue()

@app.post("/play")
def play():
    return {"message": manager.play_song()}
