#!/usr/bin/env bash
set -e

pip install "grpcio-tools>=1.15.0"
python -m grpc_tools.protoc -I./proto --pyi_out=./chimera_llm_proto --python_out=./chimera_llm_proto --grpc_python_out=./chimera_llm_proto ./proto/chimera_llm.proto
2to3 -n -w ./chimera_llm_proto/*_pb2*
