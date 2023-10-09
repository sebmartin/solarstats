# Solarstats

A very simple engine for collecting statistics from a solar charge controller.

Solarlstats works by polling `probes` for stats and persisting them with `writers`.  Probes and Writers are generic objects that can be extended to integrate with different data sources and backends. A running instance of solarstats can be configured with multiple probes and multiple writers.

The probes and writers are configured [via a simple YAML config file](config/README.md).

e.g.

```yaml
frequency: 5.0
logging_level: INFO
probes:
  RenogyRover:
    device: /dev/ttyUSB0
    address: 1
writers:
  Http:
    port: 5555
  Sql:
    connection: sqlite:///solarstats.sqlite
```

The main (only?) probe availabe in this implementation is for communicating with Renogy charge controllers via the RS232 port. The implementation of the Renogy probe is heavily based on https://github.com/corbinbs/solarshed. This repo builds on this by adding tests and improving ergonomics.

# Running solarstats

Tested with python 3.11 but probably works with earlier versions.

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m solarstats
```

The output will look something like this:
```
2023-10-04 22:21:44 - __main__ - INFO | Loaded configuration from: /Users/seb/Documents/Dev/solarstats/config/config.yaml
2023-10-04 22:21:44 - engine - INFO | ================================================================================
2023-10-04 22:21:44 - engine - INFO | Starting probes. Press CTRL-C to terminate
2023-10-04 22:21:44 - engine - INFO | Polling with probe RenogyRoverSimulator
2023-10-04 22:21:44 - probes.renogy - INFO | Polling contoller RenogyRoverControllerSimulator
2023-10-04 22:21:44 - engine - INFO | Writing to Http
2023-10-04 22:21:44 - writers.http - INFO | Starting http server at: http://localhost:5555
2023-10-04 22:21:44 - engine - INFO | Writing to Sql
2023-10-04 22:21:44 - writers.sql - INFO | Writing metrics for provider RenogyRoverSimulator@0.1
2023-10-04 22:21:49 - engine - INFO | Polling with probe RenogyRoverSimulator
2023-10-04 22:21:49 - probes.renogy - INFO | Polling contoller RenogyRoverControllerSimulator
2023-10-04 22:21:49 - engine - INFO | Writing to Http
2023-10-04 22:21:49 - engine - INFO | Writing to Sql
2023-10-04 22:21:49 - writers.sql - INFO | Writing metrics for provider RenogyRoverSimulator@0.1
^C2023-10-04 22:21:50 - __main__ - INFO | Done
```

# Simulator

You might have noticed that the logs above mention the `RenogyRoverSimulator` controller. This is a
handy stand in for the real Renogy probe for testing solarstats when not connected to a real solar
controller.

The simulator works by taking a SQL database as a source of metrics and simply replays them at a given interval. The configuration for the example above looks like this:

```yaml
frequency: 5.0
logging_level: INFO
probes:
  # RenogyRover:
  #   device: /dev/ttyUSB0
  #   address: 1
  RenogyRoverSimulator:
    connection: sqlite:///solarstats.simulated.sqlite  # source of fake metrics
writers:
  Http:
    port: 5555
  Sql:
    connection: sqlite:///solarstats.sqlite
```

You can use the `Sql` writer when connected with the real `RenogyRover` probe to generate your own database of metrics that can be used directly with the simulator.