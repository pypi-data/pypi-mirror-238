#!/bin/bash
set -e

SOURCES="kt2 tests"

echo "Running isort..."
isort --check $SOURCES
echo "-----"

echo "Running black..."
black --skip-string-normalization --experimental-string-processing $SOURCES
echo "-----"

echo "Running ruff..."
ruff --fix $SOURCES
echo "-----"

echo "All passed!"
