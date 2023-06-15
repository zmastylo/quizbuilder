#!/bin/zsh

usage() {
  echo "$0: module location"
}

param_num="$#"
[ ${param_num} -ne 1 ] && usage && exit 1;


location=$1

command echo "Run code checks at: ${location}"
command echo "Check/fix code formatting."
python -m black --include \.py ${location}

command echo "Check for code complexity."
python3 -m flake8 --max-complexity 7 ${location}

command echo "Check imports."
python3 -m isort ${location}

