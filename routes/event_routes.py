import os
from flask import Blueprint, render_template
import sqlite3
import utils.event_scraper as scraper_utils
event_bp = Blueprint('event', __name__)
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'campusconnect.db')
DB_PATH = os.path.abspath(DB_PATH)  # Ensures full absolute path

@event_bp.route("/events")
def events():
    # Run the campus event scraper to refresh external_events
    scraper = scraper_utils.CampusEventScraper(
        db_path=DB_PATH,
        events_url="https://www.adrian.edu/calendar"
    )
    try:
        scraper.run()
    except Exception as e:
        # error prevention
        print("Error running CampusEventScraper:", e)

    # Opens a DB connection and queries the tables
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Fetch internal events - Example
    cursor.execute("SELECT title, location, date FROM events")
    internal_events = cursor.fetchall()
    # Print out values for debugging
    print(internal_events)

    # Fetch external events 
    cursor.execute("SELECT title, location, date, description FROM external_events")
    external_events = cursor.fetchall()




    

    conn.close()
    return render_template("events.html", internal_events=internal_events, external_events=external_events)