import datetime
import requests as req
from icalendar import Calendar, Event


def fetch_address_ids(
    auth_headers: dict, config: dict, streetname: str, number: int, postalcode: int
) -> dict:
    zip_resp = req.get(
        config["api_endpoint"] + "/zipcodes", {"q": postalcode}, headers=auth_headers
    )
    if zip_resp.status_code == 200:
        zip_json = zip_resp.json()
        zip_id = ""
        for item in zip_json["items"]:
            if int(item["code"]) == postalcode:
                zip_id = item["id"]
                break
        if zip_id == "":
            raise Exception(
                "Could not find the right zip code." f"Zip code = {postalcode}"
            )
    else:
        raise Exception(
            "Error occurred while fetching zipcode id. " f"[HTTP {zip_resp.status_code}]"
        )

    street_resp = req.post(
        config["api_endpoint"] + "/streets",
        params={"q": streetname, "zipcodes": zip_id},
        headers=auth_headers,
    )
    if street_resp.status_code == 200:
        street_json = street_resp.json()
        street_id = ""
        for item in street_json["items"]:
            if streetname in item["names"].values():
                street_id = item["id"]
                break
        if street_id == "":
            raise Exception(
                "Could not find the right street name. " f"Street name = {streetname}"
            )
    else:
        raise Exception(
            "Error occurred while fetching street id. "
            f"[HTTP {street_resp.status_code}]"
        )

    return {"zip": zip_id, "street": street_id, "housenumber": number}


def fetch_collections(
    auth_headers: dict, config: dict, address_ids: dict, from_date: str, to_date: str
) -> dict:
    req_params = {
        "zipcodeId": address_ids["zip"],
        "streetId": address_ids["street"],
        "houseNumber": address_ids["housenumber"],
        "fromDate": from_date,
        "untilDate": to_date,
        "size": "200",
    }
    collection_resp = req.get(
        config["api_endpoint"] + "/collections", req_params, headers=auth_headers
    )

    if collection_resp.status_code == 200:
        collections = collection_resp.json()
    else:
        raise Exception(
            "Something went wrong while fetching collections."
            f"[{collection_resp.status_code}]"
        )
    return collections


def create_calendar(collections, lang, set_day_events) -> Calendar:
    collection_msg = {
        "nl": "Ophaling van ",
        "fr": "Collecte de ",
        "en": "Collection of ",
    }
    calendar = Calendar()
    calendar.add("prodid", "-//Belgian Recycle Calendar//EN")
    calendar.add("version", "2.0")
    for item in collections["items"]:
        if item.get("exception", {}).get("replacedBy") is None:
            e = Event()
            if item["type"] == "collection":
                e.add("summary", collection_msg[lang] + item["fraction"]["name"][lang])
                date = datetime.date.fromisoformat(item["timestamp"][:10])
                if set_day_events:
                    e.add("dtstart", date)
                else:
                    e.add(
                        "dtstart", datetime.datetime.combine(date, datetime.time(6, 0))
                    )
                    e.add("duration", datetime.timedelta(hours=1))
            elif item["type"] == "event":
                e.add("summary", item["event"]["title"][lang])
                e.add("description", item["event"]["description"][lang] + "\n\n")
                e.add("dtstart", datetime.date.fromisoformat(item["timestamp"][:10]))
                e.add("location", item["event"]["introduction"][lang])
                e.add("url", item["event"]["externalLink"][lang])
            calendar.add_component(e)
    return calendar
