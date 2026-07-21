import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ["MONGO_URI"]
client = MongoClient(MONGO_URI)
db = client["spotify"]

# Завдання 1 — Топ-10 виконавців
print("=== ЗАВДАННЯ 1: Топ-10 виконавців за середньою популярністю ===")
pipeline = [
    {"$unwind": "$artists"},
    {"$group": {
        "_id": "$artists",
        "track_count": {"$sum": 1},
        "avg_popularity": {"$avg": "$popularity"}
    }},
    {"$match": {"track_count": {"$gte": 5}}},
    {"$sort": {"avg_popularity": -1}},
    {"$limit": 10},
    {"$project": {
        "artist": "$_id",
        "avg_popularity": {"$round": ["$avg_popularity", 1]},
        "_id": 0
    }}
]
results = list(db["tracks"].aggregate(pipeline))
for i, r in enumerate(results, 1):
    print(f"{i}. {r['artist']} — середня популярність: {r['avg_popularity']}")

# Завдання 2 — Розподіл за настроєм
print("\n=== ЗАВДАННЯ 2: Розподіл треків за настроєм ===")
pipeline = [
    {"$addFields": {
        "mood": {"$switch": {"branches": [
            {"case": {"$and": [
                {"$gte": ["$audio_features.valence", 0.5]},
                {"$gte": ["$audio_features.energy", 0.5]}
            ]}, "then": "happy"},
            {"case": {"$and": [
                {"$lt": ["$audio_features.valence", 0.5]},
                {"$gte": ["$audio_features.energy", 0.5]}
            ]}, "then": "angry"},
            {"case": {"$and": [
                {"$gte": ["$audio_features.valence", 0.5]},
                {"$lt": ["$audio_features.energy", 0.5]}
            ]}, "then": "calm"},
        ], "default": "sad"}}
    }},
    {"$group": {"_id": "$mood", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}
]
results = list(db["tracks"].aggregate(pipeline))
for r in results:
    print(f"{r['_id']:10} — {r['count']} треків")

# Завдання 3 — Найтанцювальніший жанр
print("\n=== ЗАВДАННЯ 3: Найтанцювальніший жанр ===")
pipeline = [
    {"$group": {
        "_id": "$track_genre",
        "avg_danceability": {"$avg": "$audio_features.danceability"},
        "avg_energy": {"$avg": "$audio_features.energy"},
        "avg_valence": {"$avg": "$audio_features.valence"},
        "count": {"$sum": 1}
    }},
    {"$match": {"count": {"$gte": 100}}},
    {"$sort": {"avg_danceability": -1}},
    {"$limit": 10},
    {"$project": {
        "genre": "$_id",
        "avg_danceability": {"$round": ["$avg_danceability", 3]},
        "avg_energy": {"$round": ["$avg_energy", 3]},
        "avg_valence": {"$round": ["$avg_valence", 3]},
        "count": 1,
        "_id": 0
    }}
]
results = list(db["tracks"].aggregate(pipeline))
for i, r in enumerate(results, 1):
    print(f"{i}. {r['genre']:15} | danceability: {r['avg_danceability']} | energy: {r['avg_energy']} | valence: {r['avg_valence']} | треків: {r['count']}")
