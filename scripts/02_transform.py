import os
import pprint
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ["MONGO_URI"]
client = MongoClient(MONGO_URI)
db = client["spotify"]

db["tracks"].drop()

pipeline = [
    {"$project": {
        "track_id": 1,
        "track_name": 1,
        "album_name": 1,
        "explicit": 1,
        "popularity": 1,
        "duration_ms": 1,
        "track_genre": 1,
        "artists_raw": "$artists",
        "danceability": 1,
        "energy": 1,
        "loudness": 1,
        "speechiness": 1,
        "acousticness": 1,
        "instrumentalness": 1,
        "liveness": 1,
        "valence": 1,
