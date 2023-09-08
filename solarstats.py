import argparse
from probes import ALL_CONTROLLERS, DEFAULT_CONTROLLER, Probe

from writers import MetricsWriter
from writers.http import HttpMetricsWriter
from writers.sql import SqlMetricsWriter


def parse_http(args) -> MetricsWriter:
    return HttpMetricsWriter(port=args.port)


def parse_sqlite(args) -> MetricsWriter:
    raise NotImplementedError("TODO")
    return SqlMetricsWriter(file=args.file)


def parse_controller(args) -> Probe:
    ctrl = args.controller
    Controller = ALL_CONTROLLERS[ctrl]
    return Controller(args)


def run(controller: Probe, writer: MetricsWriter):
    breakpoint()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog=__package__)
    parser.add_argument(
        "--controller",
        "-c",
        help="The PV controller",
        choices=[c.value for c in ALL_CONTROLLERS.keys()],
        default=DEFAULT_CONTROLLER,
    )

    subparsers = parser.add_subparsers(title="Output", help="output writers")

    sqlite_parser = subparsers.add_parser(
        "sqlite", help="Output stats to a sqlite database"
    )
    sqlite_parser.add_argument("--file", "-f", type=str, help="Path to sqlite database")
    sqlite_parser.set_defaults(parse_writer=parse_sqlite)

    http_parser = subparsers.add_parser(
        "http",
        help="Start an HTTP server to post stats which is useful for scraping from prometheus",
    )
    http_parser.add_argument(
        "--port", "-p", type=int, help="The port to use for the HTTP server"
    )
    http_parser.set_defaults(parse_writer=parse_http)

    args = parser.parse_args()
    writer = args.parse_writer(args)
    controller = parse_controller(args)
    run(controller=controller, writer=writer)
