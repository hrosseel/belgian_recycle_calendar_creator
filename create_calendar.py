import json

import requests as req
from ics import Calendar, Event


def authenticate(config: dict) -> dict:
    headers = config["headers"]
    at_resp = req.get(config["api_endpoint"] + "/access-token",
                      headers=headers)

    if at_resp.status_code == 200:
        resp_json = at_resp.json()
        access_token = resp_json["accessToken"]
        headers["Authorization"] = access_token
    else:
        raise Exception("Error occured while requesting access-token. "
                        f"[{at_resp.status_code}]")
    return headers


def fetch_address(auth_headers: dict, config: dict):
    zip_resp = req.get(config["api_endpoint"] + "/zipcodes",
                       {"q": config["zipcode"]},
                       headers=auth_headers)
    if zip_resp.status_code == 200:
        zip_json = zip_resp.json()
        zip_id = ""
        for item in zip_json["items"]:
            if int(item["code"]) == config["zipcode"]:
                zip_id = item["id"]
                break
        if zip_id == "":
            raise Exception("Could not find the right zip code."
                            f"Zip code = {config['zipcode']}")
    else:
        raise Exception("Error occured while fetching zipcode id. "
                        f"[{zip_resp.status_code}]")

    street_resp = req.post(config["api_endpoint"] + "/streets",
                           params={"q": config["street_name"],
                                   "zipcodes": zip_id},
                           headers=auth_headers)
    if street_resp.status_code == 200:
        street_json = street_resp.json()
        street_id = ""
        for item in street_json["items"]:
            if item["name"] == config["street_name"]:
                street_id = item["id"]
                break
        if street_id == "":
            raise Exception("Could not find the right street name. "
                            f"Street name = {config['street_name']}")
    else:
        raise Exception("Error occured while fetching street id. "
                        f"[{street_resp.status_code}]")

    return {
        "zip": zip_id,
        "street": street_id,
        "housenumber": config["housenumber"]
        }


def fetch_collections(auth_headers: dict, config: dict, address: dict):
    req_params = {
        "zipcodeId": address["zip"],
        "streetId": address["street"],
        "houseNumber": address["housenumber"],
        "fromDate": config["from_date"],
        "untilDate": config["until_date"],
        "size": "200"
    }
    collection_resp = req.get(config["api_endpoint"] + "/collections",
                              req_params, headers=auth_headers)

    if collection_resp.status_code == 200:
        collections = collection_resp.json()
    else:
        raise Exception("Something went wrong while fetching collections."
                        f"[{collection_resp.status_code}]")
    return collections


def create_calendar(collections):
    lang = config["language"]
    if lang == "nl":
        collection_str = "Ophaling van "
    elif lang == "fr":
        collection_str = "Collecte de "
    else:
        collection_str = "Collection of "

    calendar = Calendar()
    for item in collections["items"]:
        if item.get("exception", {}).get("replacedBy") is None:
            e = Event()
            if item["type"] == "collection":
                e.name = collection_str + item["fraction"]["name"][lang]
                e.begin = item["timestamp"][:10] + "T06:00:00.000"
                e.duration = {"minutes": 15}
            elif item["type"] == "event":
                e.name = item["event"]["title"][lang]
                e.description = item["event"]["description"][lang] + "\n\n"
                e.begin = item["timestamp"]
                e.make_all_day()
                e.location = item["event"]["introduction"][lang]
                e.url = item["event"]["externalLink"][lang]
            calendar.events.add(e)
    return calendar


# Load config
config = json.load(open("config.json", 'r'))
# Authenticate with api
auth_headers = authenticate(config)
# Get address IDs
address = fetch_address(auth_headers, config)
# Get collections for address
collections = fetch_collections(auth_headers, config, address)
# Create calendar
calendar = create_calendar(collections)

print("Done! Writing to file...")
open("waste_calendar.ics", 'w').writelines(calendar)
