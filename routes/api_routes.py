import os
import sqlite3
from flask import Blueprint, render_template

# Used AI to help with the Api integration but I could not quite get it working
from utils.api import TrademarkAPIClient

api_bp = Blueprint("api", __name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "campusconnect.db")
DB_PATH = os.path.abspath(DB_PATH)


@api_bp.route("/api")
def api():
    # Read MarkerAPI username/password from environment variables
    marker_username = os.getenv("MARKER_USERNAME")
    marker_password = os.getenv("MARKER_PASSWORD")

    # avoid crashing
    if not marker_username or not marker_password:
        print("WARNING: MARKER_USERNAME or MARKER_PASSWORD not set; using seed data only.")
    else:
        try:
            client = TrademarkAPIClient(
                db_path=DB_PATH,
                username=marker_username,
                password=marker_password,
                search_term="FastGainz",  
                status="active",
                start=1,
            )
            client.run()
        except Exception as e:
            print("Error running TrademarkAPIClient:", e)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            trademark_name,
            serial_number,
            owner,
            status,
            filing_date,
            registration_date
        FROM api_data
        """
    )
    api_data = cursor.fetchall()

    conn.close()

    # HTML stuff left unchanged
    return render_template("api.html", api_data=api_data)
