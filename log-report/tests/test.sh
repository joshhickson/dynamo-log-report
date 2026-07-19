#!/bin/bash

# pytest and pytest-json-ctrf are baked into the environment image
# (environment/Dockerfile), so nothing is installed at verify time.
# Deliberately no `set -e`: a failing test suite is a reward of 0, not a
# verifier crash.

mkdir -p /logs/verifier

pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA
status=$?

if [ $status -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
