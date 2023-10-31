#!/bin/bash
rm -rf ./build/*
rm -rf ./dist/*
flit build
flit publish
