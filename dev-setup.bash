#!/usr/bin/env bash

# Get the directory where this script lives
DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$DIR"
[[ ! -d "venv" ]] && python3 -m venv venv && venv/bin/pip3 install pip wheel --upgrade
venv/bin/pip3 install -r requirements.txt --upgrade

if [[ ! -f "$HOME/.config/mongo-helper/settings.ini" ]]; then
    mkdir -pv "$HOME/.config/mongo-helper"
    cp -av mongo_helper/settings.ini "$HOME/.config/mongo-helper"
fi
