#!/bin/bash

# Check if the user has provided the required input
if [ -z "$1" ]; then
  echo "Usage: $0 <file name>"
  exit 1
fi

python client/main.py fetch -r /ndn -f $1
