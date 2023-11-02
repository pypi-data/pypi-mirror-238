# Copyright(C) 2021 Horus View and Explore B.V.
"""Horus Media Server strategy example

Example utility
"""

import psycopg2
import argparse
import logging

from horus_media import Client, Geometry


class read_arguments_from_file(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        file_name = None
        if option_string == "--db-file":
            file_name = namespace.db_file

        if option_string == "--s-file":
            file_name = namespace.s_file

        if file_name != None:
            f = open(file_name, "r")
            parser.parse_args(f.read().split(), namespace)


def create_argument_parser():
    return argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )


def add_database_arguments(parser):
    # db
    parser.add_argument(
        "--db-name", type=str, default="HorusWebMoviePlayer", help="the database name"
    )
    parser.add_argument(
        "--db-user",
        type=str,
        default="postgres",
        help="database user name used to authenticate",
    )
    parser.add_argument(
        "--db-password", type=str, help="database password used to authenticate"
    )
    parser.add_argument(
        "--db-host",
        type=str,
        default="localhost",
        help="database database host address",
    )
    parser.add_argument(
        "--db-port", type=int, default=5432, help="database connection port number"
    )

    parser.add_argument(
        "--db-file",
        help="database configuration file",
        type=str,
        default="input/db.conf",
        action=read_arguments_from_file,
        nargs=0,
    )


def add_server_arguments(parser):
    parser.add_argument(
        "-s",
        "--server",
        metavar="URL",
        type=str,
        default="http://localhost:5050/web/",
        help="Horus Media Server endpoint",
    )
    parser.add_argument(
        "-st",
        "--server-timeout",
        metavar="SECONDS",
        type=int,
        default=4,
        help="Horus Media Server timeout in seconds",
    )
    parser.add_argument(
        "-sa",
        "--server-attempts",
        metavar="ATTEMPTS",
        type=int,
        default=5,
        help="Horus Media Server number of attempts on connection failure",
    )

    parser.add_argument(
        "--s-file",
        help="server configuration file",
        type=str,
        default="input/server.conf",
        action=read_arguments_from_file,
        nargs=0,
    )


def add_size_argument(parser, default=(1024, 1024)):
    parser.add_argument(
        "-S",
        "--size",
        metavar=("WIDTH", "HEIGHT"),
        nargs=2,
        type=int,
        default=default,
        help="size of the image",
    )


def add_geometry_arguments(parser):
    parser.add_argument(
        "-gsc",
        "--geom-scale",
        type=int,
        default=400,
        help="output scale in px/m (orthographic)",
    )
    parser.add_argument(
        "-gw",
        "--geom-width",
        type=float,
        default=6,
        help="geometry width (orthographic)",
    )
    parser.add_argument(
        "-gh",
        "--geom-height",
        type=float,
        default=2,
        help="geometry height (orthographic)",
    )
    parser.add_argument(
        "-gd",
        "--geom-dist",
        type=float,
        default=4,
        help="geometry distance (orthographic)",
    )
    parser.add_argument(
        "-gs",
        "--geom-shift",
        type=float,
        default=0,
        help="geometry shift (orthographic)",
    )


def get_database_connection_string(args):
    db_params = [
        ("host", args.db_host),
        ("port", str(args.db_port)),
        ("dbname", args.db_name),
        ("user", args.db_user),
        ("password", args.db_password),
    ]

    return " ".join(map("=".join, filter(lambda x: x[1] != None, db_params)))


def get_connection(args):
    try:
        return psycopg2.connect(get_database_connection_string(args))
    except psycopg2.OperationalError as exception:
        logging.error(f"{exception} Connecting to database")
        exit()


def get_geometry(args, altitude_next=None):
    return Geometry(
        args.geom_scale,
        args.geom_width,
        args.geom_height,
        args.geom_dist,
        args.geom_shift,
        altitude_next,
    )


def get_client(args):
    try:
        client = Client(args.server, args.server_timeout)
        client.attempts = args.server_attempts
        return client
    except OSError as exception:
        logging.error(f"{exception}. Connecting to server {args.server}")
        exit(1)


def sample_script_header(name):
    if name == "__main__":
        print(
            f"This module is a sample script. It cannot run as an interactive example."
        )
        exit(1)
