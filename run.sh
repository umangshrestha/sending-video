#!/bin/bash

help () {
cat <<-EOF
    --------------
    Help Menu
    --------------
    $(grep -ioE "version='([0-9]\.[0-9]\.[0-9])'" setup.py)
    --init | -i # creates virtual env 
            # and adds current dir to PYTHONPATH
    --test | -t # runs unittest for the given modules
    --run  | -r # tuns the code
    --build | -b # creates whl files
    --help | -h # displays help menu
    --------------
EOF
}


init () {
    # runs the virtual environemnt
    . venv/bin/activate
    # needs to be run to enable pytest
    pip install -e
}

test () {
    # I have spend lot of time pondering over 
    # which is the best way to deal with path 
    # related issues in pytest and python as
    # whole. Not sure this is an standard
    # practice but it works for me. If anyone
    # knows better way kindly let me know 
    python -m pytest -cov=src/ tests
}

freeze () {
    # stores the python dependencies to
    # requrements.txt file 
    pip freeze > requirements.txt
}

run () {
    # runs the video code
    python src/lib_video.py
}

build () {
    # this creates the whl file in the
    python setup.py bdist_wheel

}

main () {
    case $1
    in
    --init   | -i)  init ;;
    --test   | -t) test ;;
    --help   | -h) help ;;
    --run    | -r) run ;;
    --freeze | -f) freeze ;;
    --build  | -b) build ;;
    *) help ;; 
    esac
}

main "$@"