#!/bin/bash

# Loop through all json files in all subdirectories
for f in $(find $1 -name '*.json' ! -name '*.dbg.json' ! -name '*_abi.json'); do
  filename=$(basename -- "$f")

  # Use jq to extract the "abi" field and replace boolean literals
  jq '.abi' $f > "${filename%.json}.json"
done

