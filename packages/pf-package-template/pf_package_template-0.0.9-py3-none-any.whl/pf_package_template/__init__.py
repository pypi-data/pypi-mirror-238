from promptflow import PFClient
from os import path


def main(inputs, connections=None):
    pf_client = PFClient()
    flow_results = pf_client.test(flow=path.dirname(__file__), inputs=inputs)
    return flow_results