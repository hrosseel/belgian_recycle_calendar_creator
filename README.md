# Belgian Recycle Calendar Creator

A Python script for creating a personalized recycling calendar using the [Recycle!](https://recycleapp.be) API. Only works for Belgian addresses.

# How to run in Python

0. Install Python dependencies (see [requirements.txt](requirements.txt))
1. Execute `python main.py` in a terminal and follow the prompts
2. Import the resulting calendar file (ics) in your favorite calendar application

Alternatively, you can use the Makefile: `make install-deps && make run`

# How to run in Docker

1. Start the Docker container by executing `docker-compose run --rm belgian_recycle_calendar_creator` and follow the prompts
2. Import the resulting calendar file (ics) in your favorite calendar application

Alternatively, you can use the Makefile: `make run-docker`

# How to run the executable

1. Download the [Unix executable](dist/be_recycle_calendar) and give it permission to execute using `chmod +x ./be_recycle_calendar`
2. Execute `./be_recycle_calendar` in a Unix terminal (macOS and Linux) and follow the prompts
3. Import the resulting calendar file (ics) in your favorite calendar application

Windows executables are currently not supported.

# Requirements

* Python 3.7 or higher
