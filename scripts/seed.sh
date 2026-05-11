#!/usr/bin/env bash
set -e

docker compose exec api python seed.py
