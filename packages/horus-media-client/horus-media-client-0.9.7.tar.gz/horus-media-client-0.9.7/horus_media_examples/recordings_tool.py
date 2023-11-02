# Copyright(C) 2021 Horus View and Explore B.V.

import psycopg2
import sys

from horus_db import Frames, Recordings, Frame, Recording
from . import util

# This example shows how to iterate over all the recordings

# Command line input handling
parser = util.create_argument_parser()
util.add_database_arguments(parser)
util.add_server_arguments(parser)

args = parser.parse_args()

connection = util.get_connection(args)
recordings = Recordings(connection)

cursor = recordings.all()

recording = Recording(cursor)

while recording is not None:
    print(recording, " -> ", recording.directory)
    recording = Recording(cursor)
