.PHONY: all clean docker run-native

# Variables
DOCKER_COMPOSE_FILE = docker-compose.yml

# Default target
all: docker

# Build Docker container
docker:
	docker-compose build

# Clean up generated files
clean:
	rm -f *.ics

# Run the application using Docker
run-docker:
	docker-compose run --rm belgian_recycle_calendar_creator

# Install requirements
install-deps:
  pip install -r requirements.txt

# Run the application natively
run:
	python main.py
