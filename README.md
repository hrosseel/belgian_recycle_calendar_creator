# Belgian Recycle Calendar Creator

Create a recycling calendar using the [Recycle!](https://recycleapp.be) API. Only works in Belgium.

# How to

0. Install dependencies (see [Requirements](#requirements))
1. Edit `config.json` file to include your address and preferred language (currently supports: 'nl', 'fr', and 'en')
2. Run the `create_calendar.py` file
3. Import the resulting calendar file (ics) in your favorite calendar application

# Requirements

* Python 3
* [ics](https://pypi.org/project/ics/) (`pip install ics`)
* [Requests](https://pypi.org/project/requests/) (`pip install requests`)