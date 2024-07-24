#!/bin/bash

pip3 install -r requirements.txt

if [ ! -f .env ] || ! grep -q "NVIDIA_API_KEY" .env; then
    echo ""
    echo "Creating .env file"
    touch .env
    echo "Please enter your NVIDIA API key:"
    read api_key
    echo "NVIDIA_API_KEY=$api_key" > .env
    echo ""
    echo ".env file created with API key."
else
    echo ""
    echo ".env file with API key already exists."
fi

printf '%0.s-' {1..100}
echo
echo ""
echo "Running the Script..."
echo ""
python rename_image.py
