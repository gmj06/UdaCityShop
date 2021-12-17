#!/bin/bash -eu

set -e

# TODO: Add the commands to generate the gRPC files
python3 -m grpc_tools.protoc -I../../pb --python_out=. --grpc_python_out=. ../../pb/demo.proto

