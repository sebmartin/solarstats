# Solarstats

A very simple engine for collecting statistics from a solar charge controller.

Solarlstats works by polling `probes` for stats and persisting them with `writers`.  Probes and Writers are generic objects that can be extended to integrate with different data sources and backends. A running instance of solarstats can be configured with multiple probes and multiple writers.

The probes and writers are configured [via a simple YAML config file](config/README.md).

The main (only?) probe availabe in this implementation is for communicating with Renogy charge controllers via the RS232 port. The implementation of the Renogy probe is heavily based on https://github.com/corbinbs/solarshed. This repo builds on this by adding tests and improving ergonomics.

# Running solarstats

Tested with python 3.11 but probably works with earlier versions.

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m solarstats
```