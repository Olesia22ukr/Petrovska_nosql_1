import os
import pprint
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ["MONGO_URI"]
client = MongoClient(MONGO_URI)
db = client["spotify"]

# Завдання 1 — explain() БЕЗ індексу
print("=== ЗАВДАННЯ 1: explain() БЕЗ індексу ===")
explain_before = db.command("explain", {
    "find": "tracks",
    "filter": {
        "track_genre": "pop",
        "audio_features.danceability": {"$gte": 0.7}
    },
    "sort": {"popularity": -1}
}, verbosity="executionStats")
stats = explain_before["executionStats"]
print(f"Переглянуто документів: {stats['totalDocsExamined']}")
print(f"Час виконання (мс): {stats['executionTimeMillis']}")
print(f"Стадія плану: {explain_before['queryPlanner']['winningPlan']['stage']}")

# Створюємо індекс
print("\n=== Створюємо індекс ===")
db["tracks"].create_index([
    ("track_genre", 1),
    ("audio_features.danceability", 1),
    ("popularity", -1)
])
print("Індекс створено!")

# explain() ПІСЛЯ індексу
print("\n=== ЗАВДАННЯ 1: explain() ПІСЛЯ індексу ===")
explain_after = db.command("explain", {
    "find": "tracks",
    "filter": {
        "track_genre": "pop",
        "audio_features.danceability": {"$gte": 0.7}
    },
    "sort": {"popularity": -1}
}, verbosity="executionStats")
stats = explain_after["executionStats"]
print(f"Переглянуто документів: {stats['totalDocsExamined']}")
print(f"Час виконання (мс): {stats['executionTimeMillis']}")
print(f"Стадія плану: {explain_after['queryPlanner']['winningPlan']['stage']}")

# Завдання 2 — Індекс для фонової музики
print("\n=== ЗАВДАННЯ 2: БЕЗ індексу ===")
explain_before2 = db.command("explain", {
    "find": "tracks",
    "filter": {
        "audio_features.instrumentalness": {"$gt": 0.5},
        "audio_features.speechiness": {"$lt": 0.1},
        "explicit": False
    }
}, verbosity="executionStats")
stats2 = explain_before2["executionStats"]
print(f"Переглянуто документів: {stats2['totalDocsExamined']}, Час: {stats2['executionTimeMillis']} мс")

db["tracks"].create_index([
    ("audio_features.instrumentalness", 1),
    ("audio_features.speechiness", 1),
    ("explicit", 1)
])
print("Індекс створено!")

print("\n=== ЗАВДАННЯ 2: ПІСЛЯ індексу ===")
explain_after2 = db.command("explain", {
    "find": "tracks",
    "filter": {
        "audio_features.instrumentalness": {"$gt": 0.5},
        "audio_features.speechiness": {"$lt": 0.1},
        "explicit": False
    }
}, verbosity="executionStats")
stats2 = explain_after2["executionStats"]
print(f"Переглянуто документів: {stats2['totalDocsExamined']}, Час: {stats2['executionTimeMillis']} мс")
print(f"Стадія плану: {explain_after2['queryPlanner']['winningPlan']['stage']}")

# Завдання 3 — Covered query
print("\n=== ЗАВДАННЯ 3: Covered query ===")
explain3 = db.command("explain", {
    "find": "tracks",
    "filter": {
        "track_genre": "pop",
        "popularity": {"$gte": 70}
    },
    "projection": {"track_genre": 1, "popularity": 1, "_id": 0}
}, verbosity="executionStats")
stats3 = explain3["executionStats"]
print(f"Переглянуто документів: {stats3['totalDocsExamined']}")
print(f"Переглянуто ключів індексу: {stats3['totalKeysExamined']}")
print(f"Час виконання (мс): {stats3['executionTimeMillis']}")
print(f"Стадія плану: {explain3['queryPlanner']['winningPlan']['stage']}")
