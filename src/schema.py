from typing import Any


CANONICAL_COLUMNS = [
    "flight_id",
    "flight_number",
    "flight_date",
    "departure_airport",
    "arrival_airport",
    "scheduled_departure_time",
    "scheduled_arrival_time",
    "airline",
]

REQUIRED_FIELDS = ["airline", "flight_number", "flight_date"]
DATETIME_FIELDS = ["scheduled_departure_time", "scheduled_arrival_time"]

def normalize_flight_payload(payload: dict[str, Any]) -> list[dict[str, Any]]:
    records = payload.get("data", [])
    normalized: list[dict[str, Any]] = []

    for record in records:
        flight = record.get("flight", {}) or {}
        departure = record.get("departure", {}) or {}
        arrival = record.get("arrival", {}) or {}
        airline = record.get("airline", {}) or {}

        normalized.append(
            {
                "flight_number": flight.get("number"),
                "flight_date": record.get("flight_date"),
                "departure_airport": departure.get("airport"),
                "arrival_airport": arrival.get("airport"),
                "scheduled_departure_time": departure.get("scheduled"),
                "scheduled_arrival_time": arrival.get("scheduled"),
                "airline": airline.get("name"),
            }
        )

    return normalized
