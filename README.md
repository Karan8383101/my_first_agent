# my_first_agent

A collection of small Python agent examples.

## Run the calculator

Use Python to run the app:

```bash
python calculator.py
```

## Run the tests

```bash
python test.py
```

## Weather agent (no API key required)

This project includes a lightweight weather agent that uses the Open-Meteo APIs and does not require an API key.

Run interactively:

```bash
python weather_agent.py
# then type a city name at the prompt, e.g. London
```

Non-interactive examples:

```bash
# Basic query (metric units):
python weather_agent.py --city "London"

# Use imperial units and pretty formatting:
python weather_agent.py --city "New York" --units imperial --pretty
```

Interactive mode also accepts `exit` or `quit` to stop.
