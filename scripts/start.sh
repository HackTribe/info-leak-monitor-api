#!/bin/env bash
#
BASEPATH=$(cd `dirname $0`; pwd)

if type supervisord >/dev/null 2>&1; then
    supervisord
fi

$BASEPATH/wait-for-it.sh database:3306 -- alembic revision --autogenerate -m "init" && alembic upgrade head &&uvicorn main:app --host 0.0.0.0 --port 80 --reload
