# Configuration

## Configuration files

By default, solarstats looks for a file in this directory called `config.yaml`. This file
contains all parameters to configure:
- The engine
- The probes
- The writers

The configuration schema is quite simple. At the root are keys for each constructure argument
for the Engine class.

The `probes` and `writers` keys in the root of the config are dictionaries where:
- each key is the name of a probe or writer
- the value is a nested dict wher the key/value pairs match each probe/writer's constructer arguments

## Example config

Example `config/config.yaml`:

```yaml
frequency: 1.0
probes:
  probe1:
    arg1: 1
  probe2:
    arg2: two
writers:
  writer1:
    arg1: 1
    arg2: two
```