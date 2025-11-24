import sqlite3
import os

DB_PATH = "db/campusconnect.db"

# Removes existing DB for a clean seeding
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Creates tables manually or runs schema.sql
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    preferences TEXT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    location TEXT,
    date TEXT
)''')

# New table for scraped external campus events
c.execute('''CREATE TABLE IF NOT EXISTS external_events (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    location TEXT,
    date TEXT,
    description TEXT
)''')

# New table to hold public api data used AI to help with api integration.
c.execute('''CREATE TABLE IF NOT EXISTS api_data (
    id INTEGER PRIMARY KEY,
    trademark_name TEXT NOT NULL,
    serial_number TEXT,
    owner TEXT,
    status TEXT,
    filing_date TEXT,
    registration_date TEXT
)''')

# Create Users Seed Data
c.execute("INSERT INTO users (name, preferences) VALUES (?, ?)", ("Alice", "Aly"))
c.execute("INSERT INTO users (name, preferences) VALUES (?, ?)", ("Bob", "art, Bobby"))
c.execute("INSERT INTO users (name, preferences) VALUES (?, ?)", ("Charlie", "Chaz"))

# Internal Events Seed Data
c.execute("INSERT INTO events (title, location, date) VALUES (?, ?, ?)", ("Music Night", "Student Center", "2025-04-05"))
c.execute("INSERT INTO events (title, location, date) VALUES (?, ?, ?)", ("Hackathon", "Library", "2025-04-01"))
c.execute("INSERT INTO events (title, location, date) VALUES (?, ?, ?)", ("Art Exhibition", "Gallery", "2025-04-10"))

# External Events Seed Data (optional example data because I could not seem to get the api to show up)
external_events_sample = [
    ("Adrian Preview Day", "Adrian College Campus", "2025-04-10",
     "Visit campus, meet faculty, and learn about academic programs."),
    ("Bulldog Community Day", "Main Quad", "2025-04-15",
     "Community picnic with food, games, and music."),
    ("Career & Internship Fair", "Student Center", "2025-04-20",
     "Meet employers and learn about internships and jobs.")
]

# Sample API data seed rows for testing the /api route
api_data_sample = [
    ("FASTGAINZ", "12345678", "Fast Development LLC", "LIVE",
     "2024-01-10", "2024-06-15"),
    ("CAMPUSCONNECT", "87654321", "CampusConnect, Inc.", "PENDING",
     "2023-11-05", ""),
    ("BULLDOG BITES", "11223344", "Adrian College Dining", "LIVE",
     "2022-08-20", "2023-02-01")
]

c.executemany(
    "INSERT INTO api_data (trademark_name, serial_number, owner, status, filing_date, registration_date) VALUES (?, ?, ?, ?, ?, ?)",
    api_data_sample
)

c.executemany(
    "INSERT INTO external_events (title, location, date, description) VALUES (?, ?, ?, ?)",
    external_events_sample
)




conn.commit()
conn.close()