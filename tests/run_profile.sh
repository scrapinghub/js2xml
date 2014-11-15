#!/bin/bash

abort() {
    echo "$*"; exit 1;
}

usage() {
    abort """Usage: $(basename $0) [PROFILE_NAME]

    Typical profiling workflow is:

    1) change code in profile.py
    2) (re-)run profiler passing a different name to use for file
    """
}

require() {
    type $1 >/dev/null 2>/dev/null
}

realpath(){
    if echo "$1" | grep -q '^/'
    then
        echo "$1"
    else
        echo $(cd $(dirname "$1") && pwd)/$(basename "$1")
    fi
}

while [ "${1#-}" != "$1" ]; do
    case "$1" in
        -h) usage;;
        *) usage;;
    esac
    shift
done
profile_name="${1:-output}"

require dot || abort "Please install graphviz first:   sudo apt-get install graphviz"
require gprof2dot || abort "Please install gprof2dot first:   pip install gprof2dot"

# stop script if some command fails
set -e

proj_dir=$(dirname $(dirname $(realpath $0)))

profile_py=$proj_dir/tests/profile.py

file_prefix=/tmp/profile-${profile_name}

echo "Running profile.py (output on ${file_prefix}.pstats)..."
PYTHONPATH=$proj_dir python -m cProfile -o ${file_prefix}.pstats $profile_py

echo "Generating image with profiling results..."
gprof2dot -f pstats ${file_prefix}.pstats | dot -Tpng -o ${file_prefix}.png

echo "Generated ${file_prefix}.png"
