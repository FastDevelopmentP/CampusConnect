import requests
import re
import sqlite3
from bs4 import BeautifulSoup


# Start Class
class CampusEventScraper:
    # This class is responsible for:
    # Downloading HTML info from the Adrian College 
    # Parse events title, location, date, descriptin
    # Save the cleaned events in the external_events SQLite

    def __init__(self, db_path: str, events_url: str) -> None:
        # Store the path and URL of the events page
        self.db_path = db_path
        self.events_url = events_url

    # Network

    def fetch_html(self) -> str:
        # Send a GET request to the events URL and return HTML text
        # raise_for_status will throw an error if the request fails
        response = requests.get(self.events_url, timeout=10)
        response.raise_for_status()
        return response.text

    # Parsing

    def parse_events(self, html: str):
        # Take HTML strings into BeautifulSoup objects
        soup = BeautifulSoup(html, "html.parser")
        events = []

        event_cards = soup.select("#event-listing-hybrid a.event")

        for card in event_cards:
            # Pull title from <h3> tag inside the event card learned in 250 Rize Webdevelopment
            title_el = card.find("h3")
            if title_el:
                title = title_el.get_text(strip=True)
            else:
                title = card.get_text(strip=True)

            # Read the date from data-date attribute
            date = card.get("data-date", "").strip()

            # Try to find a child element that contains the location text
            location_el = card.find(class_="event-location")
            location = location_el.get_text(strip=True) if location_el else ""

            # find element that contains description
            desc_el = card.find(class_="event-description")
            description = desc_el.get_text(strip=True) if desc_el else ""

            # Use regex to collapse extra whitespace
            title = re.sub(r"\s+", " ", title)
            date = re.sub(r"\s+", " ", date)
            location = re.sub(r"\s+", " ", location)
            description = re.sub(r"\s+", " ", description)

            # Store each event as a tuple
            events.append((title, location, date, description))

        # Return the full list now that is has been parsed
        return events

    # Datbase

    def save_events(self, events) -> None:
        # Open connection to the SQLite database
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        # keep the latest scraped data
        cursor.execute("DELETE FROM external_events")

        # Insert all new events into the external_events table
        cursor.executemany(
            "INSERT INTO external_events (title, location, date, description) VALUES (?, ?, ?, ?)",
            events,
        )

        # Save changes and close the connection
        connection.commit()
        connection.close()

    # Public Pipeline

    def run(self) -> None:
        html = self.fetch_html()
        events = self.parse_events(html)

        if events:
            self.save_events(events)

