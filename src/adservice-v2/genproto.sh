#!/bin/bash -eu

set -e


# Add the commands to generate the gRPC files
PROTODIR=../../pb

python3 -m  grpc_tools.protoc -I $PROTODIR --python_out=./ --grpc_python_out=./ demo.proto