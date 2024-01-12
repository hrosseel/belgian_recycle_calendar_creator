import json
import os

import click
import datetime

from lib import (authenticate, create_calendar, fetch_address_ids,
                 fetch_collections)


@click.command()
@click.option("-s", "--streetname", type=str, required=True,
              help="The street name for which you would like to generate the "
              "recycle calendar", prompt="Please enter your streetname")
@click.option("-n", "--number", type=int, required=True,
              help="The housenumber for which you would like to generate the "
              "recycle calendar", prompt="Please enter your housenumber "
              "(without apt./bus suffix)")
@click.option("-p", "--postalcode", type=int, required=True,
              help="The postal code for which you would like to generate the "
              "recycle calendar", prompt="Please enter your postal code")
@click.option("-l", "--lang", type=click.Choice(['nl', 'fr', 'en'],
              case_sensitive=False), default='en', required=False,
              help="The preferred language of the recycle "
              "calendar. Options are: 'nl', 'fr', and 'en'. Defaults to 'en'.",
              prompt="Please specify your preferred language")
def click_main(streetname, number, postalcode, lang='en', year=None):

    year = datetime.datetime.now().year

    filedir = os.path.dirname(__file__)
    # Load config
    config = json.load(open(os.path.join(filedir, "config.json"), 'r'))
    # Authenticate with api
    auth_headers = authenticate(config)
    # Get address IDs
    address_ids = fetch_address_ids(auth_headers, config, streetname, number,
                                    postalcode)

    # Get collections for address
    collections = fetch_collections(auth_headers, config, address_ids,
                                    f"{year}-01-01", f"{year}-12-31")
    # Create calendar
    calendar = create_calendar(collections, lang)

    filename = f"recycle_calendar_{streetname}_{number}.ics"

    print(f"Done! Writing calendar to file: {filename}")
    with open(filename, 'w', encoding='utf-8') as my_file:
        my_file.writelines(calendar.serialize_iter())


click_main()
