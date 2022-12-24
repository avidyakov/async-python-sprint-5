#!/usr/bin/env bash

(cd src && alembic upgrade head)
python src/main.py
