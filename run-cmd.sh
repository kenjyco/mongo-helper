#!/usr/bin/env bash


run_cmd() {
    if [[ -z "$@" ]]; then
        echo "No python command passed in"
        return 1
    fi
	for venv_name in venv_py*; do
		echo -e "\n\n\n%%%%%%%%%%%%%%%\n  $(echo $venv_name | tr '[a-z]' '[A-Z]')\n%%%%%%%%%%%%%%%"
        echo $@
        ${venv_name}/bin/python -c "$@"
	done
}

run_cmd "import mongo_helper as mh; import pymongo; print('pymongo: {}'.format(pymongo.__version__))"