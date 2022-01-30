#!/usr/bin/env bash

echo Apply migrations...

flask db upgrade
#flask db downgrade
echo migrations ok
exec "$@"