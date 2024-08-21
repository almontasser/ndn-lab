#!/bin/bash

# Check if the user has provided the required input
if [ -z "$1" ]; then
  echo "Usage: $0 <node number>"
  exit 1
fi

# Assign the user input to a variable
NODE_NUMBER=$1

# Run the Python script with the user-provided last character
python repo/main.py -rp /ndn -n /ndn${NODE_NUMBER}
