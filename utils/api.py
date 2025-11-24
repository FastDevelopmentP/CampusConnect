import requests
import re
import sqlite3

# Create API class.
class TrademarkAPIClient:
    # Calls the MarkerAPI trademark search endpoint, parses JSON,
    # cleans the data, and saves it into the api_data table.

    def __init__(
        self,
        db_path: str,
        username: str,
        password: str,
        search_term: str,
        status: str = "active",
        start: int = 1,
    ) -> None:
        self.db_path = db_path
        self.username = username
        self.password = password
        self.search_term = search_term
        self.status = status
        self.start = start

        # Base URL for the MarkerAPI 
        self.base_url = "https://app.rize.education/courses/4471/resource/943a4d86-52a2-4eea-b721-5657e11446a7?weekId=10702"

    # Network

    def fetch_json(self):
        # Build full MarkerAPI URL:
        # https://markerapi.com/api/v2/trademarks/trademark/{search}/status/{status}/start/{start}/username/{user}/password/{pass}
        safe_search = self.search_term.replace(" ", "%20")
        url = (
            f"{self.base_url}/{safe_search}"
            f"/status/{self.status}"
            f"/start/{self.start}"
            f"/username/{self.username}"
            f"/password/{self.password}"
        )

        # Show the exact URL
        print("Requesting MarkerAPI URL:", url)

        # Send the request to MarkerAPI
        response = requests.get(url, timeout=10)

        # Debug prints 
        print("MarkerAPI status code:", response.status_code)
        print("MarkerAPI raw text (first 500 chars):")
        print(response.text[:500])

        # Raise if error
        response.raise_for_status()

        # Attept to parse JSON
        try:
            data = response.json()
            print("Parsed JSON type:", type(data))
            if isinstance(data, dict):
                print("Top-level JSON keys:", list(data.keys()))
            return data
        except ValueError:
            print("Response was not valid JSON, returning empty dict")
            return {}



    # Parsing

    def parse_records(self, data):
        records = []

        trademarks = data.get("trademarks", []) if isinstance(data, dict) else []

        for item in trademarks:
            raw_name = item.get("trademark") or item.get("wordmark") or ""
            raw_serial = item.get("serialnumber") or ""
            raw_owner = item.get("owner") or ""
            raw_status = item.get("status") or ""
            raw_filing_date = item.get("filingdate") or ""
            raw_registration_date = item.get("regdate") or ""

            trademark_name = re.sub(r"\s+", " ", str(raw_name)).strip()
            serial_number = re.sub(r"\s+", " ", str(raw_serial)).strip()
            owner = re.sub(r"\s+", " ", str(raw_owner)).strip()
            status = re.sub(r"\s+", " ", str(raw_status)).strip()
            filing_date = re.sub(r"\s+", " ", str(raw_filing_date)).strip()
            registration_date = re.sub(r"\s+", " ", str(raw_registration_date)).strip()

            records.append(
                (
                    trademark_name,
                    serial_number,
                    owner,
                    status,
                    filing_date,
                    registration_date,
                )
            )

        return records

    # Database 

    def save_records(self, records) -> None:
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM api_data")

        cursor.executemany(
            """
            INSERT INTO api_data (
                trademark_name,
                serial_number,
                owner,
                status,
                filing_date,
                registration_date
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            records,
        )

        connection.commit()
        connection.close()

    # Public pipeline 

    def run(self) -> None:
        data = self.fetch_json()
        records = self.parse_records(data)

        if records:
            self.save_records(records)

