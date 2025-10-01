#!/bin/bash

alembic upgrade head
exec python3 -m backend.main
