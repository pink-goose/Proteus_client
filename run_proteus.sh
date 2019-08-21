#!/bin/bash

# Here could be some Copyright,
# Licenses and rights


script=${0}

function help() {
    echo "${script}:  Proteus launcher"
    echo "Usage: ${script} [COMMAND]"
    echo
    echo "COMMANDS:"
    echo "  all           run all services of Proteus"
    echo "  cli           run only cli of Proteus"
    echo "  background    run Proteus in background without cli"
    echo
    echo "Examples:"
    echo "  ${script} all"
    echo "  ${script} cli"
    echo "  ${script} background"

    exit 1
}

function launch-all() {
    python3 src/app.py init_main  > /dev/null &
    python3 src/app.py init_cli
    # possible variant for future
    # python3 -m services.main > /dev/null &
}

function launch-background() {
    python3 src/app.py init_main &
}

function launch-cli() {
    python3 src/app.py init_cli
}

opt=$1

case ${opt} in
    "all")
        launch-all
        ;;
    "cli")
        launch-cli
        ;;
    "background")
        launch-background
        ;;
    *)
        help
        ;;
esac
