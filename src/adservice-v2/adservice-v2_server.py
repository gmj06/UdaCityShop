#!/usr/bin/python

import os
import random
import time
import traceback
from concurrent import futures

import grpc

from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc

#import these pb2 files after generating them

import demo_pb2
import demo_pb2_grpc

from logger import getJSONLogger
logger = getJSONLogger('adservice-v2-server')


class AdServiceV2(demo_pb2_grpc.AdServiceV2Servicer, health_pb2_grpc.HealthServicer):
    # TODO:
    # Implement the Ad service business logic

    # Uncomment to enable the HealthChecks for the Ad service
    # Note: These are needed for the liveness and readiness probes
    def Check(self, request, context):
        return health_pb2.HealthCheckResponse(status=health_pb2.HealthCheckResponse.SERVING)
    
    def Watch(self, request, context):
        return health_pb2.HealthCheckResponse(status=health_pb2.HealthCheckResponse.UNIMPLEMENTED)
    def Ads(self, request, context):
        # Define the channel and the stub from the pb2 file
        channel = grpc.insecure_channel("productcatalogservice:3550")
        stub = demo_pb2_grpc.ProductCatalogServiceStub(channel)
        response = stub.ListProducts(demo_pb2.Empty())
        # Find items based on random ID
        random_id = random.choices(response.products, k=3)
        # Define the URL and text to be displayed
        url = "/product/{}"
        display_text = "AdV2 - Items with 25% Discount!"
        # Define the ads with the url and text
        random_ads = [demo_pb2.Ad(redirect_url=url.format(p.id), text=display_text) for p in random_id]
        return demo_pb2.AdResponse(ads=random_ads)

if __name__ == "__main__":
    logger.info("initializing adservice-v2")

    # TODO:
    # create gRPC server, add the Ad-v2 service and start it
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=256))
    health_pb2_grpc.add_HealthServicer_to_server(AdServiceV2(), server)
    demo_pb2_grpc.add_AdServiceV2Servicer_to_server(AdServiceV2(), server)
    print("Server starting on port 9556...")
    server.add_insecure_port("[::]:9556")
    # start the server
    server.start()
    # Keep the thread alive
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
    
