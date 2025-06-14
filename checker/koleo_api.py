import requests
from datetime import datetime
import urllib.parse
from django.utils.text import slugify

BRAND_IDS = [
    6, 51, 2, 29, 64, 28, 4, 10, 58, 14, 33, 57, 11, 12, 54, 47, 13,
    46, 43, 63, 49, 3, 9, 27, 38, 20, 18, 48, 1, 53, 8,
]
HEADERS = {
    "User-Agent": "koleo-seats-checker(https://github.com/pawelktk/koleo-seats-checker)",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "x-koleo-version": "2",
    "X-Requested-With": "XMLHttpRequest",
}


def find_connections(start_station: str, end_station: str, date_str: str, time_str: str, allowed_ids: list):
    """
    Wyszukuje połączenia i od razu sprawdza dla nich dostępne miejsca.
    """
    start_station_processed = start_station.replace("ł", "l").replace("Ł", "L")
    end_station_processed = end_station.replace("ł", "l").replace("Ł", "L")
    start_slug = slugify(start_station_processed)
    end_slug = slugify(end_station_processed)

    try:
        full_datetime_str = f"{date_str} {time_str}"
        search_datetime = datetime.strptime(full_datetime_str, "%Y-%m-%d %H:%M")
        formatted_date = search_datetime.strftime("%d-%m-%Y %H:%M:%S")
    except ValueError:
        print(f"Błędny format daty lub godziny: {date_str} {time_str}")
        return []

    params = {
        "query[date]": formatted_date,
        "query[start_station]": start_slug,
        "query[end_station]": end_slug,
        "query[brand_ids][]": BRAND_IDS,
        "query[only_direct]": "false",
        "query[only_purchasable]": "false",
    }
    query_string = urllib.parse.urlencode(params, doseq=True)
    url = f"https://koleo.pl/pl/connections?{query_string}"

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()

        trains_map = {train["id"]: train for train in data.get("trains", [])}
        processed_connections = []

        for conn in data.get("connections", []):
            if not conn.get("train_ids"):
                continue

            train_info = trains_map.get(conn["train_ids"][0], {})
            
            start_time = conn["start_date"].split(" ")[0][:5]
            end_time = conn["finish_date"].split(" ")[0][:5]

            available_seats = get_seat_availability(
                conn["id"], train_info.get("train_nr"), allowed_ids
            )

            processed_connections.append(
                {
                    "connection_id": conn["id"],
                    "start_time": start_time,
                    "end_time": end_time,
                    "travel_time": conn["travel_time"],
                    "train_nr": train_info.get("train_nr"),
                    "train_name": train_info.get("train_name"),
                    "train_brand": train_info.get("train_brand"),
                    "available_seats": available_seats,
                }
            )
        return processed_connections
    except (requests.RequestException, ValueError, requests.exceptions.JSONDecodeError) as e:
        print(f"Błąd podczas pobierania połączeń: {e}")
        return []


def get_seat_availability(connection_id: int, train_nr: int, allowed_ids: list):
    """
    Sprawdza dostępne miejsca dla konkretnego połączenia.
    """
    if not train_nr:
        print(f"Brak numeru pociągu dla połączenia {connection_id}, pomijam sprawdzanie miejsc.")
        return []

    url = f"https://koleo.pl/api/v2/main/seats_availability/{connection_id}/{train_nr}/5"
    headers = HEADERS.copy()
    headers["Referer"] = f"https://koleo.pl/traveloptions/{connection_id}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        seats = data.get("seats", [])
        available_seats = [
            s
            for s in seats
            if s.get("state") == "FREE"
            and (
                s.get("special_compartment_type_id") is None
                or s.get("special_compartment_type_id") in allowed_ids
            )
        ]
        return available_seats
    except (requests.RequestException, ValueError) as e:
        if isinstance(e, requests.HTTPError) and e.response.status_code == 404:
            print(f"Brak możliwości rezerwacji miejsc dla pociągu {train_nr} (połączenie {connection_id}).")
        else:
            print(f"Błąd podczas sprawdzania miejsc dla {connection_id}: {e}")
        return []