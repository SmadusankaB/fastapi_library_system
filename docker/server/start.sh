#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset
uvicorn main:app  --host 0.0.0.0 --port 8000