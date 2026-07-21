import os
import pprint
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ["MONGO_URI"]
client = MongoClient(MONGO_URI)
db = client["spotify"]

# Завдання 1 — Треки для вечірки
print("=== ЗАВДАННЯ 1: Треки для вечірки ===")
results = list(db["tracks"].find(
    {
        "audio_features.danceability": {"$gt":
