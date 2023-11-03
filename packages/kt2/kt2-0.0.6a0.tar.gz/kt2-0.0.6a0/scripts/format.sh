#!/bin/bash
SOURCES="koppeltaal tests"

echo "Running isort..."
isort $SOURCES
echo "-----"

echo "Running black..."
black --skip-string-normalization $SOURCES
