#!/usr/bin/python

import sys
import grpc

from logger import getJSONLogger
logger = getJSONLogger('adservice-v2-server')

if __name__ == "__main__":

   
    # set up server stub
    # ensure the service is listening to port 9556
    channel = grpc.insecure_channel("localhost:9556")
    stub = demo_pb2_grpc.AdServiceV2Stub(channel)

    
    # form a request with the required input
    ad_request = demo_pb2.AdRequest(context_keys="antique")

   
    # make a call to server and return a response
    response = stub.DisplayAds(ad_request)
    # Uncomment to log the resoinse from the Server
    logger.info(response)
