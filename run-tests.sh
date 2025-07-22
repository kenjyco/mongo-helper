#!/usr/bin/env bash

echo -e "\n\n\n\n\n\n\n\n\n"
for venv_name in venv_py[0-9\.]*_**; do
# for venv_name in venv_py*pymongo3.7.2*; do
# for venv_name in venv_py3.1**pymongo3.10.0*; do
    echo -e "\n\n\n%%%%%%%%%%%%%%%\n  $(echo $venv_name | tr '[a-z]' '[A-Z]')\n%%%%%%%%%%%%%%%"
    ${venv_name}/bin/pytest
done