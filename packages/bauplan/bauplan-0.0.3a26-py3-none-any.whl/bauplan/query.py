import os

import grpc
import pyarrow.flight
from grpc import (
    ssl_channel_credentials,
)

from .protobufs.bauplan_pb2 import TriggerRunRequest
from .protobufs.bauplan_pb2_grpc import CommanderServiceStub


def dial_commander():
    addr = ''
    if os.getenv('BPLN_ENV') == 'local':
        addr = 'localhost:2758'
    elif os.getenv('BPLN_ENV') == 'dev':
        addr = 'commander-poc.use1.adev.bauplanlabs.com:443'
    elif os.getenv('BPLN_ENV') == 'qa':
        addr = 'commander-poc.use1.aqa.bauplanlabs.com:443'
    else:
        addr = 'commander-poc.use1.aprod.bauplanlabs.com:443'
    creds = ssl_channel_credentials()
    conn = grpc.secure_channel(addr, creds)
    return conn


def query(
    query: str,
    max_rows: int = 10,
    no_cache: bool = False,
    branch: str = 'main',
    args: dict = None
):
    conn = dial_commander()
    client = CommanderServiceStub(conn)

    trigger_run_request = TriggerRunRequest(
        module_version='0.0.1',
        args=args or {},
        query_for_flight=query,
        is_flight_query=True
    )

    if no_cache:
        trigger_run_request.args['runner-cache'] = 'off'

    if branch:
        trigger_run_request.args['read-branch'] = branch

    job_id = client.TriggerRun(trigger_run_request)

    log_stream = client.SubscribeLogs(job_id)

    flight_endpoint = None
    for log in log_stream:
        # TODO(nathanleclaire): Better log type checking
        if log.task_lifecycle_event.flight_endpoint:
            flight_endpoint = log.task_lifecycle_event.flight_endpoint
            break

    if not flight_endpoint:
        return None

    flight_client = pyarrow.flight.FlightClient('grpc://'+flight_endpoint)
    options = pyarrow.flight.FlightCallOptions(
        headers=[(b'authorization', 'Bearer my_special_token'.encode())]
    )
    ticket = next(flight_client.list_flights(
        options=options,
    )).endpoints[0].ticket
    reader = flight_client.do_get(
        ticket,
        options=options,
    )
    return reader.read_all()
