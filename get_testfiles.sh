#!/bin/bash

mkdir -p test_files

wget -q https://storage.googleapis.com/rs-streaming-testdata/sweeps.zip
unzip -d test_files/ sweeps.zip

rm sweeps.zip
echo "Got testfiles."
