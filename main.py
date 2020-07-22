import json

import grpc

from graphql import graphql_pb2_grpc
from graphql.graphql_pb2 import Request


def create_client():
    channel = grpc.insecure_channel("localhost:13024",)
    return graphql_pb2_grpc.GraphQLStub(channel)


query = """
subscription {
  searchTransactionsForward(query: "action:onblock", limit: 6) {
    trace {
      id
      block {
        num
        timestamp
      }
      matchingActions{
        account
        receiver
        name
        json
      }
    }
  }
}
"""

client = create_client()
stream = client.Execute(Request(query=query))

for rawResult in stream:
    if rawResult.errors:
        print("An error occurred")
        print(rawResult.errors)
    else:
        result = json.loads(rawResult.data)
        trace = result["searchTransactionsForward"]["trace"]
        block = trace["block"]
        print(block)
