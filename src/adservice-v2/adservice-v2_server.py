#!/usr/bin/python

import os
import random
import time
import traceback
from concurrent import futures

import grpc

from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc

# generated pb2 files from ../../pb/demo.proto
import demo_pb2
import demo_pb2_grpc

from logger import getJSONLogger
logger = getJSONLogger('adservice-v2-server')

RANDOM_ADS_TO_SERVE = 2


class AdServiceV2(demo_pb2_grpc.ProductCatalogServiceServicer):
    
    # Implemet the Ad service business logic

    # Uncomment to enable the HealthChecks for the Ad service
    # Note: These are needed for the liveness and readiness probes
    def Check(self, request, context):
        return health_pb2.HealthCheckResponse(
            status=health_pb2.HealthCheckResponse.SERVING)
    
    def Watch(self, request, context):
        return health_pb2.HealthCheckResponse(
            status=health_pb2.HealthCheckResponse.UNIMPLEMENTED)

    def DisplayAds(self, request, context):
        channel =  grpc.insecure_channel("productcatalogservice:3550")
        stub = demo_pb2_grpc.ProductCatalogServiceStub(channel)
        output = stub.ListProducts(demo_pb2.Empty())

        # generating random product id(s) to display with text "AdV2 -  Items with 25% Discount!"
        random_product_ids =  random.choice(output.products, k=RANDOM_ADS_TO_SERVE)
        display_text = "AdV2 -  Items with 25% Discount!"
        random_ads = [demo_pb2.Ad(redirect_url="/product/{}".format(p.id), text=display_text) for p in random_product_ids]
        return demo_pb2.AdResponse(ads=random_ads)


if __name__ == "__main__":
    logger.info("initializing adservice-v2")

  
    # create gRPC server, add the Ad-v2 service and start it
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=200))
    # Uncomment to add the HealthChecks to the gRPC server to the Ad-v2 service
    health_pb2_grpc.add_HealthServicer_to_server(AdServiceV2(), server)
    demo_pb2_grpc.add_AdServiceV2Servicer_to_server(AdServiceV2(), server)
    print("gRPC Server starting on port 9556...")
    server.add_insecure_port('[::]:9556')
    server.start()
    server.wait_for_termination()